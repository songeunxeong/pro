from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
@app.route("/upload")
def index():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f'static/file1.wav')
        return render_template('wavplay.html')


if __name__ == '__main__':
    app.run(debug = True)