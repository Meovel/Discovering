import unittest
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
# from manager import organizations

# Parse setting
application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)


class _User(Object):
    pass


class TestOrganizations(unittest.TestCase):
    def test_organizations(self):
    	
    	organizations =  _User.Query.all().filter(type="org")
    	organizationsA = organizations[1]
    	organizationsB = organizations[2]
        # Pass certain parameters to see if the result matches expectation
        self.assertEqual( organizationsA.type, "org" )
        self.assertEqual( organizationsA.username, "Hao" )
       
        

if __name__ == '__main__':
    unittest.main()