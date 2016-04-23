import json
import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import quiz_inforamtion
from manager import serialize
from manager import getChannels
from manager import like
from manager import unlike
from manager import userDashBoard
# from manager import organizations

# Parse setting
application_id = '1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD'
rest_api_key = 'SPF588ITDAue5aFwT8XhZRqCph9iqLA2J86hncy5'
register(application_id, rest_api_key)



# Parse classes
class QuestionPersonalStatistics(Object):
    pass

class QuizPersonalStatistics(Object):
    pass

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


class Comment(Object):
    pass

class Like(Object):
    pass


class Notification(Object):
    pass

class Message(Object):
    pass

class QuizPersonalStatistics(Object):
    pass

class RecentlyVisited(Object):
    pass


''' comment out previous code
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
'''

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', param=None):
        super(ParametrizedTestCase, self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_klass, param=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, param=param))
        return suite


class TestOne(ParametrizedTestCase):
    def test_quiz_information1(self):
    	object_id = self.param
    	print object_id
    	names = quiz_inforamtion(object_id, True)
    	self.assertIsNotNone(names)
    	self.assertTrue(len(names)>=1)


 	def test_quiz_information2(self):
 		object_id = self.param
    	print object_id
    	names = quiz_inforamtion(object_id, True)
    	self.assertTrue("dev10" in names)

   	def test_quiz_information3(self):
   		object_id = self.param
    	print object_id
    	names = quiz_inforamtion(object_id, True)
    	self.assertTrue("dev9" not in names)



class TestTwo(ParametrizedTestCase):
	# testing on a existing one
    def test_user_DashBoard1(self):
    	if self.param is None:
    		self.param = ["RzlZiu7ZA8", "qGU7Nd47kl"]
    	print self.param[0]
    	organization = _User.Query.get(objectId = self.param[0])
    	prev_count = RecentlyVisited.Query.all().filter(target=organization).order_by("-visitCount").limit(1)
    	if len(prev_count)==0:
    		prev_count = 0
    	else:
    		prev_count = prev_count[0].visitCount
    	userDashBoard(self.param[0], True, self.param[1])
    	after_count= RecentlyVisited.Query.all().filter(target=organization).order_by("-visitCount").limit(1)
    	after_count = after_count[0].visitCount
    	# check if the target organization visit increase by 1 or not
    	if prev_count==0:
    		self.assertTrue(after_count==1)
    	else:
    		self.assertTrue(after_count-prev_count==1)
    '''
    # testing on a new one
 	def test_user_DashBoard2(self):
 		if self.param is None:
 			self.param = ["RzlZiu7ZA8", "qGU7Nd47kl"]
 		organization = _User.Query.get(objectId = self.param[0])
    	prev_count = RecentlyVisited.Query.all().filter(target=organization).order_by("-visitCount").limit(1)
    	if len(prev_count)==0:
    		prev_count = 0
    	else:
    		prev_count = prev_count[0].visitCount
    	userDashBoard(self.param[1], True, self.param[0])
    	after_count= RecentlyVisited.Query.all().filter(target=organization).order_by("-visitCount").limit(1)
    	after_count = after_count[0].visitCount
    	# check if the target organization visit increase by 1 or not
    	if prev_count==0:
    		self.assertTrue(after_count==0)
    	else:
    		self.assertTrue(after_count==prev_count)
   	'''


quiz_id = "CiXSGRo3eI"
# user id and organizaiton id
visit0 = ["RzlZiu7ZA8", "qGU7Nd47kl"]
visit1 = ["RzlZiu7ZA8", "WrWZRnIDbv"]
suite = unittest.TestSuite()
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=quiz_id))
suite.addTest(ParametrizedTestCase.parametrize(TestTwo, param=visit0))
suite.addTest(ParametrizedTestCase.parametrize(TestTwo, param=visit1))
unittest.TextTestRunner(verbosity=3).run(suite)




if __name__ == '__main__':
    unittest.main()

