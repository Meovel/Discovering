var _ = require('underscore.js');
var lib = require("cloud/lib.js");
var AUTOPLAY = "autoplay";
// exports
var exports = {
    "deleteQuizlingRalations": deleteQuizlingRalations,
    "assignFollowers": assignFollowers,
    "assignFollowings": assignFollowings,
    "getOrgUsers": getOrgUsers,
    "getPrivateUsers": getPrivateUsers,
    "completedQuizling": completedQuizling,
    "getBestGame": getBestGame,
    "getUserGameCount": getUserGameCount,
    "getUserById": getUserById,
    "unfollowUser": unfollowUser,
    "deleteQuizlingPiecemeal": deleteQuizlingPiecemeal,
    "setBestGames": setBestGames,
    "addFollowers": addFollowers // old
};
module.exports = exports;

function setBestGames(iterations) {
    var query = new Parse.Query("Game");
    var best = {};
    var promise = Parse.Promise.as();
    for(var i = 0; i < iterations; i++) {
        promise = promise.then(function() {
            query.equalTo("best", undefined);
            return query.first()
                .then(function(game) {
                    if (!game) {
                        throw "all games was changed";
                    }
                    var query2 = new Parse.Query("Game");
                    query2.equalTo("quizling", game.get("quizling"));
                    query2.equalTo("user", game.get("user"));
                    return lib.findAll(query2)
                        .then(function(uniques) {
                            return checkGames(uniques)
                                .then(function() {
                                    best = uniques[0];
                                    _.each(uniques, function(unique) {
                                        if (unique.get("endScore") && (unique.get("endScore") > best.get("endScore"))) {
                                            best = unique;
                                        }
                                    });
                                    return saveHighScore(best)
                                        .then(function() {
                                            best.set("best", true);
                                            return best.save();
                                        })
                                })
                        })
                })
        });
    }
    return promise;
}

function saveHighScore(game) {
    var HighScore = Parse.Object.extend("HighScore");
    var highScore = new HighScore();
    highScore.set("totalTime", game.get("totalTime"));
    highScore.set("quizling", game.get("quizling"));
    highScore.set("correctAnswers", game.get("correctAnswers"));
    highScore.set("totalQuestions", game.get("totalQuestions"));
    highScore.set("endScore", game.get("endScore"));
    highScore.set("user", game.get("user"));
    highScore.set("geolocation", game.get("geolocation"));
    highScore.set("gameId", game.id);
    return highScore.save()
}

function checkGames(uniques) {
    var promises = [];
    _.each(uniques, function(unique) {
        unique.set("best", false);
        promises.push(unique.save())
    });
    return Parse.Promise.when(promises)
}

function deleteQuizlingPiecemeal(quizling) {
    var query = new Parse.Query("Question");
    var questionIds = [];
    query.equalTo("quizling", quizling);
    return lib.findAll(query)
        .then(function(results) {
            if(results.length > 0) {
                var quizlingDelete = new Parse.Object("QuizlingDelete");
                questionIds = {
                    quizid: quizling.id,
                    questionIds:_.pluck(results, 'id')
                };
                quizlingDelete.set("quizId", quizling.id);
                quizlingDelete.set("questionIds", questionIds);
                return quizlingDelete.save()
                    .then(function() {
                        return Parse.Object.destroyAll(results);
                    })
            }
        });
}

function deleteQuizlingRalations(quizling) {
    var promise = Parse.Promise.as();
    var relationTables = {
        DownloadedQuizling: "quizling",
        SharedQuizling: "quizling",
        Game: "quizling",
        HighScore: "quizling",
        QuestionPersonalStatistics: "quizling",
        QuizPersonalStatistics: "quizling",
        Question: "quizling"
    };
    _.each(relationTables, function(columnName, relationTable) {
        promise = promise.then(function() {
            var query = new Parse.Query(relationTable);
            query.equalTo(columnName, quizling);
            return lib.findAll(query)
                .then(function(results) {
                    if(results.length > 0) {
                        return Parse.Object.destroyAll(results);
                    }
                });
        });
    });
    return promise;
}

