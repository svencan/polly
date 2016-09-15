import unittest
import os
import sys
import time
import shutil

sys.path.insert(0, os.path.abspath('..')) # import intuitively
from polly import core

class TestClasses(unittest.TestCase):

    def setUp(self):
        self.delete_afterwards = True
        core.MAIN_PATH = '../testdata-' + str(time.time()) + '/'
    
    def tearDown(self):
        '''Delete testdata folder'''
        if (self.delete_afterwards):
            shutil.rmtree(core.MAIN_PATH, ignore_errors=True)

    def test_identified(self):
        path       = 'event/'
        id         = 'lk161'
        identified = core.Identified(path, id)
        
        self.assertRaises(core.EmptyError, core.Identified, '', '')
        self.assertEqual(identified.url, path + id)
        self.assertEqual(identified.id, id)
    
    def test_timestamped(self):
        time_before = time.time()
        timestamped = core.Timestamped('event/', 'lk162')
        time_after  = time.time()
        
        self.assertTrue(time_before <= timestamped.timestamp <= time_after)
    
    def test_event(self):
        id    = 'lk161'
        short = 'LK16-1'
        long  = 'Landeskongress 16.1'
        event = core.Event(id, short, long)
        
        self.assertEqual(event.id, id)
        self.assertEqual(event.title.short, short)
        self.assertEqual(event.title.long, long)
        self.assertEqual(event.question, [])
        self.assertEqual(event.accreditation, [])
    
    def test_get_latest(self):
        id    = 'lk161'
        short = 'LK16-1'
        long  = 'Landeskongress'
        event1 = core.Event(id, short, long)
        event1.persist()
        time.sleep(1)
        event2 = core.Event(id, 'LK16--1', long)
        event2.persist()
        latest = core.Event.get_latest(id)

        self.assertEqual(event2.url, latest.url)
        
    def test_question(self):
        id    = 'lk161'
        short = 'LK16-1'
        long  = 'Landeskongress'
        event1 = core.Event(id, short, long)
        event1.persist()
    
        q_id    = 'lk161/question/säa1'
        q_short = 'SÄA1: Prokuratiounen'
        q_long  = 'SÄA 1: Prokuratiounen sinn doof'
        question = core.Question(q_id, q_short, q_long)
        question.persist()
        
        self.assertEqual(question.id, q_id)
        self.assertEqual(question.title.short, q_short)
        self.assertEqual(question.title.long, q_long)
        self.assertEqual(question.vote, [])
        self.assertEqual(question.opening, [])
        
    def test_question_inexistent_event(self):
        q_id    = 'lk121/question/säa1'
        q_short = 'SÄA1: Prokuratiounen'
        q_long  = 'SÄA 1: Prokuratiounen sinn cool!'
        question = core.Question(q_id, q_short, q_long)
        
        self.assertRaises(core.NotFoundError, question.persist)
        
        
if __name__ == '__main__':
    unittest.main()