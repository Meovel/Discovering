// exports
var exports = {
    "getNewQuizling": getNewQuizling,
    "getQuestions": getQuestions,
    "parseQuestions": parseQuestions,
    "prepareQuestionPersonalStatistics": prepareQuestionPersonalStatistics,
    "addNewQuestionPersonalStatistics": addNewQuestionPersonalStatistics,
    "getBUser": getBUser
};
module.exports = exports;

var MAX_ANSWER_TIME = 15;
var MAX_SCORE = 1000;
var DEFAULT_READ_SPEED = 14; // letter per second (this value is random)
var MAX_READ_SPEED = 21; // letter per second (this value is random)
var DEFAULT_LUCK = 50; // luck : how quickly the user to remember the right answer, this value like percent (50%)
var MAX_LUCK = 100; //this value like percent (100%)
var DEFAULT_IQ = 50; // IQ : if the user knows the answer, this value like percent (50%)
var MAX_IQ = 100; // this value like percent (100%)
var MAX_PERCENTS = 100; // this value like percent (100%)
var TIME_OUT_TEXT = "questionNotAnsweredInTime";
var BONUS = 0;
var BONUS_INCREMENT = 33.3; // each pass Quizling Increases IQ, luck, readSpeed user-bot 1/3
var PRIVATE_USER = "private";
// underscore
var _ = require("underscore.js");
var lib = require("cloud/lib.js");
var manager = require("cloud/manager.js");

/**
 * Get random quizling
 * @returns {*}
 */
function getNewQuizling() {
    var BSettings = Parse.Object.extend("BSettings");
    var query = new Parse.Query(BSettings);
    return query.first()
        .then(function(settings) {
            var triggeringChance = (settings.get("triggeringChance") ? settings.get("triggeringChance") : settings.get("defaultTriggeringChance"));
            if (Math.floor((MAX_PERCENTS * Math.random() + (MAX_PERCENTS - (MAX_PERCENTS - triggeringChance) ))) + 1 <= MAX_PERCENTS) {
                var increaseTrigger = (Math.floor(triggeringChance / 2) + triggeringChance < MAX_PERCENTS ? Math.floor(triggeringChance / 2) : MAX_PERCENTS - triggeringChance);
                settings.increment("triggeringChance", increaseTrigger);
                return settings.save()
                    .then(function() {
                        return Parse.Promise.error({"message": "trigger not work, increase chance to " + (triggeringChance + increaseTrigger) + "%"});
                    })
            } else {
                settings.set("triggeringChance", settings.get("defaultTriggeringChance"));
                return settings.save()
                    .then(function() {
                        var Quizling = Parse.Object.extend("Quizling");
                        var temporizingHours = settings.get("temporizingHours");
                        var temporizingTime = new Date(new Date().setHours(new Date().getHours() - temporizingHours));
                        var query = new Parse.Query("Quizling");
                        query.greaterThan("createdAt", temporizingTime);
                        query.equalTo("userType", PRIVATE_USER);
                        return lib.findAll(query)
                            .then(function(quizlings) {
                                if (quizlings.length > 0) {
                                    return _.first(_.shuffle(quizlings));
                                } else {
                                    return Parse.Promise.error({"message": "new quziling not found"});
                                }
                            })
                    })
            }
        })
}


function getBUser() {
    var BUser = Parse.Object.extend("BUser");
    var bUser = new Parse.Query(BUser);
    bUser.include("user");
    return bUser.find()
        .then(function(users) {
            if (users.length == 0) {
                return Parse.Promise.error({"message": "user not found"});
            }
            return Parse.Promise.as(users[Math.floor(Math.random() * users.length)])
        })
}