function assignFollowings(followers, followings) {
    var promise = Parse.Promise.as();
    var promises = [];
    _.each(followers, function(follower) {
        promise = promise.then(function() {
            _.each(followings, function(following) {
                var relation = following.relation("followers");
                promises.push(relation.add(follower));
            });
            return Parse.Promise.when(promises);
        }).then(function() {
            return Parse.Object.saveAll(followings);
        })
    });
    return promise;
}

function assignFollowers(followers, followings) {
    var promise = Parse.Promise.as();
    var promises = [];
    _.each(followings, function(following) {
        promise = promise.then(function() {
            _.each(followers, function(follower) {
                var relation = follower.relation("followings");
                promises.push(relation.add(following));
            });
            return Parse.Promise.when(promises);
        }).then(function() {
            return Parse.Object.saveAll(followers);
        })
    });
    return promise;
}

function unfollowUser(follower, following) {
    var relation1 = follower.relation("followings");
    var relation2 = following.relation("followers");
    relation1.remove(following);
    relation2.remove(follower);
    return following.save()
        .then(function() {
            return follower.save();
        })
}

function getOrgUsers() {
    var orgUsers = new Parse.Query(Parse.User);
    orgUsers.equalTo("type", "org");
    return lib.findAll(orgUsers);
}

function getPrivateUsers() {
    var privateUsers = new Parse.Query(Parse.User);
    privateUsers.equalTo("type", "private");
    return lib.findAll(privateUsers);
}

function getQuizlingById(quizlingId) {
    var query = new Parse.Query("Quizling");
    query.equalTo("objectId", quizlingId);
    return query.first();
}

function setQuizlingScore(request, object) {
    var currentPlaycount = object.get("playCount");
    if (currentPlaycount === undefined) {
        currentPlaycount = 0;
    }
    var newPlayCount = currentPlaycount + 1;
    var currentAverage = object.get("averageScore");
    if (currentAverage === undefined) {
        currentAverage = 0;
    }
    var newAverage = (currentAverage * currentPlaycount + request.params.correctAnswers) / newPlayCount;
    object.set("averageScore", newAverage);
    object.set("playCount", newPlayCount);
    return object.save();
}

/**
 *
 * @param request
 * @returns {*}
 */
function completedQuizling(request) {
    var quizlingId  = request.params.quizlingId;
    var gameMode = request.params.gameMode;
    return getQuizlingById(quizlingId)
        .then(function(object) {
            return setQuizlingScore(request, object)
                .then(function(object) {
                    return getHighScore(request.user, object)
                    .then(function(highScoreObj) {
                        if (highScoreObj && gameMode == AUTOPLAY) {
                            if (highScoreObj.get("endScore") <= request.params.endScore) {
                                return destroyHighScore(highScoreObj)
                            }
                        }
                        return Parse.Promise.as("");
                    })
                    .then(function() {
                        return getHighScore(request.user, object)
                            .then(function(bestGameObj) {
                                console.log({bestGame: !_.isEmpty(bestGameObj)});
                                if (!_.isEmpty(bestGameObj)) {
                                    if (bestGameObj.get("endScore") <= request.params.endScore) {
                                        return changeBestGame(bestGameObj)
                                            .then(function() {
                                                return createGame(request, object, true);
                                            })
                                    } else {
                                        return createGame(request, object, false);
                                    }
                                } else {
                                    return createGame(request, object, true);
                                }
                            })
                    })
                })
        })
}

function destroyHighScore(bestGameObj)
{
    return bestGameObj.destroy()
}

function changeBestGame(bestGameObj)
{
    bestGameObj.set("best", false);
    return bestGameObj.save()
}

function getHighScore(user, object) {
    var query = new Parse.Query("HighScore");
    query.equalTo("quizling", object);
    query.equalTo("user", user);
    return query.first();
}

