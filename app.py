from flask import Flask, render_template, send_file
from music_generator import generate_music_file  # ye function aapne abhi banaya

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Ye HTML page dikhayega

@app.route('/generate', methods=['POST'])
def generate():
    output_path = 'static/generated_music.mid'
    generate_music_file(output_path)  # AI se music generate karega
    return send_file(output_path, as_attachment=True)  # Download link

if __name__ == '__main__':
    app.run(debug=True)