function getAnsweredQuestion(questionId, questionStatistics) {
    for(var i = 0; i < questionStatistics.length; i++) {
        if (questionId == questionStatistics[i].get("question").id) {
            return questionStatistics[i];
        }
    }
}
function prepareQuestionPersonalStatistics(questions, userData) {
    var person = userData.get("user");
    var quizling = {};
    if (questions[0] && questions[0].get("quizling")) {
        quizling = questions[0].get("quizling");
    } else {
        return Parse.Promise.error({"message": "No questions found"});
    }
    return manager.getUserGameCount(person, quizling)
        .then(function(count) {
            return manager.getBestGame(person, quizling)
                .then(function(bestGame) {
                    var replyGame = false;
                    if (bestGame) {
                        var query = new Parse.Query("QuestionPersonalStatistics");
                        query.equalTo("game", bestGame);
                        BONUS = count * BONUS_INCREMENT;
                        return query.find()
                            .then(function(questionStatistics) {
                                if (questionStatistics.length !== questions.length) {
                                    return Parse.Promise.error({"message": "an error in the statistics of the quiz"})
                                }
                                replyGame = true;
                                return setStatistic(questions, userData, quizling, replyGame, questionStatistics);
                            });
                    } else {
                        return setStatistic(questions, userData, quizling, replyGame);
                    }
                });
        })
}

function setStatistic(questions, userData, quizling, replyGame, questionStatistics) {
    var geolocation = getGeoPointExpression(userData);
    var score = 0;
    var totalTime = 0;
    var correctAnswerCount = 0;
    var person = userData.get("user");
    var questionPersonalStatistics = [];
    var totalQuestions = 0;
    var correctlyAnswered = false;
    _.each(questions, function(question) {
        if (replyGame) {
            var answeredQuestion = getAnsweredQuestion(question.id, questionStatistics);
            correctlyAnswered = answeredQuestion.get("correctlyAnswered");
        }
        var timeUsed = getTimeUsedExpression(question, userData);
        var answered = getAnswerExpression(question, userData, timeUsed, correctlyAnswered);
        var questionStatistic = {
            geolocation: geolocation,
            person: person,
            question:question,
            quizling: quizling,
            timeUsed: timeUsed,
            game: "",
            correctlyAnswered: answered.correctlyAnswered,
            answered: answered.answer
        };
        score += getScoreExpression(timeUsed);
        questionPersonalStatistics.push(questionStatistic);
        totalTime += timeUsed;
        totalQuestions++;
        correctAnswerCount += answered.correctAnswerCount;
    });
    return {
        completedQuizling: {
            params: {
                correctAnswers: correctAnswerCount,
                endScore: score,
                geolocation: geolocation,
                totalQuestions: totalQuestions,
                totalTime: totalTime,
                quizlingId: questions[0].get("quizling").id
            },
            user: userData.get("user")
        },
        questionPersonalStatistics: questionPersonalStatistics
    };
}

function getAnswerExpression(question, userData, timeUsed, answeredQuestion) {
    if (timeUsed === 0) {
        return  {
            correctlyAnswered: false,
            answer: TIME_OUT_TEXT,
            correctAnswerCount: 0
        };
    }
    var bonus = BONUS / MAX_PERCENTS + 1;
    var IQ = (userData.get("IQ") ? (userData.get("IQ") * bonus >= MAX_IQ ? MAX_IQ : userData.get("IQ") * bonus) : DEFAULT_IQ * bonus);
    var answers = question.get("answers");
    var answer = question.get("correctAnswer");
    var notCorrectAnswers = [];
    for (var i = 0; i < answers.length; i++) {
        if (answers[i] != answer) {
            notCorrectAnswers.push(answers[i]);
        }
    }
    if (answeredQuestion) {
        return {
            correctlyAnswered: true,
            answer: answer,
            correctAnswerCount: 1
        };
    } else {
        if (Math.floor((MAX_PERCENTS * Math.random() + (MAX_PERCENTS - (MAX_PERCENTS - IQ) ))) <= MAX_PERCENTS) {
            return {
                correctlyAnswered: true,
                answer: answer,
                correctAnswerCount: 1
            };
        } else {
            return {
                correctlyAnswered: false,
                answer: notCorrectAnswers[Math.floor(Math.random() * notCorrectAnswers.length)],
                correctAnswerCount: 0
            };
        }
    }
}

