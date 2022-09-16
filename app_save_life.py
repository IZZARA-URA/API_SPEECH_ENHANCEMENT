# importing the required libraries
import os
import time
import shutil

from flask import Flask, config, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from zipfile import ZipFile


# initialising the flask app
app = Flask(__name__)


# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = "uploads/"

# configuring the allowed extensions
allowed_extensions = ['wav']

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

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    namelist = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        #!Multifile
        if len(files) > 1:
            print(len(files))
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) 
##################################################################################################
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
###################################################################################################
        #zip file before send link to download and deleted file at completed
            dir_down = zip_file('./completed') 
            return {"status":"success", "type":"zip" ,"namelist":namelist, "link":f'http://127.0.0.1:5000/download/{dir_down}'}, 201

        #!Single file return .wav
        elif len(files) == 1:
            for f in files:
                namelist.append(f.filename)
                if check_file_extension(f.filename):
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename)))

##################################################################################################
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
###################################################################################################
                    return {"status":"success", "type":"wav","namelist":namelist, "link":f'http://127.0.0.1:5000/download/ready2down_single/{name_single}'}
        #!Nothing
        return {"status":"false"}
@app.route('/download/<path:name>', methods=['GET', 'POST'])
def download_file(name):
    cwd = os.getcwd()
    return send_from_directory(
        cwd, name, as_attachment=True
    )		
if __name__ == '__main__':
    app.run(debug=True) # running the flask app


    