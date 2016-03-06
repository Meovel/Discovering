import unittest
from unittest import TestCase
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import searchKeyword

__author__ = 'Hao'


class TestSearch(TestCase):
    def test_search(self):
        keyword = 'test'
        result = searchKeyword(keyword)
        # Pass certain parameters to see if the result matches expectation
        for quiz in result:
            self.assertTrue(keyword in quiz.name.lower())

if __name__ == '__main__':
    unittest.main()