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

import string


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


class Comment(Object):
    pass

class Like(Object):
    pass


class Notification(Object):
    pass

class Message(Object):
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
notifications = []
following = []
follower = []
messages = []
user = None




@manager.route('/', methods=['GET', 'POST'])
def login():
    global user, notifications, messages
    print 'cookie in homepage: '
    print request.cookies
    if request.method == 'POST':
        data = request.form

        try:
            user = User.login(data['username'], data['password'])
        except:
            user = None
            flash('Incorrect username or password', 'info')
        # login_user(user)

        if user:
            username = data.getlist('username')[0]

            notifications = Notification.Query.filter(to=username)
            messages = Message.Query.filter(toUser=username)
            resp = make_response(render_template('organizations/organizations.html', notifications=notifications, messages=messages))
            following_query = Following.Query.filter(subscriber=user)
            for u in following_query:
                following.append(u.user)
            follower_query = Following.Query.filter(user=user)
            for u in follower_query:
                follower.append(u.subscriber)
            resp.set_cookie('username', username)

            resp.set_cookie('user_objectId', user.objectId)

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
    global notifications, messages
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
        channels = channels,
        notifications=notifications,
        messages=messages)



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


############################### User Dashboard ###############################
@manager.route('/user/<target_id>')
def userDashBoard(target_id = None):
    '''
        This page required organization basic information, follower, followed, 
        quizzes(if have any) and comment
    '''
    user_id = "hfy96QWaXg"

    comments = Comment.Query.all().filter(user = target_id)
    organization = _User.Query.get(objectId = target_id)  
    followings = Following.Query.all().filter(user = organization).limit(12)
    followers = []
    for following in followings:
        if hasattr(following.subscriber, "username"):
            followers.append(following.subscriber)
    quizzes = getQuiz(organization.username)

    #like
    like = ""
    like = Like.Query.all().filter(liker=user_id).filter(likee=target_id)
    if len(like) == 0:
        like = "unlike"
    else:
        like = "like"
    numOfLikes = len(Like.Query.all().filter(likee=target_id))

    # get related organizations
    relatedOrgs, relatedOrgsArea = getRelatedOrgs(quizzes, organization.username)


    return render_template("dashboard.html",
        comments = comments,
        numOfComments = len(comments),
        username = "guoqiao",
        target_id = target_id,
        organization = organization,
        followers = followers,
        numOfFollowers = len(followers),
        quizzes = quizzes,
        relatedOrgs = relatedOrgs,
        relatedOrgsArea = relatedOrgsArea,
        like = like,
        numOfLikes = numOfLikes)

def getRelatedOrgs(quizzes, organizationName):
    areas = []
    areasName = []
    relatedOrgs = []
    relatedOrgsName = []
    relatedOrgsArea = []

    count = 0
    if quizzes is not None:
        for quiz in quizzes:
            if count == 20:
                break
            if hasattr(quiz, "area"):
                if quiz.area.name not in areasName:
                    areas.append(quiz.area)
                    areasName.append(quiz.area.name)
            count += 1


        for area in areas:
            representativeQuizzes = Quizling.Query.all().filter(area = area).limit(10)
            for quiz in representativeQuizzes:
                relatedOrg = _User.Query.get(username = quiz.ownerName)
                if relatedOrg.username not in relatedOrgsName and relatedOrg.username != organizationName:
                    relatedOrgs.append(relatedOrg)
                    relatedOrgsName.append(relatedOrg.username)
                    relatedOrgsArea.append(quiz.area.name)

    return relatedOrgs,relatedOrgsArea


@manager.route('/comment/<target_id>')
def postComment(target_id = None):
    content = request.args.get('content', 0, type = str)
    poster = request.args.get('poster', 0, type = str)

    # create comment and save
    comment = Comment()
    comment.content = content
    comment.poster = poster
    comment.user = target_id
    comment.save()

    return jsonify(result = "OK")


@manager.route('/like/<target_id>')
def like(target_id = None):
    user_id = "hfy96QWaXg"

    newLike = Like()
    newLike.liker = user_id
    newLike.likee = target_id
    newLike.save()
    return jsonify(result="OK")

