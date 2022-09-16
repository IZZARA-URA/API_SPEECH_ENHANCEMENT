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
