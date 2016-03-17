from unittest import TestCase
# Replace the login with the function you want to test
from manager import login

__author__ = 'Chris Riyad'


class TestChart(TestCase):
    def test_chart(self):
        keyword = 'test'
        result = stats()
        # Pass certain parameters to see if the result matches expectation
        self.assertNotEquals("Error", result)

if __name__ == '__main__':
    unittest.main()
