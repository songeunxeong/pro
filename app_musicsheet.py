import flask
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from scipy.io import wavfile
from music21 import *
import librosa
import random
import controller
import pygame
import time

app = Flask(__name__)


@app.route('/')
@app.route("/upload")
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def wav_transform():
    if request.method == 'POST':
        f = request.files['file']
        if request.form['length']:
            random_length = request.form['length']
            random_length = int(random_length)
        else:
            random_length = 100
        f.save(f'static/original_song.wav')
        try:
            sr, data = wavfile.read('static/original_song.wav')
        except ValueError:
            return render_template('error.html')  #wav파일외업로드시 error페이지로 이동

        y, sr1 = librosa.load('static/original_song.wav')
        bpm, beats = librosa.beat.beat_track(y=y, sr=sr1)

        convertor = controller.NoteTempoConvertor(data, bpm, sr)
        song = convertor.convert()
        # global musicsheet_song
        global musicsheet_song
        musicsheet_song = convertor.for_musicsheet_song

        composition_model = controller.MarcovMatrix(song)
        candidate = composition_model.uniq_song
        choice = random.randrange(0, len(candidate)-1)
        start_note = candidate[choice]

        ## 보류
        random_song = []
        for i in range(0, random_length):
                start_note = composition_model.next_note(start_note)
                random_song.append(start_note)

        ## song/random_song
        midi = controller.MakeMidi(song, bpm, "static/random.midi")
        midi.makemidi()
        return render_template('midiplay2.html')

@app.route('/midi_play')
def midi_play():
    pygame.init()
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    BUFFER = 3072
    filename = "static/random.midi"
    pygame.mixer.init(freq, size, chan, BUFFER)

    clock = pygame.time.Clock()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(1000)

    return "nothing"

@app.route('/midi_stop')
def midi_stop():
    pygame.mixer.init()
    pygame.mixer.music.stop()

    return "nothing"

@app.route('/make_musicsheet')
def make_musicsheet():
#    global musicsheet_song
    song = musicsheet_song
    s = stream.Stream()

    for i, elm in enumerate(song):
        if elm[0] == 'r':
            n = note.Rest()
        else:
            n = note.Note(elm[0])
        n.duration.quarterLength = elm[1]
        s.append(n)
        
    s.show('vexflow')

    return "nothing"

if __name__ == '__main__':
    app.run(debug = True)
