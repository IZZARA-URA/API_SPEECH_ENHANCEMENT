#Vivee
import os
import time
import shutil

from zipfile import ZipFile
from werkzeug.utils import secure_filename
from flask import Flask, config, render_template, request, send_from_directory, flash, redirect, Markup

# wav2vec2 module
from wav2vec2.wav2vec2 import Wav2Vec2_larynx

# utill 
from utill import *

# initialising the flask app
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = "uploads/"

allowed_extensions = ['wav','txt']

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html', header= 'Home')

@app.route('/Wav2Vec2', methods = ['GET', 'POST'])
def wv():
    if request.method == 'GET':
        return render_template('wv.html', header= 'BETA 1.0.0v')

    namelist = []
    output_speech = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        if len(files) >= 1:
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) 

                output_speech.append(Wav2Vec2_larynx(app.config['UPLOAD_FOLDER'] + f'{f.filename}', True))
                

        for i in output_speech: 
            flash(Markup(f"<div class='alert alert-warning alert-dismissible fade show' role='alert' style='margin-top: 5px;'> \
                <strong>Prediction : </strong> {i}. \
                <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button> \
            </div>"))

        entries = os.listdir(app.config['UPLOAD_FOLDER'])
        for file2del in entries: 
            variableX1 = f'./uploads/{file2del}'
            os.remove(variableX1)
            print('remove', file2del)

        return redirect('/Wav2Vec2')

        '''
        #!Single file return text
        elif len(files) == 1:
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                    # print(OUTPUT_WAV2VEC2)
                    OUTPUT_SPEECH = Wav2Vec2_larynx(f)

                    flash(Markup(
                        f"<div class='alert alert-warning alert-dismissible fade show' role='alert' style='margin-top: 5px;'> \
                            <strong>Prediction : </strong> {OUTPUT_SPEECH}. \
                            <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button> \
                        </div>"
                        ))
                    return redirect('/MackCycleGan-VC') 
        '''

@app.route('/Wav2Vec2_test', methods = ['GET', 'POST'])
def test_wv():
    if request.method == 'GET':
        return render_template('wv_test.html', header= 'BETA 1.0.0v')

    namelist = []
    link = None
    # OUTPUT_SPEECH = 'ปราสาทหิน ผุผุ พังพัง กลางแดดเปรี้ยงเชียวนะคุณ'
    OUTPUT_SPEECH = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        if len(files) > 1:
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) 
                    name_single = change_name_download('wav')
                    copy_file_current_dir(f'uploads\{f.filename}', f'ready2predict_single\{name_single}')

        # Methods for predicction Wav2Vec2
        entries = os.listdir('uploads/')
        for wavfile in entries : 
            variableX1 = f'./uploads/{wavfile}'
            variableX2 = Wav2Vec2_larynx(variableX1, True)
            print(variableX2)
    
        return render_template('wv_test.html', header= 'BETA 1.0.0v')

@app.route('/download/<path:name>', methods=['GET', 'POST'])
def download_file(name):
    cwd = os.getcwd()
    return send_from_directory(cwd, name, as_attachment=True)		

if __name__ == '__main__':
    app.run(debug=True) # running the flask app