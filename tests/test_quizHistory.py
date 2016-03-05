import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object

# http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from manager import getQuizHistory

# Parse setting
application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)

class _User(Object):
    pass

class TestQuizHistory(TestCase):
    def test_quizHistory(self):
        user = _User.Query.get(objectId='RGzYAhZZN2')
        # Pass certain parameters to see if the result matches expectation
        # self.assertEqual(getQuizHistory(user), [])
        self.assertEqual(getQuizHistory(user), None)


if __name__ == '__main__':
    unittest.main()
