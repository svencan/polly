import time
import os

from polly import helpers
from polly import errors

MAIN_PATH = '../data/' # Folder to store data

class Identified:
    def __init__(self, path, id):
        if (path.strip() == '' or id.strip() == ''):
            raise errors.EmptyError('path and id must not be empty')
        
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
        file = open(helpers.get_latest_file(path, filename), 'r')
        json = file.read()
        file.close()
        return helpers.json_decode(json)

class Question(Timestamped):
    def __init__(self, id, short_title, long_title):
        super().__init__(MAIN_PATH + 'event/', id)
        self.title = Title(short_title, long_title)
        self.vote = []
        self.opening = []
        
    def persist(self):
        url_parts = self.url.split('/')
        event_path = url_parts[:-2 or None]
        event_exists = helpers.check_directory('/'.join(event_path))
        
        if (event_exists == False):
            raise errors.NotFoundError('Event does not exists')
        
        helpers.touch_directory(self.url)
        file = open(self.url + '/description_' + str(self.timestamp), 'w')
        file.write(helpers.json_encode(self))
        file.close()
    
    def get_votes():
        pass
    
    def get_openings():
        pass
    
    @staticmethod
    def get_latest(id):
        path = MAIN_PATH + 'event/' + id + '/'
        filename = 'description'
        file = open(helpers.get_latest_file(path, filename), 'r')
        json = file.read()
        file.close()
        return helpers.json_decode(json)
        
class Member(Timestamped):
    def __init__(self, id, short_title, long_title):
        super().__init__(MAIN_PATH + 'member/', id)
        self.title = Title(short_title, long_title)
    
    def persist(self):
        helpers.touch_directory(MAIN_PATH + 'member/')
        file = open(self.url + '_' + str(self.timestamp), 'w')
        file.write(helpers.json_encode(self))
        file.close()
    
    @staticmethod
    def get_latest(id):
        path = MAIN_PATH + 'member/'
        filename = id
        file = open(helpers.get_latest_file(path, filename), 'r')
        json = file.read()
        file.close()
        return helpers.json_decode(json)