@manager.route('/unlike/<target_id>')
def unlike(target_id = None):
    user_id = "hfy96QWaXg"

    like = Like.Query.get(liker = user_id, likee = target_id)
    like.delete()

    return jsonify(result="OK")


############################### End Of User Dashboard ###############################



############################### Dashboard ###############################

@manager.route('/organizations')
def organizations():
    global notifications, messages

    print 'cookie in organizations: '
    print request.cookies

    # get all the organizations
    organizations = _User.Query.all().filter(type="org")

    # render page
    return render_template("organizations/organizations.html",
        organizations = organizations, notifications=notifications, messages=messages)

def getQuiz(organizationName):
    quizzes = Quizling.Query.all().filter(ownerName = organizationName)
    
    return quizzes;

@manager.route("/follow/<organizationId>")
def handleFollow(organizationId = None):
    print("=======================")

    organizationId = organizationId
    subscriberId = "seGQaKSk1O"
    #find subscriber and organization
    organization = _User.Query.get(objectId = organizationId)
    subscriber = _User.Query.get(objectId = subscriberId)

    type = request.args.get('type', 0, type=str)
    print type

    # save the follow relation
    if type == "follow":
        following = Following()
        following.subscriber = subscriber
        following.user = organization

        following.save()

    # cancel follow relation
    elif type == "cancel":
        following = Following.Query.filter(subscriber = subscriber, user = organization)
        for follow in following:
            follow.delete()

    return jsonify(result = "success")


@manager.route("/deleteFollower/<userId>")
def follow(userId = None):
    global user
    follower = _User.Query.get(objectId=userId)
    if follower:
        relations = Following.Query.filter(subscriber=follower, user=user)
        for r in relations:
            r.delete()
    return "success"


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
    global notifications, messages
    if org_name:
        quiz_list = Quizling.Query.filter(ownerName=org_name)
    try:
        return render_template('quizzes.html',
                user_list=user_list, quiz_list=quiz_list, keyword=keyword,
                notifications=notifications, messages=messages)
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
    global notifications, messages

    print 'cookie in stats: '
    print request.cookies

    user = request.cookies.get('username')
    # print "stats user: "
    # print user
    user_obj = _User.Query.all().filter().limit(300)
    if user_obj is None:
        print "Error: user_obj returned None"
        return "Error"
        exit()
    print len(user_obj)
    obj_id = ''
    for obj in user_obj:
        # print obj.username
        if obj.username == user:
            obj_id = obj.objectId

    print obj_id

    return render_template('stats.html',
                           org=org_info_parse, objectId=obj_id,
                           notifications=notifications, messages=messages)


def fetch_timeline_data(user_objectId):
    relevant_data = []
    quiz_obj = QuizPersonalStatistics.Query.all().filter().limit(900)
    question_obj = QuestionPersonalStatistics.Query.all().filter().limit(17000)
    quizling_obj = Quizling.Query.all().filter().limit(500)

    for quiz_stat in quiz_obj:
        quiz_data = []
        quiz_id = quiz_stat.quizling.objectId
        quiz_name = ""
        for q in quizling_obj:
            if q.objectId == quiz_id:
                quiz_name = q.name

        if (quiz_stat.user.objectId == user_objectId):
            quiz_data.append(quiz_name)
            quiz_data.append(quiz_id)
            quiz_data.append(quiz_stat.averageScore)
            quiz_data.append(quiz_stat.updatedAt)

            # convert datetime.datetime to string, take out punctuation,
            # take out whitespace, finally convert to integer so it is a
            # numeric date-timestamp
            quiz_data.append(int(str(quiz_stat.updatedAt).translate(None, string.punctuation).replace(' ', '')))

            for quest_stat in question_obj:
                quest_data = []
                if (quest_stat.quizling.objectId == quiz_id) and (quest_stat.person.objectId == user_objectId):
                    quest_data.append(quest_stat.objectId)
                    quest_data.append(quest_stat.geolocation.latitude)
                    quest_data.append(quest_stat.geolocation.longitude)
                    if quest_data:
                        quiz_data.append(quest_data)

        if quiz_data: # data is sometimes empty. Discard those entries in relevant_data.
            relevant_data.append(quiz_data)

    # sorts the list, relevant_data, by the 3-th value in each sublist
    # (a numeric date), in descending order.
    relevant_data.sort(key=lambda x: x[4], reverse=True)

    return relevant_data


