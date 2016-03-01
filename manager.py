from flask import Flask, render_template, redirect, url_for, request, flash
from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User
from werkzeug.exceptions import HTTPException, NotFound
# import pymongo
# from pymongo import MongoClient
# from bson import json_util

# Parse setting
application_id = '1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD'
rest_api_key = 'SPF588ITDAue5aFwT8XhZRqCph9iqLA2J86hncy5'
register(application_id, rest_api_key)

# Flask setting
manager = Flask(__name__)
manager.secret_key = 'discoveringfalsksecretkey2016'


# Parse classes
class QuestionPersonalStatistics(Object):
    pass


class _User(Object):
    pass


class Quizling(Object):
    pass

org_info_parse = "Random"

Quizzes = Quizling.Query.all().filter()


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
        return redirect(url_for("organizations"))
    return render_template('login.html')


@manager.route('/organizations')
def organizations():

    # get all the organizations
    organizations = _User.Query.all().filter(type="org")

    # render page
    return render_template("organizations.html",
        organizations = organizations,
        organizationsCount = len(organizations))


def getQuizHistory(userName):
    results = QuestionPersonalStatistics.Query.filter(person=userName)
    return


@manager.route('/quizzes/<org_name>')
def quizzes(org_name=None, quiz_list=None):
    if org_name:
        quiz_list = Quizling.Query.filter(ownerName=org_name)
    try:
        return render_template('quizzes.html', quiz_list=quiz_list)
    except HTTPException as e:
        return "error page"


def getMongoQuizHistory(userName):
    stuff = []
    client = MongoClient('localhost',27017)
    db = client['discovering_user_db']
    collection = db['test_user_name']
    results = collection.find({'type':'quiz_result'}).sort([('time', pymongo.DESCENDING)])
    for result in results:
        stuff.append(json_util.dumps(result,default=json_util.default))
    return str({'result':stuff})


@manager.route('/stats', methods=['GET', 'POST'])
def stats():
    return render_template('stats.html', org=org_info_parse)


@manager.route('/search')
def search():
    keyword = request.query_string[6:]
    quiz_list = searchKeyword(keyword)
    return quizzes(quiz_list=quiz_list)


def searchKeyword(keyword):
    result = set()
    for quiz in Quizzes:
        if quiz.name:
            if keyword in quiz.name:
                result.add(quiz)
        else:
            if quiz.summary:
                if keyword in quiz.summary:
                    result.add(quiz)
    return result


@manager.route('/testing', methods=['POST'])
def ajaxResponse():
    return getMongoQuizHistory('test_user_name')

if __name__ == '__main__':
    manager.run(debug=True)
