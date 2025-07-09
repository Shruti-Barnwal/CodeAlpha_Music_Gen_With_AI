## 🎵 Listening to the Generated Music

This project generates music in the form of `.mid` (MIDI) files using AI models like LSTM.

To play the generated MIDI file without any software setup, follow these simple steps:

### 🔗 Online Playback (Recommended for Demo)

You can use an online MIDI player to listen to your generated music:

1. Visit: [https://onlinesequencer.net](https://onlinesequencer.net)
2. Click on **"Import MIDI"** (top-right corner)
3. Upload the `generated_music.mid` file from the project directory
4. Click the **▶ Play** button to listen to the generated music 🎶

> This is the easiest way to preview the output without installing any additional tools like VLC or SoundFont.

### 💻 Optional: Local Playback with VLC

If you want to play the MIDI file locally using VLC:

1. Download a SoundFont file (e.g., `FluidR3_GM.sf2`)
2. In VLC, go to **Tools > Preferences > Input / Codecs > Audio Codecs > FluidSynth**
3. Set the path to the `.sf2` file
4. Restart VLC and open the `.mid` file
