import json
import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import quiz
from manager import serialize
from manager import getChannels
# from manager import organizations

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

class TestOrganizations(unittest.TestCase):
    def test_organizations1(self):
    	self.assertTrue(True)

    def test_organizations3(self):
    	self.assertTrue(True)
    	 # get the current user
    	clientId = "tWv8MQspc5"
    	client = _User.Query.get(objectId = clientId)
    	#print client.username

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
		#test getchannel function
		channel_arr = getChannels(True);
		self.assertTrue("channel_RzlZiu7ZA8" in channel_arr)
		self.assertTrue("channel_Fu4XCipsP9" in channel_arr)
		self.assertTrue("channel_6XAT3fA7wR" in channel_arr)
		
		

if __name__ == '__main__':
    unittest.main()

