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
from manager import markMessagesAsRead
from manager import deleteMessages
from manager import handleFollow


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
        self.assertTrue(len(notifications2)-len(notifications1)==0)


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





    #testing mark message as Read

    #testing handle follow as follow


    #testing handle cancellation of follow

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
    # testing delete message
    def test_delete_message(self):
        if self.param is None:
            delete_messages = ["IlKnifE68t", "cXu01KGQQb", "EnxKy0tfBG"]
            read_message = ["pHcSjbJppF", "Jrpna149uv", "I5xelphVko"]
            test_arr = []
            test_arr.append(delete_messages)
            test_arr.append(read_message)
            self.param = test_arr
        delete_messages = self.param[0]
        deleteMessages(True, delete_messages)
        # testing if the deleted message still exist or not
        for i in delete_messages:
            temp_message = Message.Query.all().filter(objectId=i)
            self.assertTrue(len(temp_message)==0)

        
    def test_mark_message_read(self):
        if self.param is None:
            delete_messages = ["IlKnifE68t", "cXu01KGQQb", "EnxKy0tfBG"]
            read_message = ["pHcSjbJppF", "Jrpna149uv", "I5xelphVko"]
            test_arr = []
            test_arr.append(delete_messages)
            test_arr.append(read_message)
            self.param = test_arr
        read_messages = self.param[1]
        markMessagesAsRead(True, read_messages)
        for i in read_messages:
            temp_message = Message.Query.all().filter(objectId=i, read=True)
            self.assertTrue(len(temp_message)>0)


'''
class TestTwo(ParametrizedTestCase):
    # def testing handle follow
    def test_follow(self):
        if self.param is None:
            self.param= ["Test2", "Test"]
        follows = self.param
        handleFollow(follows[0], follows[1], True, "follow")
        following = Following.Query.all().filter(subscriber = follows[0], user = follows[1])
        self.assertTrue(len(following)>0)

    # testing unfollow    
    def test_unfollow(self):
        if self.param is None:
            self.param= ["Test2", "Test"]
        follows = self.param
        handleFollow(follows[0], follows[1], True, "cancel")
        following = Following.Query.all().filter(subscriber = follows[0], user = follows[1])
        self.assertTrue(len(following)==0)
'''

delete_messages = ["IlKnifE68t", "cXu01KGQQb", "EnxKy0tfBG"]
read_message = ["pHcSjbJppF", "Jrpna149uv", "I5xelphVko"]
test_arr = []
test_arr.append(delete_messages)
test_arr.append(read_message)

# testing parameters about follow
#follows = ["Test2", "Test"]
suite = unittest.TestSuite()
suite.addTest(ParametrizedTestCase.parametrize(TestOne, param=test_arr))
#suite.addTest(ParametrizedTestCase.parametrize(TestTwo, param=follows))
unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    unittest.main()
