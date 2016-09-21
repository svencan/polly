import os
import polly.core
import jsonpickle

def touch_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_directory(path):
    return os.path.exists(path)

def get_latest_file(path, name):
    versions = []
    files = os.listdir(path)
    
    for file in files:
        parts = file.split('_')
        if (parts[0] == name and len(parts) == 2):
            versions.append(float(parts[1]))
    
    if (not versions):
        return None
    
    file = path + name + '_' + str(max(versions))
    return file

def get_names(path):
    ''' Returns distinct set of timestamped filenames without the timestamp'''
    if not os.path.exists(path):
        return []
    
    files = os.listdir(path)
    names = set()
    
    for file in files:
        parts = file.split('_')
        if (len(parts) == 2) and (not parts[0] in names):
            names.add(parts[0])
    
    return names

def json_encode(o):
    return jsonpickle.encode(o)

def json_decode(json):
    return jsonpickle.decode(json)