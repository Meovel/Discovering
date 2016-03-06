import flask
import unittest
import tempfile
from unittest import TestCase
from parse_rest.connection import register
from parse_rest.datatypes import Object
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
from werkzeug.exceptions import HTTPException, NotFound

# http://stackoverflow.com/questions/714063/python-importing-modules-from-parent-folder
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

# from manager import organizations
from manager import follow

# Parse setting
application_id = '1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD'
rest_api_key = 'SPF588ITDAue5aFwT8XhZRqCph9iqLA2J86hncy5'
register(application_id, rest_api_key)

# Flask setting
manager = Flask(__name__)


class _User(Object):
    pass

class Following(Object):
    pass

class TestFollow(unittest.TestCase):
    def test_Follow(self):
    #manually create a follow relationship and check if it appears in "following" table in database
        #organizationId = "Ef8XPm3Atd"
        subscriberId = "gm10kUBxnM"
        org = "info@quizlingapp.com"
        organization = _User.Query.get(email = org)
        subscriber = _User.Query.get(objectId = subscriberId)


        #test for follow
        following = Following()
        following.subscriber = subscriber
        following.user = organization
        
        following.save()
        a = Following.Query.get(subscriber = subscriber, user = organization)
        self.assertTrue(a)

        #test for cancel relationship
        following = Following.Query.get(subscriber = subscriber, user = organization)
        following.delete()
#b = Following.Query.get(subscriber = subscriber, user = organization)
#self.assertFalse(Following.Query.get(subscriber = subscriber, user = organization))

#Cannot be tested, since Following.Query.get(subscriber = subscriber, user = organization) will just return error[QueryResourceDoesNotExist]

#one more testcase
    def test_Follow2(self):
        subscriberId = "aRg3aCKL4x"
        org = "YW99fRF1fx"
        organization = _User.Query.get(objectId = org)
        subscriber = _User.Query.get(objectId = subscriberId)
        
        
        #test for follow
        following = Following()
        following.subscriber = subscriber
        following.user = organization
        
        following.save()
        a = Following.Query.get(subscriber = subscriber, user = organization)
        self.assertTrue(a)
        
        #test for cancel relationship
        following = Following.Query.get(subscriber = subscriber, user = organization)
        following.delete()
#Cannot be tested, since Following.Query.get(subscriber = subscriber, user = organization) will just return error[QueryResourceDoesNotExist]



if __name__ == '__main__':
    unittest.main()