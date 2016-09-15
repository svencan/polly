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
        if parts[0] == name and len(parts) == 2:
            versions.append(float(parts[1]))

    file = path + name + '_' + str(max(versions))
    return file

def json_encode(o):
    return jsonpickle.encode(o)

def json_decode(json):
    return jsonpickle.decode(json)