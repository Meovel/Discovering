from flask import Flask, render_template, redirect, url_for, request, flash
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
from pymongo import MongoClient
import pymongo
from bson import json_util
# from flask.ext.login import login_user, login_required, logout_user, current_user

# Parse setting
application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)

# Flask setting
manager = Flask(__name__)
# manager.secret_key = 'discoveringfalsksecretkey2016'


# Parse classes
class QuestionPersonalStatistics(Object):
    pass


class _User(Object):
    pass

org_info_parse = "Random"


def getQuizHistory(userName):
    results = QuestionPersonalStatistics.Query.filter(person=userName)
    return

def getMongoQuizHistory(userName):
	stuff = []
	client = MongoClient('localhost',27017)
	db = client['discovering_user_db']
	collection = db['test_user_name']
	results = collection.find({'type':'quiz_result'}).sort([('time', pymongo.DESCENDING)])
	for result in results:
		stuff.append(json_util.dumps(result,default=json_util.default))
	return str({'result':stuff})


@manager.route('/', methods=['GET', 'POST'])
def login():
    user = None
    if request.method == 'POST':
        data = request.form
        try:
            user = User.login(data['username'], data['password'])
        except:
            flash('Incorrect username or password', 'info')
        # login_user(user)
        return redirect(url_for(""))
    return render_template('login.html')


@manager.route('/stats', methods=['GET', 'POST'])
def stats():
    return render_template('stats.html', org=org_info_parse)


@manager.route('/testing', methods=['POST'])
def ajaxResponse():
    return getMongoQuizHistory('test_user_name')

if __name__ == '__main__':
    manager.run(debug=True)
