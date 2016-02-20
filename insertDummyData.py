from pymongo import MongoClient




print 'starting script'
client = MongoClient('localhost',27017)
db = client['discovering_user_db']
collection = db['test_user_name']
dummyQuiz1 = {'name':'testQuizName1','score':90,'type':'quiz_result'}
dummyQuiz2 = {'name':'testQuizName2','score':80,'type':'quiz_result'}
dummyQuiz3 = {'name':'testQuizName3','score':99,'type':'quiz_result'}
stuff = [dummyQuiz1, dummyQuiz2, dummyQuiz3]
collection.insert_many(stuff)
print 'finished script'
