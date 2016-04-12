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
from manager import quizzes
from manager import serialize
from manager import getChannels
from manager import userDashBoard
from manager import postComment
import pytest
import mock


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


class Comment(Object):
    pass

class TestOrganizations(unittest.TestCase):

    def test_organizations1(self):
    	self.assertTrue(True)

    def test_organizations3(self):
    	self.assertTrue(True)
    	 # get the current user
    	clientId = "tWv8MQspc5"
    	client = _User.Query.get(objectId = clientId)
    	#print client.username

    def parameter_test():
        @pytest.mark.parametrize("test_input,expected", [
        ("3+1", 4),
        ("2+3", 5),
        ("6*9", 42),
         ])
        def test_eval(test_input, expected):
            assert eval(test_input) == expected

    def test_organizations2(self):
		# test quiz from specific organization
		quizzes = Quizling.Query.all().filter(ownerName="dev10")
		print len(quizzes)
		name_arr = []
		for i in quizzes:
			name_arr.append(i.name)
		self.assertTrue(any("Test" in s for s in name_arr))
		self.assertTrue(any("Ct!ktvovylo" in s for s in name_arr))
		self.assertTrue(any("Derp" in s for s in name_arr))	
		# find the follow organizations
		quizzes = Quizling.Query.all().filter(ownerName = "dev10")
		result = serialize(quizzes)
		self.assertFalse(result.has_key("BibkfMywdy"))
		self.assertFalse(result.has_key("9dpqwKxgze"))
		self.assertFalse(result.has_key("khiIVpFi8C"))
		#test serialize function
		organizationName = "dev10"
		quizzes = Quizling.Query.all().filter(ownerName = organizationName)
		result = serialize(quizzes)
		self.assertTrue(result.has_key("idgtXmekx4"))
		self.assertTrue(result.has_key("Y6I9zDbZHw"))
		self.assertTrue(result.has_key("CiXSGRo3eI"))

		'''
		channel_arr = getChannels();
		self.assertTrue("channel_RzlZiu7ZA8" in channel_arr)
		self.assertTrue("channel_Fu4XCipsP9" in channel_arr)
		self.assertTrue("channel_6XAT3fA7wR" in channel_arr)
		'''

		#testing comment staff
		self.assertTrue(True)
		user_id = "123"
		#retrieve all comments relate to a specific user
		comment_arr= userDashBoard(user_id, True)
		self.assertEqual(len(comment_arr),5)
		self.assertTrue("guoqiao" in comment_arr)
		self.assertEqual(comment_arr.count("guoqiao"), 4)
		self.assertTrue("123" in comment_arr)
		# count the occurences of comment
		self.assertEqual(comment_arr.count("123"), 1)
		self.assertTrue("haotian" not in comment_arr)
		self.assertTrue("zhao jin" not in comment_arr)
		# testing comment staff2
		user_id = "RzlZiu7ZA8"
		comment_arr = userDashBoard(user_id, True)
		self.assertEqual(len(comment_arr), 2)
		self.assertEqual(comment_arr.count("guoqiao"),2)


		#testing posting comment
		comment_num1 = len(Comment.Query.all())
		postComment(True, "test123", "cs428 meeting", "haotian" )
		comment_num2 = len(Comment.Query.all())
		self.assertEqual(comment_num2-comment_num1,1)
		postComment(True, "test123", "coding challenge", "robben")
		comments = Comment.Query.all()
		posters = []
		for temp_comment in comments:
			posters.append(temp_comment.poster)
		self.assertTrue("haotian" in posters)
		self.assertTrue("robben" in posters)
		self.assertFalse("zhanghao" in posters)

		#parametrize test
  		

if __name__ == '__main__':
    unittest.main()