function getRandomArbitary(min, max)
{
    return Math.random() * (max - min) + min;
}

function getGeoPointExpression(userData) {
    var latitude = userData.get("geo").latitude;
    var longitude = userData.get("geo").longitude;
    var randLatitude = parseFloat(getRandomArbitary(latitude - 1, latitude + 1).toFixed(4));
    var randLongitude = parseFloat(getRandomArbitary(longitude - 1, longitude + 1).toFixed(4));
    return new Parse.GeoPoint({latitude: randLatitude, longitude: randLongitude});
}

function getTimeUsedExpression(question, userData) {
    var bonus = BONUS / MAX_PERCENTS + 1;
    var readSpeed = (userData.get("readSpeed") ? (userData.get("readSpeed") * bonus >= MAX_READ_SPEED ? MAX_READ_SPEED : userData.get("readSpeed") * bonus) : DEFAULT_READ_SPEED * bonus);
    var answersLength = 0;
    for (var i = 0; i < question.get("answers").length; i++) {
        answersLength += question.get("answers")[i].length;
    }
    var questionLength = (question.get("questionText").length);
    var timeSpentReading = (questionLength + answersLength) / readSpeed;

    var IQ = (userData.get("IQ") ? (userData.get("IQ") * bonus >= MAX_IQ ? MAX_IQ : userData.get("IQ") * bonus) : DEFAULT_IQ * bonus);
    var luck = (userData.get("luck") ? (userData.get("luck") * bonus >= MAX_LUCK ? MAX_LUCK : userData.get("luck") * bonus) : DEFAULT_LUCK * bonus);

    var timeThink = (((MAX_PERCENTS - luck) / MAX_PERCENTS) + ((MAX_PERCENTS - IQ) / MAX_PERCENTS )) * MAX_ANSWER_TIME;
    var timeThinkRand = Math.floor(Math.random() * timeThink) + 1;
    return (Math.floor(timeThinkRand + timeSpentReading) < MAX_ANSWER_TIME ? Math.floor(timeThinkRand + timeSpentReading) : 0);
}

function addNewQuestionPersonalStatistics(questionsAnswered, gameId) {
    Parse.Cloud.useMasterKey();
    var promises = [];
    var Game = Parse.Object.extend("Game");
    var game = new Parse.Query(Game);
    game.equalTo("objectId", gameId);
    return game.first()
        .then(function(gameObject) {
            _.each(questionsAnswered, function(answered) {
                var QuestionPersonalStatistics = Parse.Object.extend("QuestionPersonalStatistics");
                var query = new QuestionPersonalStatistics();
                query.set("answered", answered.answered);
                query.set("correctlyAnswered", answered.correctlyAnswered);
                query.set("game", gameObject);
                query.set("geolocation", answered.geolocation);
                query.set("person", answered.person);
                query.set("question", answered.question);
                query.set("quizling", answered.quizling);
                query.set("timeUsed", answered.timeUsed);
                promises.push(query.save());
            });
            return Parse.Promise.when(promises);
        });
}

function parseQuestions(/*array*/ qustions) {
    var answers = [];
    qustions.forEach(function(qustion) {
        answers["answers"].push(qustion.get("answers"));
        answers["correctAnswer"].push(qustion.get("correctAnswer"));
    });
    return Parse.Promise.as(answers);
}
/**
 * Get all the questions available in quizling
 * @param quizling
 * @returns {*}
 */
function getQuestions(/*object*/ quizling) {
    console.log(["quizling in job", quizling.id]);
    var query = new Parse.Query("Question");
    query.equalTo("quizling", quizling);
    query.ascending("order");
    return query.find();
}

/**
 * Scoring makes the logic
 * @param timeUsed
 * @returns {number}
 */
function getScoreExpression(timeUsed) {
    var score = Math.floor((MAX_ANSWER_TIME - timeUsed) * MAX_SCORE/MAX_ANSWER_TIME);
    return (timeUsed > 0 ? score : 0);
}