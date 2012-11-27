#!/usr/bin/env python
'''
Tests generated with gen_tests.py https://github.com/drsm79/gen_tests
'''
import unittest
import datetime
import json
from gen_docs import *


class GenDocTest(unittest.TestCase):
    """
    Tests for doc generating script
    """
    def test_gen_doc(self):
        """
        def gen_doc(schema)
        """
        pass

    def test_ipsum(self):
        """
        def ipsum(nlines)

        function takes a number of lines and returns that many lines of text
        """
        self.assertEqual(len(ipsum(5).split('\n')), 5)

    def test_randdate_stamp(self):
        """
        def randdate(field)

        function takes a field object and returns a date object
        field obejct:
            format : stamp | string
            output : stamp | string
            start
            end
        """
        startdate = 313135200
        enddate = 1317186000
        field = {'format': 'stamp', 'output': 'stamp', 'start': startdate, 'end': enddate}
        date = randdate(field)
        self.assertTrue(date > startdate) 
        self.assertTrue(enddate > date) 

    def test_randdate_string_out(self):
        """
        def randdate(field)

        function takes a field object and returns a date object
        field obejct:
            format : stamp | string
            output : stamp | string
            start
            end
        """
        startdate = 313135200
        enddate = startdate + 3600 #1317186000
        timefmt = "%B %d, %Y %H:%M:%S"

        field = {'format': 'stamp', 'output': 'string', 'start': startdate, 'end': enddate}
        date = randdate(field)
        date_as_num = time.mktime(time.strptime(date, timefmt))
        self.assertTrue(date_as_num > startdate) 
        self.assertTrue(enddate > date_as_num)

    def test_randdate_string_in(self):
        """
        def randdate(field)

        function takes a field object and returns a date object
        field obejct:
            format : stamp | string
            output : stamp | string
            start
            end
        """
        startdate = "December 04, 1979 00:00:00"
        enddate = "September 28, 2011 00:00:00"
        timefmt = "%B %d, %Y %H:%M:%S"

        field = {'format': 'string', 'output': 'string', 'start': startdate, 'end': enddate}
        date = randdate(field)
        date_as_num = time.mktime(time.strptime(date, timefmt))
        self.assertTrue(date_as_num > time.mktime(time.strptime(startdate, timefmt))) 
        self.assertTrue(time.mktime(time.strptime(enddate, timefmt)) > date_as_num) 

    def test_bind_function_exception(self):
        """
        def bind_function(field)
        """
        self.assertRaises(KeyError, bind_function, {'type':'error'})

    def test_bind_function(self):
        """
        def bind_function(field)
        """
        types =['int', 'float', 'string', 'ipsum', 'choice', 'bool', 'name', 'date']
        for t in types:
            self.assertEqual(type(bind_function({'type': t})), type(lambda x: x))

if __name__ == '__main__':
    unittest.main()
