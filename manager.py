from flask import Flask, render_template, url_for
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
from pymongo import MongoClient

# Parse setting
application_id = 'PoSB6H1T3fxmdTEPngtYGaDnaFZsQnvBicUZt5Rc'
rest_api_key = 'q5sYZvNdnAA6S58Dx1qqzVLOgWRJYbOqCBrqSngy'
register(application_id, rest_api_key)

manager = Flask(__name__)
manager.secret_key = 'discoveringfalsksecretkey2016'

class QuestionPersonalStatistics(Object):
    pass
class _User(Object):
    pass

org_info_parse = "Random"

# def getUserQuizHistory(userName):
# 	resultList = []
# 	client = MongoClient('localhost', 27017)
# 	db = client['discovering_user_db']
# 	collection = db[userName]
# 	results = collection.find({"type":"quiz_result"})
# 	for result in results:
# 		resultList.append({'name':result['name'],'accuracy':result['score']})
# 	return resultList

def getQuizHistory(userName):
	# results = QuestionPersonalStatistics.Query.filter(person=userObj).order_by('quizling')
	results = QuestionPersonalStatistics.Query.filter(person=userName);
	print results

user = _User.Query.get(objectId='RGzYAhZZN2')
getQuizHistory(user)

#overall user quiz accuracy

@manager.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html', org=org_info_parse)

@manager.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html', org=org_info_parse)

@manager.route('/testing', methods=['POST'])
def ajaxResponse():
    return str(getUserQuizHistory('test_user_name'))

if __name__ == '__main__':
    manager.run(debug=True)
