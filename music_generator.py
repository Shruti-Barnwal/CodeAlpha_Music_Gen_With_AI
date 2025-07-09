def generate_music_file(output_path='static/generated_music.mid'):
    import os
    import numpy as np  
    import music21 as m21
    from keras.models import Sequential
    from keras.layers import LSTM, Dense, Dropout, Input
    from keras.utils import to_categorical
    from sklearn.preprocessing import LabelEncoder

    # MIDI to notes
    def midi_to_notes(midi_path):
        try:
            midi = m21.converter.parse(midi_path)
            notes = []
            for element in midi.flatten().notes:
                if isinstance(element, m21.note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, m21.chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
            return notes
        except Exception as e:
            print(f"Error reading {midi_path}: {e}")
            return []

    def find_midi_files(directory):
        midi_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.mid'):
                    midi_files.append(os.path.join(root, file))
        return midi_files

    midi_directory = 'midi_file'
    all_notes = []

    midi_files = find_midi_files(midi_directory)
    print(f"Found {len(midi_files)} MIDI files.")
    for midi_file_path in midi_files:
        notes = midi_to_notes(midi_file_path)
        if notes:
            all_notes.extend(notes)

    if not all_notes:
        print("No valid notes found. Training aborted.")
        return

    note_names = sorted(set(all_notes))
    encoder = LabelEncoder()
    encoder.fit(note_names)
    encoded_notes = encoder.transform(all_notes)

    #  Smaller sequence for faster training
    sequence_length = 50
    network_input = []
    network_output = []

    for i in range(len(encoded_notes) - sequence_length):
        input_sequence = encoded_notes[i:i + sequence_length]
        output_sequence = encoded_notes[i + sequence_length]
        network_input.append(input_sequence)
        network_output.append(output_sequence)

    network_input = np.reshape(network_input, (len(network_input), sequence_length, 1))
    network_output = to_categorical(network_output, num_classes=len(note_names))

    # Optimized model: smaller LSTM units
    model = Sequential()
    model.add(Input(shape=(sequence_length, 1)))
    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(128))
    model.add(Dense(len(note_names), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')
    model.fit(network_input, network_output, epochs=10, batch_size=32)

    # Generate new music
    def generate_music(model, network_input, encoder, num_generate=300):
        start_index = np.random.randint(0, len(network_input) - 1)
        pattern = network_input[start_index]

        generated_notes = []
        for _ in range(num_generate):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction = model.predict(prediction_input, verbose=0)
            index = np.argmax(prediction)
            result = encoder.inverse_transform([index])[0]
            generated_notes.append(result)
            pattern = np.append(pattern[1:], index)
            pattern = pattern[-sequence_length:]
        return generated_notes

    def notes_to_midi(notes, output_path):
        output_notes = []
        offset = 0
        for note in notes:
            if ('.' in note) or note.isdigit():
                chord_notes = [m21.note.Note(int(n)) for n in note.split('.')]
                chord = m21.chord.Chord(chord_notes)
                chord.offset = offset
                output_notes.append(chord)
            else:
                note_obj = m21.note.Note(note)
                note_obj.offset = offset
                output_notes.append(note_obj)
            offset += 0.5

        midi_stream = m21.stream.Stream(output_notes)
        midi_stream.write('midi', fp=output_path)

    generated_notes = generate_music(model, network_input, encoder)
    notes_to_midi(generated_notes, output_path=output_path)
    print(f" Music generated and saved to: {output_path}")