@manager.route('/timeline', methods=['GET', 'POST'])
def timeline():
    global notifications, messages

    username = request.cookies.get('username')
    user_objectId = request.cookies.get('user_objectId')

    if username is None:
        print "Error: user returned None"
        return redirect(url_for(''))
        # exit()

    relevant_data = fetch_timeline_data(user_objectId)

    # send the data to timeline.html using Jinja2, built in to Flask.
    return render_template('timeline.html', org=org_info_parse,
                        relevant_data=relevant_data, objectId = user_objectId,
                        notifications=notifications, messages=messages)


@manager.route('/favourites')
def bookmark():
    global notifications, messages, following, follower
    return render_template('bookmark.html',
                           notifications=notifications, messages=messages, followings=following, followers=follower)


@manager.route('/inbox')
def inbox():
    global notifications, messages
    return render_template('inbox.html',
                           notifications=notifications, messages=messages)


@manager.route('/inbox/markasread',methods=['POST'])
def markMessagesAsRead():
    global notifications, messages
    parsedMsg = json.loads(request.form.keys()[0])
    readMessages = parsedMsg["result"]
    for messageId in readMessages:
        print messageId
        message = Message.Query.get(objectId=messageId)
        message.read = True
        message.save()
    for message in messages:
        if message.objectId in readMessages:
            messages.remove(message)
    return "success"
    # return redirect(url_for('inbox'))


@manager.route('/inbox/delete',methods=['POST'])
def deleteMessages():
    global notifications, messages
    parsedMsg = json.loads(request.form.keys()[0])
    deletedMessages = parsedMsg["result"]
    for messageId in deletedMessages:
        message = Message.Query.get(objectId=messageId)
        message.delete()
    for message in messages:
        if message.objectId in deletedMessages:
            messages.remove(message)
    return "success"
    # return redirect(url_for('inbox'))


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
    reqJSON = json.loads(request.form.keys()[0])
    order = True
    if reqJSON["order"] != 'ascending':
        order = False
    if reqJSON["field"] == 'name':
        filteredResult.sort(key=lambda x: x.name, reverse=order)
    if reqJSON["field"] == 'updatedAt':
        filteredResult.sort(key=lambda x: x.updatedAt, reverse=order)
    if reqJSON["field"] == 'averageScore':
        filteredResult.sort(key=lambda x: x.averageScore, reverse=order)
    if reqJSON["field"] == 'playCount':
        filteredResult.sort(key=lambda x: x.playCount, reverse=order)
    return makeJSONquizzes(filteredResult)

@manager.route("/share", methods=['POST'])
def share(test=False, userName="", quizName="", quizId=""):
    # cases of test mode and none test mode
    if not test:
        reqJSON = json.loads(request.form.keys()[0])
        userName = request.cookies.get('username')
        user = _User.Query.get(username=userName)
        quizName = reqJSON["name"]
        quizId = reqJSON["Id"]
    else:
        user = _User.Query.get(username=userName)

    followers = Following.Query.filter(user=user)

    for follower in followers:
        notification = Notification()
        notification.fromUser = userName
        notification.to = follower.subscriber.username
        notification.quizName = quizName
        notification.quizId = quizId
        notification.read = False
        notification.save()
    print "finished sending share notification"
    if not test:
        return '{"result":1}'
    else:
        return userName

@manager.route("/message", methods=['POST'])
def sendMessage(test=False, userName ="", toUserName="", content=""):
    if not test:
        eqJSON = json.loads(request.form.keys()[0])
        userName = request.cookies.get('username')
        toUserName = eqJSON["name"]
        content = eqJSON["message"]
    message = Message()
    message.fromUser = userName
    message.toUser = toUserName
    message.content = content
    message.save()
    return '{"result":1}'

if __name__ == '__main__':
    manager.run(debug=True)
