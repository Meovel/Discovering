# from manager import login
import json
import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
import os,sys,inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import *

__author__ = 'Chris Riyad'

application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)

class _User(Object):
    pass

class Quizling(Object):
    pass

class TestChart(TestCase):
    def test_chart1(self):
        ret = stats()
        self.assertFalse(ret == "Error")

    def test_chart2(self):
        ret = stats()
        self.assertFalse(ret == "No_Cookie")

    def test_chart3(self):
        ret = stats()
        self.assertFalse(ret == "no_obj_id")

if __name__ == '__main__':
    unittest.main()
