# Inserts dummy data to mongodb, currently for templates/stats.html
# author kkim110, shauk2
from pymongo import MongoClient
import pymongo
from bson import json_util

print 'starting script'
client = MongoClient('localhost',27017)
db = client['discovering_user_db']
db.drop_collection('test_user_name')
collection = db['test_user_name']
dummyQuiz1 = {'name':'testQuizName1','score':90,'type':'quiz_result','time':1}
dummyQuiz2 = {'name':'testQuizName2','score':80,'type':'quiz_result','time':2}
dummyQuiz3 = {'name':'testQuizName3','score':99,'type':'quiz_result','time':3}
stuff = [dummyQuiz1, dummyQuiz2, dummyQuiz3]
# Test to ensure database connection was valid
try:
    collection.insert_many(stuff)
except: # If not valid db connection, ie, then...
    print("Database may not be properly connected. Could not insert data")
results = collection.find({'type':'quiz_result'}).sort([('time', pymongo.DESCENDING)])
for result in results:
	print json_util.dumps(result,default=json_util.default)
print 'finished script'
