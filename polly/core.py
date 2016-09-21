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

class Opening(Timestamped):
    def __init__(self, id):
        super().__init__(MAIN_PATH + 'event/', id)
    
    def persist(self):
        url_parts = self.url.split('/')
        question_path = url_parts[:-1 or None]
        question_exists = helpers.check_directory('/'.join(question_path))
        
        if (question_exists == False):
            raise errors.NotFoundError('Question does not exists')
        
        # Check opening and closure consistency
        id_parts = self.id.split('/')
        self.type = id_parts[-1]
        
        latest_opening_url = (('/'.join(id_parts[:-1])) + '/opening')
        latest_opening = Opening.get_latest(latest_opening_url)
        latest_closure_url = (('/'.join(id_parts[:-1])) + '/closure')
        latest_closure = Opening.get_latest(latest_closure_url)
        
        if (self.type == 'closure'):
            if (latest_closure != None and latest_closure.timestamp > latest_opening.timestamp):
                raise errors.InvalidValueError('Question is already closed')
                
            if (latest_opening == None):
                raise errors.InvalidValueError('Question is not open')
        
        if (self.type == 'opening'):
            if (latest_closure != None and latest_opening > latest_closure):
                raise errors.InvalidValueError('Question is already open')
            
            if (latest_opening != None):
                raise errors.InvalidValueError('Question is already open')
        
        # TODO: Check if opening after closure is allowed (config)?
        
        file = open(self.url + '_' + str(self.timestamp), 'w')
        file.write(helpers.json_encode(self))
        file.close()
    
    @staticmethod
    def get_latest(id):
        id_parts = id.split('/')
        type = id_parts[-1]
        question_id = '/'.join(id_parts[:-1])
    
        path = MAIN_PATH + 'event/' + question_id
        latest = helpers.get_latest_file(path + '/', type)
        if (latest == None):
            return latest
        
        file = open(latest, 'r')
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
        print(self.url)
    
    def get_openings():
        pass
    
    @staticmethod
    def get_latest(id):
        path = MAIN_PATH + 'event/' + id + '/'
        filename = 'description'
        file = open(helpers.get_latest_file(path, filename), 'r')
        json = file.read()
        file.close()
        
        question = helpers.json_decode(json)
        vote_path = question.url + '/vote'
        vote_names = helpers.get_names(vote_path)
        vote_count = {'aye': 0, 'nay': 0, 'abstention': 0, 'total': 0}
        votes = []
        
        for vote in vote_names:
            vote_parts = vote.split('/')
            vote_id = vote_parts[-1]
            votes.append(vote_id)
            vote = Vote.get_latest(question.id, vote_id)
            vote_count[vote.vote] += 1
            vote_count['total'] += 1
        
        question.votecount = vote_count
        question.vote = votes
        
        return question
        
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

class Vote(Timestamped):
    def __init__(self, event_id, question_id, member_id, vote):
        valid_votes = ['aye', 'nay', 'abstention']
        if (vote not in valid_votes):
            raise errors.InvalidValueError('Invalid vote')
        
        question_url = MAIN_PATH + 'event/' + question_id
        if (helpers.check_directory(question_url) == False):
            raise errors.NotFoundError('Event or question does not exist')
        
        members = helpers.get_names(MAIN_PATH + 'member/')
        if (member_id not in members):
            raise errors.NotFoundError('Member does not exist')
        
        # TODO check if question is opened
        # TODO check if member is accredited
        
        vote_url = MAIN_PATH + 'event/' + question_id + '/vote/'
        super().__init__(vote_url, member_id)
        self.vote = vote
        
    def persist(self):
        url_parts = self.url.split('/')
        vote_path = url_parts[:-1 or None]
        helpers.touch_directory('/'.join(vote_path))
        
        file = open(self.url + '_' + str(self.timestamp), 'w')
        file.write(helpers.json_encode(self))
        file.close()
        
    @staticmethod
    def get_latest(question_id, member_id):
        path = MAIN_PATH + 'event/' + question_id + '/vote/'
        filename = member_id
        file = open(helpers.get_latest_file(path, filename), 'r')
        json = file.read()
        file.close()
        return helpers.json_decode(json)