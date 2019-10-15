import flask
from flask import Flask, request, render_template
from sklearn.externals import joblib
import numpy as np
from scipy import misc
import pysynth as ps      # 노트 만들면 wav파일로 저장
from scipy.io import wavfile    # sample_rate, data 반환

app = Flask(__name__)
app.debug = True


# 메인 페이지 라우팅
@app.route("/")
@app.route("/upload")
def index():
    return render_template('index.html')

@app.route('/uploader', methods=['POST'])
def wav_freq_transform():
    if request.method == 'POST':
        # 업로드 파일 처리 분기
        f = request.files['music']        
        sr, data = scipy.io.wavfeil(f)
                    
        # 노트 추출
        empty_notes = controller.NoteConvertor.convert(data)
        notes = empty_notes.convertor()
        song = sum(notes, [])
        
        # 마르코프 추출
        matrix = controller.MarcovMatrix(song)
        start_note = ['c4', 4]

        # 작곡 추출
        random_song = []
        for i in range(0, 100):
                start_note = matrix.next_note(start_note)
                random_song.append(start_note)

        ps.make_wav(random_song, fn='./random.wav')

        return 

# Rest 등록
if __name__ == '__main__':
    # Flask 서비스 스타트
    app.run(host='0.0.0.0', port=8000, debug=True)
