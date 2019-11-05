import flask
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from scipy.io import wavfile
import librosa
import random
import pysynth as ps
import controller

app = Flask(__name__)


@app.route('/')
@app.route("/upload")
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def wav_transform():
    if request.method == 'POST':
        f = request.files['file']
        random_length = request.form['length']
        random_length = int(random_length)
        f.save(f'static/original_song.wav')
        try:
            sr, data = wavfile.read('static/original_song.wav')
        except ValueError:
            return render_template('error.html')  #wav파일외업로드시 error페이지로 이동

        y, sr1 = librosa.load('static/original_song.wav')
        bpm, beats = librosa.beat.beat_track(y=y, sr=sr1)

        convertor = controller.NoteTempoConvertor(data, bpm, sr)
        song = convertor.convert()

        composition_model = controller.MarcovMatrix(song)
        candidate = composition_model.uniq_song
        choice = random.randrange(0, len(candidate)-1)
        start_note = candidate[choice]

        random_song = []
        for i in range(0, random_length):
                start_note = composition_model.next_note(start_note)
                random_song.append(start_note)

        ps.make_wav(random_song, fn='static/random.wav')

        return render_template('wavplay.html')


if __name__ == '__main__':
    app.run(debug = True)
