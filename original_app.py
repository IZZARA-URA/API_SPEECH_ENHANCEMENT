#Vivee
import os
import time
import shutil

import flask
from zipfile import ZipFile
from werkzeug.utils import secure_filename
from flask import Flask, config, render_template, request, send_from_directory, flash, redirect, Markup

# wav2vec2 module
from wav2vec2.wav2vec2 import Wav2Vec2_larynx

# initialising the flask app
app = Flask(__name__)
app.secret_key = "super secret key"

# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = "uploads/"

# configuring the allowed extensions
allowed_extensions = ['wav','txt']

def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

def change_name(name):
    l = name.split('.')
    new_name = f'{l[0]}_NEW.{l[1]}'
    return new_name

def change_name_download(extend):
    name_timestr = f'{time.strftime("%Y%m%d-%H%M%S")}.{extend}' 
    return name_timestr

def zip_file(directory):
    file_paths = []
    dir_down= f"ready2down_multi/{change_name_download('zip')} "
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    print(file_paths)
    with ZipFile(dir_down,'w') as zip:
        for file in file_paths:
            zip.write(file)
            #remove after zip thet file
            os.remove(file)
    print('All files zipped successfully!')
    return dir_down

def copy_file_current_dir(source, destination):
     cwd = os.getcwd()
     source = os.path.join(cwd, source) 
     destination = os.path.join(cwd, destination)
     shutil.copyfile(source, destination)  

#@app.route('/MackCycleGan-VC')
#def mvc():
#   return render_template('mvcNew.html', header= 'BETA 1.0.0v')

@app.route('/MackCycleGan-VC', methods = ['GET', 'POST'])
def upload_mvc():
    if request.method == 'GET':
        return render_template('mvcNew.html', header= 'BETA 1.0.0v')
    namelist = []
    link = None
    if request.method == 'POST':
        files = request.files.getlist('files')
        #!Multifile
        if len(files) > 1:
            print(len(files))
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) 

        # ?Process Speech Enhancement and reture new file to completed
                    def speech_bad_to_good():
                        #
                        #
                        #
                        #
                        return None # The good sound save at complete (for zip file)
        # ?For test I change name to 0001_001_New.wav from uploads then saved a file none processing at complete for zip fileand 
        # save name at complete for zip all folders
                    new_name = change_name(f.filename)
                    copy_file_current_dir(f'uploads\{f.filename}', f'completed\{new_name}')
        #zip file before send link to download and deleted file at completed
            dir_down = zip_file('./completed') 
            link = f'http://127.0.0.1:5000/download/{dir_down}'
            #return {"status":"success", "type":"zip" ,"namelist":namelist, "link":f'http://127.0.0.1:5000/download/{dir_down}'}, 201
            #flash(f'You have file {len(namelist)} file for process,<a href="{link}">Click this!!</a> click to download')
            #flash(Markup(f'<strong>Successfully for {len(namelist)} processing!</strong> Please click <a href='{link}' class='closePopUp'>Download</a>))
            flash(Markup(f"<div class='alert alert-success alert-dismissible fade show' role='alert' style='margin-top: 5px;'><strong>Successfully for {len(namelist)} processing!</strong> <br> Please click <a href='{link}' class='closePopUp'>Download</a><button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>"))
            return redirect('/MackCycleGan-VC')

        #!Single file return .wav
        elif len(files) == 1:
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename)))


        # ?Process Speech Enhancement and reture new file to completed
                    def speech_bad_to_good():
                        #
                        #
                        #
                        #
                        return None # The good sound save at ready2down_single
        # ?In true Must use file from upload (f.filename) to process | after process must save in ready2down_single 
        # For test I  use file non process at uploads and save in ready2down_single       
                    name_single = change_name_download('wav')
                    copy_file_current_dir(f'uploads\{f.filename}', f'ready2down_single\{name_single}')

                    #return {"status":"success", "type":"wav","namelist":namelist, "link":f'http://127.0.0.1:5000/download/ready2down_single/{name_single}'}
                    link = f'http://127.0.0.1:5000/download/ready2down_single/{name_single}'
                    flash(Markup(f"<div class='alert alert-success alert-dismissible fade show' role='alert' style='margin-top: 5px;'><strong>Successfully for {len(namelist)} processing!</strong> <br> Please click <a href='{link}' class='closePopUp'>Download</a><button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button></div>"))
                    return redirect('/MackCycleGan-VC')

        flash(Markup(
            f"<div class='alert alert-warning alert-dismissible fade show' role='alert' style='margin-top: 5px;'> \
                <strong>You are't upload!</strong> Please upload file. \
                <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button> \
              </div>"
            ))
        return redirect('/MackCycleGan-VC')

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




    #    #!Single file return text
    #     elif len(files) == 1:
    #         for f in files:
    #             namelist.append(f.filename)
    #             if check_file_extension(f.filename):
    #                 f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
    #                 # print(OUTPUT_WAV2VEC2)
    #             OUTPUT_SPEECH = Wav2Vec2_larynx(f)

    #             flash(Markup(
    #                     f"<div class='alert alert-warning alert-dismissible fade show' role='alert' style='margin-top: 5px;'> \
    #                         <strong>Prediction : </strong> {OUTPUT_SPEECH}. \
    #                         <button type='button' class='btn-close' data-bs-dismiss='alert' aria-label='Close'></button> \
    #                     </div>"
    #                  ))
    #             return redirect('/MackCycleGan-VC') 

@app.route('/download/<path:name>', methods=['GET', 'POST'])
def download_file(name):
    cwd = os.getcwd()
    return send_from_directory(
        cwd, name, as_attachment=True
    )		

if __name__ == '__main__':
    app.run(debug=True) # running the flask app