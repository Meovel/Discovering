from flask import Flask, render_template, url_for
from pymongo import MongoClient

manager = Flask(__name__)

org_info_parse = "Random"

def getUserQuizHistory(userName):
	resultList = []
	client = MongoClient('localhost', 27017)
	db = client['discovering_user_db']
	collection = db[userName]
	results = collection.find({"type":"quiz_result"})
	for result in results:
		resultList.append({'name':result['name'],'accuracy':result['score']})
	return resultList

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
