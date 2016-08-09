import time
import os

from polly import helpers

MAIN_PATH = '../data/' # Folder to store data

class Identified:
    def __init__(self, path, id):
        self.url = path + id
        self.id = id

class Timestamped(Identified):
    def __init__(self, path, id):
        super().__init__(path, id)
        self.timestamp = time.time()

class Title():
    def __init__(self, short, long):
        self.short = short
        self.long = long
        
class Event(Timestamped):
    def __init__(self, id, short_title, long_title):
        super().__init__(MAIN_PATH + 'event/', id)
        self.title = Title(short_title, long_title)
        self.question = []
        self.accreditation = []
    
    def persist(self):
        helpers.touch_directory(self.url)
        file = open(self.url + '/description_' + str(self.timestamp), 'w')
        
        file.write(helpers.json_encode(self))
        file.close()
    
    def get_questions():
        pass
        
    def get_accreditations():
        pass
    
    @staticmethod
    def get_latest(id):
        path = MAIN_PATH + 'event/' + id + '/'
        filename = 'description'
        file = helpers.get_latest_file(path, filename)