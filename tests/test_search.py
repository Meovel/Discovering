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

    def test_search1(self):
    	#testing search keyword
    	result1 = searchKeyword("red", True)
    	# case1 the quiz name is in search box
    	self.assertTrue("Red bull" in result1)
    	result2 = searchKeyword("info", True)
    	self.assertTrue("The information" in result2)
    	# case1ase2 the part of quiz summary is in search box
    	result3 = searchKeyword("If", True)
    	self.assertFalse("The information" in result3)
    	result4 = searchKeyword("quest", True)
    	self.assertFalse("Derp" in result4)

    def test_search2(self):
    	result1 = searchKeyword("Test", True)
    	# case1 the quiz name is in search box
    	self.assertTrue("Test" in result1)
    	result2 = searchKeyword("Wheel", True)
    	self.assertTrue("Wheel" in result2)
    	# case1ase2 the part of quiz summary is in search box
    	result3 = searchKeyword("Bottle", True)
    	self.assertFalse("Red bull" in result3)
    	result4 = searchKeyword("Zfd", True)
    	self.assertFalse("Zagged" in result4)


if __name__ == '__main__':
    unittest.main()
