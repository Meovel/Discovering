from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, make_response, session
from parse_rest.connection import register, SessionToken
from parse_rest.datatypes import Object
from parse_rest.user import User
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.datastructures import ImmutableMultiDict
import json
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

org_info_parse = "Random"

Quizzes = Quizling.Query.all().filter().limit(300)
for q in Quizzes:
    if not hasattr(q, 'averageScore'):
        q.averageScore = 0
    if not hasattr(q, 'playCount'):
        q.playCount = 0
kw = ''
result = []
filteredResult = []





@manager.route('/', methods=['GET', 'POST'])
def login():
    print 'cookie in homepage: '
    print request.cookies
    if request.method == 'POST':
        data = request.form

        try:
            user = User.login(data['username'], data['password'])
        except:
            flash('Incorrect username or password', 'info')
        # login_user(user)
    #     return redirect(url_for("index"))
    # return render_template('login.html')


        resp = make_response(render_template('organizations/organizations.html'))

        username = data.getlist('username')[0]
        user_obj_query = _User.Query.all().filter(username = username)
        print user_obj_query
        for obj in user_obj_query:
            print obj
        user_id = ""
        print len(user_obj_query)
        if len(user_obj_query) > 0:
            user_objectId = (user_obj_query[0]).objectId
            resp.set_cookie('user_objectId', user_objectId)

        resp.set_cookie('username', username)

        return resp


    return make_response(render_template('login.html'))


############################### Index ###############################
'''
    1. show recommanded quizzes
        a. find the follow organizations
        b. find the quizzes of the organizations
        c. find top 3 category of quizzes
        d. recommanded from the top 3 category
    2. show channels
        a. render channels
        b. show quizzes of organzations when organizations clicked
'''

@manager.route('/index')
def index():
    print "================ Index ================"

    # return variables
    categories = []
    retQuizzes = []


    # get the current user
    clientId = "tWv8MQspc5"
    client = _User.Query.get(objectId = clientId)

    '''
    ----------------------------
        recommanded quizzes
    ----------------------------
    '''
    # find the follow organizations
    follows = Following.Query.all().filter(subscriber = client)
    print "follow length: " + str(len(follows))

    followedOrgs = []
    for follow in follows:
        followedOrgs.append(follow.user)


    # get the quiz category dictionary
    quizzesCount = quizzesOfFollowedOrgs(followedOrgs)
    # quizzesCount = dict()

    count = 0
    for categoryId in sorted(quizzesCount, key=quizzesCount.get, reverse=True):
        if count == 3:
            break

        category = LearningAreas.Query.get(objectId = categoryId)

        # add to categories
        categories.append(category.name)

        # find the quizzes of this category
        quizzesTemp = Quizling.Query.all().filter(area = category).limit(8)
        retQuizzes.append(quizzesTemp)

        count += 1


    '''
    ----------------------------
        channels
    ----------------------------
    '''
    channels = getChannels()
    # for channel in channels:
    #     print channel

    print "========================================"

    return render_template("index.html",
        categories = categories,
        quizzes = retQuizzes,
        lengthOne = len(retQuizzes[0]),
        lengthTwo = len(retQuizzes[1]),
        lengthThree = len(retQuizzes[2]),
        channels = channels)



def quizzesOfFollowedOrgs(followedOrgs):
    quizzesCount = dict()

    count = 0
    for org in followedOrgs:
        quizzes = Quizling.Query.all().filter(ownerName = org.username)

        if(len(quizzes) != 0):
            count += 1

        if count == 5:
            break

        for quiz in quizzes:
            if hasattr(quiz, "area"):
                if quiz.area.name not in quizzesCount:
                    quizzesCount[quiz.area.objectId] = 1
                else:
                    quizzesCount[quiz.area.objectId] += 1

    return quizzesCount



def getChannels():
    superOrgs = []

    for channel in Channel.Query.all():
        if hasattr(channel, 'user'):
            if channel.user is not None:
                print channel.channelName
                superOrgs.append(channel.user)

    return superOrgs

############################### End of Index ###############################

############################### Dashboard ###############################

@manager.route('/organizations')
def organizations():

    print 'cookie in organizations: '
    print request.cookies

    # get all the organizations
    organizations = _User.Query.all().filter(type="org")

    # render page
    return render_template("organizations/organizations.html",
        organizations = organizations)

@manager.route('/quiz/<organizationName>')
def quiz(organizationName = None):
    quizzes = Quizling.Query.all().filter(ownerName = organizationName)
    print "============="

    if(len(quizzes) == 0):
        return jsonify(result = None)
    else:
        return jsonify(result = serialize(quizzes))

@manager.route("/follow/<organizationId>")
def follow(organizationId = None):
    print("=======================")

    organizationId = organizationId
    subscriberId = "seGQaKSk1O"
    #find subscriber and organization
    organization = _User.Query.get(objectId = organizationId)
    subscriber = _User.Query.get(objectId = subscriberId)

    type = request.args.get('type', 0, type=str)

    # save the follow relation
    if type == "follow":
        following = Following()
        following.subscriber = subscriber
        following.user = organization

        following.save()

    # cancel follow relation
    elif type == "cancel":
        following = Following.Query.get(subscriber = subscriber, user = organization)
        following.delete()

    return jsonify(result = "success")


# serialize ParseObject so that it can be jsonify
def serialize(quizzes):
    ret = dict()

    for quiz in quizzes:
        temp = dict()
        temp["ownerName"] = quiz.ownerName
        temp["name"] = quiz.name
        temp["summary"] = quiz.summary

        ret[quiz.objectId] = temp

    return ret


