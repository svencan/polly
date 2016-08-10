import unittest
import os
import sys
import time

sys.path.insert(0, os.path.abspath('..')) # import intuitively
from polly import core

class TestClasses(unittest.TestCase):

    def test_identified(self):
        path       = 'event/'
        id         = 'lk161'
        identified = core.Identified(path, id)
        
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
        long  = 'Landeskongress'
        event = core.Event(id, short, long)
        
        self.assertEqual(event.id, id)
        self.assertEqual(event.title.short, short)
        self.assertEqual(event.title.long, long)
    
    def test_get_latest(self):
        id    = 'lk161'
        short = 'LK16-1'
        long  = 'Landeskongress'
        event1 = core.Event(id, short, long)
        event2 = core.Event(id, short, long)
        event1.persist()
        event2.persist()
        latest = core.Event.get_latest(id)

        self.assertEqual(event2.url, latest.url)
        
if __name__ == '__main__':
    unittest.main()