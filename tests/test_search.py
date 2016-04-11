import json
import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import searchKeyword
from manager import share
from manager import sendMessage
import pytest


__author__ = 'Hao'

# Parse setting
application_id = '1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD'
rest_api_key = 'SPF588ITDAue5aFwT8XhZRqCph9iqLA2J86hncy5'
register(application_id, rest_api_key)

class _User(Object):
    pass

class Quizling(Object):
    pass

class LearningAreas(Object):
    pass


class LearningStage(Object):
    pass


class Following(Object):
    pass

class Channel(Object):
    pass

class Notification(Object):
    pass

class Message(Object):
    pass

class TestSearch(TestCase):
    def test_search(self):
        keyword = 'test'
        result = searchKeyword(keyword)
        # Pass certain parameters to see if the result matches expectation
        for quiz in result:
            self.assertTrue(keyword in quiz.name.lower())
    '''
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
    '''
    def test_share(self):
        test = _User.Query.get(username="test")
        followers = Following.Query.filter(user=test)
        print "%d people follow test" %len(followers)

        notifications1 = Notification.Query.filter(fromUser="test")
        print "before insert number of notification sent from %s is %d." % ("test",len(notifications1))
        share(True,"test", "haotian", "1234")
        # test if the request 
        notifications2 = Notification.Query.filter(fromUser="test")
        print "after insert number of notification sent from %s is %d." % ("test",len(notifications2))
        self.assertTrue(len(notifications2)-len(notifications1)==4)


        # second test case on chris
        chris = _User.Query.get(username="Chris")
        followers = Following.Query.filter(user=chris)
        print "%d people follow chris" %len(followers)

        chris1 = Notification.Query.filter(fromUser="Chris")
        print "before insert number of notification sent from %s is %d." % ("Chris",len(chris1))
        share(True, "Chris", "guoqiao", "123")
        # after the share of notifications
        chris2 = Notification.Query.filter(fromUser="Chris")
        print "after insert number of notification sent from %s is %d." % ("Chris",len(chris2))


        self.assertTrue(len(chris1)==len(chris2))
        # thrid test case on 
        test2 = _User.Query.get(username="Test2")
        followers = Following.Query.filter(user=test2)
        print "%d people follow Test2" %len(followers)

        test2 = Notification.Query.filter(fromUser="Test2")
        print "before insert number of notification sent from %s is %d." % ("Test2",len(test2))
        share(True, "Test2", "guoqiao", "123")
        # after the share of notifications
        test2_ = Notification.Query.filter(fromUser="Test2")
        print "after insert number of notification sent from %s is %d." % ("Test2",len(test2_))
        self.assertTrue(len(test2)==len(test2_))


    def test_message(self):
        sendMessage(True, "haotian", "guoqiao", "meeting tonight")
        messages = Message.Query.filter(fromUser="haotian")
        print "number of messages contain haotian is %d" % len(messages)
        self.assertTrue(len(messages)>=1)
        messages = Message.Query.filter(fromUser="guoqiao")
        self.assertTrue(len(messages)==0)
        sendMessage(True, "hao", "haotian", "testing requirement")
        messages = Message.Query.filter(toUser="haotian")
        self.assertTrue(len(messages)>=1)

    def parameter_test():
        @pytest.mark.parametrize("test_input,expected", [
        ("3+5", 8),
        ("2+4", 6),
        ("6*9", 42),
         ])
        def test_eval(test_input, expected):
            assert eval(test_input) == expected

if __name__ == '__main__':
    unittest.main()
