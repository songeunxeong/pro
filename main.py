import flask
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import numpy as np
import pysynth as ps
from scipy.io import wavfile

app = Flask(__name__)


@app.route('/')
@app.route("/upload")
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def wav_transform():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'static/file1.wav')
        sr, data = wavfile.read('static/file1.wav')

        empty_notes = controller.NoteConvertor(data)
        notes = empty_notes.convertor()
        song = sum(notes, [])

        matrix = controller.MarcovMatrix(song)
        start_note = ['e4', 4]

        random_song = []
        for i in range(0, 100):
                start_note = matrix.next_note(start_note)
                random_song.append(start_note)

        ps.make_wav(random_song, fn='./random.wav')

        return render_template('wavplay.html')


if __name__ == '__main__':
    app.run(debug = True)