############################### End Of Dashboard ###############################


def getQuizHistory(userName):
    results = QuestionPersonalStatistics.Query.filter(person=userName)
    print results
    return


@manager.route('/quizzes/<org_name>')
def quizzes(org_name=None, user_list=None, quiz_list=None, keyword=None):
    if org_name:
        quiz_list = Quizling.Query.filter(ownerName=org_name)
    try:
        return render_template('quizzes.html', user_list=user_list, quiz_list=quiz_list, keyword=keyword)
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


    print 'cookie in stats: '
    print request.cookies

    user = request.cookies.get('username')

    if user is None:
        print "Error: user returned None"
        # return "No_Cookie"
        # exit()

    user_obj = _User.Query.all().filter().limit(300)
    if user_obj is None:
        print "Error: user_obj returned None"
        # return "Error"
        # exit()
    print len(user_obj)
    obj_id = ''
    for obj in user_obj:
        # print obj.username
        if obj.username == user:
            obj_id = obj.objectId

    print obj_id
    if obj_id == '':
        print "Error: obj_id returned None"
        # return "no_obj_id"
        # exit()

    return render_template('stats.html', org=org_info_parse, objectId = obj_id)

@manager.route('/timeline', methods=['GET', 'POST'])
def timeline():

    user = request.cookies.get('username')

    if user is None:
        print "Error: user returned None"
        # return "No_Cookie"
        # exit()

    user_obj = _User.Query.all().filter().limit(300)
    if user_obj is None:
        print "Error: user_obj returned None"
        # return "Error"
        # exit()
    print len(user_obj)
    obj_id = ''
    for obj in user_obj:
        # print obj.username
        if obj.username == user:
            obj_id = obj.objectId

    print obj_id
    if obj_id == '':
        print "Error: obj_id returned None"
        # return "no_obj_id"
        # exit()

    relevant_data = []

    quiz_obj = QuizPersonalStatistics.Query.all().filter().limit(900)
    question_obj = QuestionPersonalStatistics.Query.all().filter().limit(17000)


    for quiz in quiz_obj:
        if quiz.user.objectId == obj_id:
            relevant_data.append(quiz.quizling.objectId)
            relevant_data.append(quiz.averageScore)
            print "quizling: " + str(quiz.quizling.objectId) + " created: " + str(quiz.createdAt) + " updated: " + str(quiz.updatedAt)
    relevant_data = {}
    relevant_data['hello'] = 'wassup'
    relevant_data['arab'] = 'spring'
    # relevant_data_json = json.dumps(relevant_data)
    # print relevant_data_json
    return render_template('timeline.html', org=org_info_parse, relevant_data=relevant_data, objectId = obj_id)


@manager.route('/search')
def search():
    keyword = request.query_string[6:]
    quiz_list = searchKeyword(keyword)
    users = _User.Query.filter(username=keyword)
    return quizzes(user_list=users, quiz_list=quiz_list, keyword=keyword)



def searchKeyword(keyword):
    global kw
    global result
    kw = keyword
    result = []
    keyword = keyword.lower()
    for quiz in Quizzes:
        if quiz.name:
            if keyword in quiz.name.lower():
                result.append(quiz)
        else:
            if quiz.summary:
                if keyword in quiz.summary.lower():
                    result.append(quiz)
    return result


@manager.route('/filterArea', methods=['POST'])
def filterArea():
    areaName = request.form.keys()[0]
    global kw
    global result
    global filteredResult
    area = LearningAreas.Query.get(objectId=areaName)
    filteredResult = []
    for quiz in result:
        if hasattr(quiz, 'area'):
            if quiz.area.objectId == area.objectId:
                filteredResult.append(quiz)
    return makeJSONquizzes(filteredResult)


@manager.route('/filterAge', methods=['POST'])
def filterAge():
    ageId = request.form.keys()[0]
    global kw
    global result
    age = LearningStage.Query.get(objectId=ageId)
    filteredResult = []
    for quiz in result:
        if hasattr(quiz, 'stage'):
            if quiz.stage.objectId == age.objectId:
                filteredResult.append(quiz)
    return makeJSONquizzes(filteredResult)


def makeJSONquizzes(quizzes):
    response = dict()
    data = []
    index = 0
    for quiz in quizzes:
        qjson = dict()
        qjson['id'] = quiz.objectId
        qjson['name'] = quiz.name
        qjson['owner'] = quiz.ownerName
        if hasattr(quiz, 'quizType'):
            qjson['quizType'] = quiz.quizType
        else:
            qjson['quizType'] = -1
        qjson['summary'] = quiz.summary
        if hasattr(quiz, 'questionCount'):
            qjson['questionCount'] = quiz.questionCount
        else:
            qjson['questionCount'] = 0
        qjson['avgScore'] = quiz.averageScore
        data.append(qjson)
    response['data'] = data
    return json.dumps(response)


@manager.route('/sortQuizzes', methods=['POST'])
def sort():
    global result
    global filteredResult
    if not filteredResult:
        filteredResult = result

    attr = request.form.keys()[0]
    if attr == 'name':
        filteredResult.sort(key=lambda x: x.name, reverse=True)
    if attr == 'updatedAt':
        filteredResult.sort(key=lambda x: x.updatedAt, reverse=True)
    if attr == 'averageScore':
        filteredResult.sort(key=lambda x: x.averageScore, reverse=True)
    if attr == 'playCount':
        filteredResult.sort(key=lambda x: x.playCount, reverse=True)

    return makeJSONquizzes(filteredResult)


if __name__ == '__main__':
    manager.run(debug=True)
