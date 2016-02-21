from unittest import TestCase
from parse_rest.datatypes import Object
from manager import getQuizHistory


class _User(Object):
    pass


class TestQuizHistory(TestCase):
    def test_quizHostory(self):
        user = _User.Query.get(objectId='RGzYAhZZN2')
        # Pass certain parameters to see if the result matches expectation
        self.assertEqual(getQuizHistory(user), [])
