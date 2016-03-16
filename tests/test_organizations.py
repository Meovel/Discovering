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
# from manager import organizations

# Parse setting
application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)


class _User(Object):
    pass

class Quizling(Object):
    pass

class TestOrganizations(unittest.TestCase):
    def test_organizations1(self):
    	
    	organizations =  _User.Query.all().filter(type="org")
    	organizationsA = organizations[1]
    	organizationsB = organizations[2]
        # Pass certain parameters to see if the result matches expectation
        self.assertEqual( organizationsA.type, "org" )
        self.assertEqual( organizationsA.username, "Hao" )
       
    def test_organizations2(self):
		# test quiz from specific organization
		quizzes = Quizling.Query.all().filter(ownerName="Bearmonkey")
		quiz5 = quizzes[4]
		quiz1 = quizzes[2]
		quiz2 = quizzes[3]
		self.assertEqual(quiz1.name, "Mathematics")	
		self.assertEqual(quiz2.name, "Science")
		self.assertEqual(quiz5.name, "Weird Animals are Weird")	
		# find the follow organizations
		organizationName = "dtl"
		quizzes = Quizling.Query.all().filter(ownerName = organizationName)
		result = serialize(quizzes)
		self.assertFalse(result.has_key("BibkfMywdy"))
		self.assertFalse(result.has_key("9dpqwKxgze"))
		self.assertFalse(result.has_key("khiIVpFi8C"))
		
		organizationName = "dev10"
		quizzes = Quizling.Query.all().filter(ownerName = organizationName)
		result = serialize(quizzes)
		self.assertFalse(result.has_key("BibkfMywdy"))
		self.assertFalse(result.has_key("9dpqwKxgze"))
		self.assertFalse(result.has_key("khiIVpFi8C"))		
			

if __name__ == '__main__':
    unittest.main()
