# importing the required libraries
import os
import time
import shutil

from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename, send_file
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

def zip_file(directory):
    file_paths = []
    name_timestr = f'ready2down_multi/{time.strftime("%Y%m%d-%H%M%S")}.zip' 
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # writing files to a zipfile
    with ZipFile(name_timestr,'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
            #remove after zip thet file
            os.remove(file)
    print('All files zipped successfully!')
    return name_timestr

@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    namelist = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        print(len(files))
        for f in files:
            namelist.append(f.filename)
            if check_file_extension(f.filename):
                f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))) 
###################################################################################################
        # Save at upload
        # Process Speech Enhancement and reture new file to completed
        # For test I saved a file none processing and change name to 0001_001_New.wav from uploads

        # save name at complete for zip all folders
                new_name = change_name(f.filename)
                cwd = os.getcwd()
                source = os.path.join(cwd, f'uploads\{f.filename}') 
                destination = os.path.join(cwd, f'completed\{new_name}')
                shutil.copyfile(source, destination)
###################################################################################################
        #zip file before send link to download and deleted file at completed
        name_download = zip_file('./completed') 
        return {"status":"success", "namelist":namelist, "link":f'http://127.0.0.1:5000/download/{name_download}'}

@app.route('/download/<path:name>', methods=['GET', 'POST'])
def download_file(name):
    cwd = os.getcwd()
    return send_from_directory(
        cwd, name, as_attachment=True
    )		
if __name__ == '__main__':
    app.run(debug=True) # running the flask app