function getBestGame(user, object) {
    var query = new Parse.Query("Game");
    query.equalTo("quizling", object);
    query.equalTo("user", user);
    query.equalTo("best", true);
    return query.first();
}

function getUserGameCount(user, object) {
    var query = new Parse.Query("Game");
    query.equalTo("quizling", object);
    query.equalTo("user", user);
    return query.count();
}


function createGame(request, object, best) {
    var gameMode = request.params.gameMode;
    var Game = Parse.Object.extend("Game");
    var game = new Game();
    game.set("totalTime", request.params.totalTime);
    game.set("quizling", object);
    game.set("quizlingOwner", object.get("owner").id);
    game.set("correctAnswers", request.params.correctAnswers);
    game.set("totalQuestions", request.params.totalQuestions);
    game.set("endScore", request.params.endScore);
    game.set("user", request.user);
    game.set("best", best);
    game.set("geolocation", request.params.geolocation);
    return game.save()
        .then(function() {
            console.log({gameMode: gameMode});
            if (best && gameMode == AUTOPLAY) {
                console.log({gameMode: gameMode, best: best});
                var HighScore = Parse.Object.extend("HighScore");
                var highScore = new HighScore();
                highScore.set("totalTime", request.params.totalTime);
                highScore.set("quizling", object);
                highScore.set("correctAnswers", request.params.correctAnswers);
                highScore.set("totalQuestions", request.params.totalQuestions);
                highScore.set("endScore", request.params.endScore);
                highScore.set("user", request.user);
                highScore.set("best", best);
                highScore.set("geolocation", request.params.geolocation);
                highScore.set("gameId", game.id);
                return highScore.save()
            }
            return Parse.Promise.as("");
        })
        .then(function() {
            var query2 = new Parse.Query("QuizPersonalStatistics");
            var requestUser = request.user;
            query2.equalTo("user", requestUser);
            query2.equalTo("quizling", object);
            return query2.find()
                .then(function(results) {
                    if (results.length > 0) {
                        var stats = results[0];
                        var currentPlaycount = stats.get("playCount");
                        if (currentPlaycount === undefined) {
                            currentPlaycount = 0;
                        }
                        var newPlayCount = currentPlaycount + 1;
                        var currentAverage = stats.get("averageScore");
                        if (currentAverage === undefined) {
                            currentAverage = 0;
                        }
                        var newAverage = (currentAverage * currentPlaycount + request.params.correctAnswers) / newPlayCount;
                        stats.set("averageScore", newAverage);
                        stats.set("playCount", newPlayCount);
                        return stats.save()
                            .then(function() {
                                return game.id
                            })
                    } else {
                        var QuizPersonalStatistics = Parse.Object.extend("QuizPersonalStatistics");
                        var stats = new QuizPersonalStatistics();
                        stats.set("user", request.user);
                        stats.set("quizling", object);
                        stats.set("playCount", 1);
                        stats.set("averageScore", request.params.correctAnswers);
                        return stats.save()
                            .then(function() {
                                return game.id
                            })
                    }
                })
        })
}

function getUserById(userId) {
    var query = new Parse.Query(Parse.User);
    query.equalTo("objectId", userId);
    return query.first();
}

function addFollowers(orgUserObj) {
    return getPrivateUsers()
        .then(function(privateUsersObj) {

            // old realization
            var promises = [];
            _.each(privateUsersObj, function(privateUserObj) {
                var Following = Parse.Object.extend("Following");
                var following = new Following();
                following.set("user", orgUserObj);
                following.set("subscriber", privateUserObj);
                promises.push(following.save());
            });
            return Parse.Promise.when(promises);

            // new realization
            //return assignFollowers([orgUserObj], privateUsersObj)
            //    .then(function() {
            //        return assignFollowings([orgUserObj], privateUsersObj)
            //    })
        })
}