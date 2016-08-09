import os
import json
import polly.core

from json import JSONEncoder

def touch_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_latest_file(path, name):
    
    files = os.listdir(path)
    
    for file in files:
        print(file + '\n')
    
    pass

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
    
def json_encode(o):
    print(json.dumps(o, cls=MyEncoder))
    return json.dumps(o, cls=MyEncoder)
    
