import json
import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from manager import quizzes
from manager import serialize
from manager import getChannels
from manager import fetch_timeline_data
from manager import compute_achievements
import datetime

__author__ = 'Chris Riyad'
# from manager import organizations

"""
Parse-specific API keys.
"""
application_id = '1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD'
rest_api_key = 'SPF588ITDAue5aFwT8XhZRqCph9iqLA2J86hncy5'
register(application_id, rest_api_key)

"""
Begin Parse-specific class-declarations
(needed to retrieve the related objects from Parse).
"""
class Achievement(Object):
    pass

class AchievementPersonalStatistics(Object):
    pass

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
"""
End Parse-specific class-declarations
"""

"""
Where we learnt about parameterized testing in Python:
http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
"""
class ParameterizedTestTimeline(TestCase):
    def __init__(self, methodName='runTest', objId=None):
        super(ParameterizedTestTimeline, self).__init__(methodName)
        self.objId = objId

    # This method is straight from: # http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
    @staticmethod
    def parametrize(testcase_klass, objId=None):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'objId'.
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_klass(name, objId=objId))
        return suite

# Tests if no empty entries were put into the date for Timeline.
class TestOne(ParameterizedTestTimeline):
    # tests if data returned from fetch_timeline_data is not none.
    def test_timeline_no_empty1(self):
        timeline_data = fetch_timeline_data(self.objId)
        self.assertIsNotNone(timeline_data)

    # NOTE: This test is no longer needed, since this variable was unnecessary.
    # We're leaving the test here, in case we decided to use this again at some later point.
    # @author chris and riyad
    # tests specifically that the date is correctly parsed as a long (converted from int by python) in timeline_data
    # def test_timeline_date_parsed_as_long(self):
    #     timeline_data = fetch_timeline_data(self.objId)
    #     for data in timeline_data:
    #         self.assertTrue(type(data[4]) is long)

    # tests first dimension of timeline_data list
    def test_timeline_no_empty2(self):
        # Pass certain parameters to see if the result matches expectation
        timeline_data = fetch_timeline_data(self.objId)
        for data in timeline_data:
            self.assertFalse(data is None)

    # tests to make sure date is a datetime.datetime object
    def test_timeline_correct_date_type(self):
        timeline_data = fetch_timeline_data(self.objId)
        for data in timeline_data:
            # self.assertTrue(type(data[3]) is datetime.datetime)
            self.assertTrue(type(data[3]) is unicode)

# Tests if the quiz affiliated with the question data actually exists in the database.
class TestTwo(ParameterizedTestTimeline):
    def test_no_quizless_questions(self):
        question_obj = QuestionPersonalStatistics.Query.all().filter().limit(17000)
        timeline_data = fetch_timeline_data(self.objId)
        for i in range(0,len(timeline_data)):
            for j in range(5, len(timeline_data[i])):
                quest_id = timeline_data[i][j][0]
                quiz_id = timeline_data[i][1]
                quizling_obj = Quizling.Query.all().filter(objectId=quiz_id)
                self.assertFalse(quizling_obj is None)

class TestThree(ParameterizedTestTimeline):
    # asserts first list exists in double-nested list
    def test_achievement_proper_format1(self):
        achieve_data = compute_achievements(self.objId)
        if(achieve_data): # if not falsy, make sure this is an array
            self.assertTrue(achieve_data[0])

    # aserts second list exists in double-nested list
    def test_achievement_proper_format2(self):
        achieve_data = compute_achievements(self.objId)
        if(achieve_data[0]):
            # if not falsy, assert is an array with non-empty first elem
            self.assertTrue(achieve_data[0][0])

    def test_achievement_proper_format3(self):
        achieve_data = compute_achievements(self.objId)
        if(achieve_data[0]):
            # if not falsy, assert is an array with non-empty second elem
            self.assertTrue(achieve_data[0][1])


objectId1 = "WrWZRnIDbv"
# mostly from http://eli.thegreenplace.net/2011/08/02/python-unit-testing-parametrized-test-cases
suite = unittest.TestSuite()
suite.addTest(ParameterizedTestTimeline.parametrize(TestOne, objId=objectId1))
suite.addTest(ParameterizedTestTimeline.parametrize(TestTwo, objId=objectId1))
suite.addTest(ParameterizedTestTimeline.parametrize(TestThree, objId=objectId1))
unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
