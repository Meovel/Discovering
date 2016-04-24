var _ = require("underscore.js");
var manager = require("cloud/manager.js");
var lib = require("cloud/lib.js");
var Image = require("parse-image");

Parse.Cloud.define("hello", function(request, response) {
  response.success("Hello world!");
});

Parse.Cloud.define("timelineSpike", function(request, response) {
  var query = new Parse.Query("QuizPersonalStatistics");
  // query.include("user");
  // query.include("averageScore");

  // var GameScore = Parse.Object.extend("GameScore");
  // var query = new Parse.Query(GameScore);
  // query.equalTo("playerName", "Dan Stemkoski");



  query.find({
    success: function(results) {
      alert("Successfully retrieved " + results.length + " scores.");
      // Do something with the returned Parse.Object values
      for (var i = 0; i < results.length; i++) {
        var object = results[i];
        alert('user - ' + object.get('user'));
      }
      return results;
    },
    error: function(error) {
      alert("Error: " + error.code + " " + error.message);
    }
  });

});

Parse.Cloud.define("completedQuizling", function(request, response) {
    Parse.Cloud.useMasterKey();
    manager.completedQuizling(request)
        .then(
        function(success) {
            return response.success(success);
        },
        function(error) {
            return response.error(error);
        });
});

Parse.Cloud.afterSave("QuestionPersonalStatistics", function(request) {
    Parse.Cloud.useMasterKey();

    var answer = request.object.get("correctlyAnswered");
    var questionId = request.object.get("question");

    query = new Parse.Query("Question");

    query.get(questionId.id, {
        success : function(question) {
            if (answer) {
                if (question.get("correctAnswers") === undefined) {
                    question.set("correctAnswers", 0);
                }
                question.increment("correctAnswers");
            } else {
                if (question.get("wrongAnswers") === undefined) {
                    question.set("wrongAnswers", 0);
                }
                question.increment("wrongAnswers");
            }
            question.save();
        },

        error : function(error) {
            console.error(error);
        }
    });
});

Parse.Cloud.define('chargeCard', function(req,res) {
    var Stripe = require('stripe');
    Stripe.initialize('sk_live_yrowO83jtcnUDCpjX1fLApuK');

    var token = req.params.token;

    var charge = Stripe.Charges.create({
        amount: 1000, // amount in cents, again
        currency: "aud",
        source: token,
        description: "Quizling access fee"
    }).then(function(data){
        res.success(data);
    }, function(data) {
        console.log(data);
        res.error(data);
    });
});

Parse.Cloud.beforeSave("Quizling", function(request, response) {
    var quizling = request.object;
    if (!quizling.get("image")) {
        response.error("No image to resize.");
        return;
    }

    if (!quizling.dirty("image")) {
        // The quizling photo isn't being modified.
        response.success();
        return;
    }

    Parse.Cloud.httpRequest({
        url: quizling.get("image").url()

    }).then(function(response) {
        var image = new Image();
        return image.setData(response.buffer);

    }).then(function(image) {
        // Resize the image to 0.15
        return image.scale({
            width: image.width()*0.15,
            height: image.height()*0.15
        });

    }).then(function(image) {
        return image.setFormat("PNG");
    }).then(function(image) {
        // Get the image data in a Buffer.
        return image.data();

    }).then(function(buffer) {
        // Save the image into a new file.
        var base64 = buffer.toString("base64");
        var image = new Parse.File("file.png", { base64: base64 });
        return image.save();

    }).then(function(image) {
        // Attach the image file to the original object.
        quizling.set("imageThumbnail", image);

    }).then(function(result) {
        response.success();
    }, function(error) {
        response.error(error);
    });
});

Parse.Cloud.job("bot", function(request, response) {
    Parse.Cloud.useMasterKey();
    var bot = require("cloud/bot.js");
    var userData = {};
    bot.getBUser()
        .then(function(user) {
            userData = user;
            return Parse.Promise.as(userData);
        })
        .then(function(userData) {
            return bot.getNewQuizling()
                .then(bot.getQuestions)
                .then(function(questions) {
                    return bot.prepareQuestionPersonalStatistics(questions, userData)
                })
                .then(function(response) {
                    return manager.completedQuizling(response.completedQuizling)
                        .then(function(gameId) {
                            return bot.addNewQuestionPersonalStatistics(response.questionPersonalStatistics, gameId)
                        });
                })
        })
        .then(
        function () {
            return response.success("game completed");
        },
        function (error) {
            return response.error(error.message);
        });
});

Parse.Cloud.define("deleteQuizling", function(request, response) {
    Parse.Cloud.useMasterKey();
    var quizlingId = request.params.id;

    var query = new Parse.Query("Quizling");
    query.equalTo("objectId", quizlingId);
    return query.first()
        .then(function(quizling) {
            if (quizling) {
                return manager.deleteQuizlingRalations(quizling)
                    .then(function() {
                        return quizling.destroy();
                    });
            } else {
                return Parse.Promise.error("quizling not found")
            }
        })
        .then(
        function () {
            return response.success("quizling was deleted");
        },
        function (error) {
            return response.error(error);
        });
});

Parse.Cloud.define("deleteQuizlingPiecemeal", function(request, response) {
    Parse.Cloud.useMasterKey();
    var quizlingId = request.params.id;

    var query = new Parse.Query("Quizling");
    query.equalTo("objectId", quizlingId);
    return query.first()
        .then(function(quizling) {
            if (quizling) {
                return manager.deleteQuizlingPiecemeal(quizling)
                    .then(function() {
                        return quizling.destroy();
                    });
            } else {
                return Parse.Promise.error("quizling not found")
            }
        })
        .then(
        function () {
            return response.success("quizling was deleted");
        },
        function (error) {
            return response.error(error);
        });
});

// followings section _________________________________________________________

// from old to new realization
Parse.Cloud.beforeSave("Following", function(request, response) {
    Parse.Cloud.useMasterKey();
    var object = request.object;
    var user = object.get("user");
    var subscriber = object.get("subscriber");
    var relationFollowings = subscriber.relation("followings");
    relationFollowings.add(user);
    var relationFollowers = user.relation("followers");
    relationFollowers.add(subscriber);
    subscriber.save()
        .then(function () {
            return user.save()
        })
        .then(function(result) {
            response.success();
        }, function(error) {
            response.error(error);
        });
});

// new
Parse.Cloud.beforeDelete("Following", function(request, response) {
    Parse.Cloud.useMasterKey();

    var object = request.object;
    var user = object.get("user");
    var subscriber = object.get("subscriber");
    var relationFollowings = subscriber.relation("followings");
    relationFollowings.remove(user);
    var relationFollowers = user.relation("followers");
    relationFollowers.remove(subscriber);
    subscriber.save()
        .then(function () {
            return user.save()
        })
        .then(function(result) {
            response.success();
        }, function(error) {
            response.error(error);
        });
});

// old
Parse.Cloud.afterSave(Parse.User, function(request) {
    Parse.Cloud.useMasterKey();
    var user = request.object;
    if (!user.existed()) {
        if (user.get("type") == "org") { // todo: set const
            return manager.addFollowers(user) // old
                .then(
                function () {
                    return response.success();
                },
                function (error) {
                    return response.error(error);
                });
        }
    }
    return response.success();
});

// new
Parse.Cloud.define("followUser", function(request, response) {
    Parse.Cloud.useMasterKey();
    if (!request.user) {
        return response.error("user not found");
    }
    if (!request.params.followingId) {
        return response.error("user to follow - not found");
    }
    manager.getUserById(request.params.followingId)
        .then(function(following) {
            return manager.assignFollowers([request.user], [following])
                .then(function() {
                    return manager.assignFollowings([request.user], [following])
                        .then(function() {
                            return Parse.Promise.as("Now you follow " + following.get("username"));
                        })
                })
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// new
Parse.Cloud.define("unfollowUser", function(request, response) {
    Parse.Cloud.useMasterKey();
    if (!request.user) {
        return response.error("user not found");
    }
    if (!request.params.followingId) {
        return response.error("user to follow - not found");
    }
    manager.getUserById(request.params.followingId)
        .then(function(following) {
            return manager.unfollowUser(request.user, following)
                .then(function() {
                    return Parse.Promise.as("You no longer follow " + following.get("username"));
                })
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// new
Parse.Cloud.define("removeFollower", function(request, response) {
    Parse.Cloud.useMasterKey();
    if (!request.user) {
        return response.error("user not found");
    }
    if (!request.params.followerId) {
        return response.error("user to remove - not found");
    }
    manager.getUserById(request.params.followerId)
        .then(function(follower) {
            return manager.unfollowUser(follower, request.user)
                .then(function() {
                    return Parse.Promise.as(follower.get("username") + " will no longer follow you");
                })
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// new
// one-time run script
Parse.Cloud.define("subscribeFollowings", function(request, response) {
    Parse.Cloud.useMasterKey();
    manager.getOrgUsers()
        .then(function(orgUsersObj) {
            return manager.getPrivateUsers()
                .then(function(privateUsersObj) {
                    return manager.assignFollowings(orgUsersObj, privateUsersObj)
                })
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// new
// one-time run script
Parse.Cloud.define("subscribeFollowers", function(request, response) {
    Parse.Cloud.useMasterKey();
    manager.getOrgUsers()
        .then(function(orgUsersObj) {
            return manager.getPrivateUsers()
                .then(function(privateUsersObj) {
                    return manager.assignFollowers(orgUsersObj, privateUsersObj)
                })
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// old
// one-time run script
Parse.Cloud.define("followOrgUsers", function(request, response) {
    var userId = request.params.userId;
    var _ = require("underscore.js");
    var orgUser = new Parse.Query(Parse.User);
    orgUser.equalTo("type", "org");
    orgUser.equalTo("objectId", userId);
    return orgUser.find()
        .then(function(orgUsersObj) {
            var promise = Parse.Promise.as();
            _.each(orgUsersObj, function(orgUserObj) {
                promise = promise.then(function() {
                    var privateUser = new Parse.Query(Parse.User);
                    privateUser.equalTo("type", "private");
                    return lib.findAll(privateUser)
                        .then(function(privateUsersObj) {
                            var promises = [];
                            _.each(privateUsersObj, function(privateUserObj) {
                                var Following = Parse.Object.extend("Following");
                                var following = new Following();
                                following.set("user", orgUserObj);
                                following.set("subscriber", privateUserObj);
                                promises.push(following.save());
                            });
                            return Parse.Promise.when(promises);
                        });
                });
            });
            return promise;
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// following section end _________________________________________________________________


// one-time run script
Parse.Cloud.define("resetUserTypeToQuizlings", function(request, response) {
    Parse.Cloud.useMasterKey();
    var _ = require("underscore.js");
    var query = new Parse.Query("Quizling");
    query.equalTo("userType", undefined);
    query.include("owner");
    lib.findAll(query)
        .then(function(quizlings) {
            var userType = "";
            var promises = [];
            _.each(quizlings, function(quizling) {
                if(quizling.get("owner") && quizling.get("owner").get("type")) {
                    userType = quizling.get("owner").get("type");
                } else {
                    userType = "deleted";
                }
                quizling.set("userType", userType);
                promises.push(quizling.save());
            });
            return Parse.Promise.when(promises);
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// one-time run script
Parse.Cloud.define("setDefaultBestGame", function(request, response) {
    var bestGame = new Parse.Query("Game");
    bestGame.equalTo("best", undefined);
    lib.findAll(bestGame)
        .then(function(games) {
            if (games.length == 0) {
                return Parse.Promise.as("all games was changed");
            }
            var promises = [];
            _.each(games, function(game) {
                game.set("best", false);
                promises.push(game.save());
            });
            return Parse.Promise.when(promises);
        })
        .then(
        function (result) {
            return response.success(result);
        },
        function (error) {
            return response.error(error);
        });
});

// one-time run script
Parse.Cloud.job("recountBestGames", function(request, response) {
    var iterations = 1000;
    manager.setBestGames(iterations)
        .then(
        function () {
            return response.success("games recounted");
        },
        function (error) {
            return response.error(error.message);
        });
});

Parse.Cloud.beforeSave("QuestionPersonalStatistics", function(request, response) {
    Parse.Cloud.useMasterKey();
    var obj = request.object;
    var query = new Parse.Query("Quizling");
    query.equalTo("objectId", obj.get("quizling").id);
    return query.first()
        .then(function(quizling) {
            if (quizling && (quizling.get("quizlingOwner") != undefined) && (_.has(quizling, "owner"))) {
                var owner = statistic.get("owner");
                statistic.set("quizlingOwner", owner.id);
                obj.set("quizlingOwner", owner.id);
            }
            return;
        }).then(function() {
            response.success();
            return;
        })
});

// one-time run script
Parse.Cloud.job("addOwnerToQuestionPersonalStatistics", function(request, response) {
    Parse.Cloud.useMasterKey();
    var promises = [];
    var owner;
    var quizling;
    var query = new Parse.Query("QuestionPersonalStatistics");
    query.include("quizling");
    query.equalTo("quizlingOwner", undefined);
    query.limit(500);
    query.find().then(
        function (statistics) {
            if (statistics.length == 0) {
                return Parse.promise.as({message: "all statistics recounted"})
            }
            _.each(statistics, function(statistic) {
                if (statistic.get("quizling") && statistic.get("quizling").get("owner")) {
                    statistic.set("quizlingOwner", statistic.get("quizling").get("owner").id);
                } else {
                    statistic.set("quizlingOwner", "not found");
                }
                promises.push(statistic.save());
            });
            return Parse.Promise.when(promises);
        },
        function (error) {
            return response.error(error.message);
        })
        .then(
        function (success) {
            return response.success(success.message || "end");
        },
        function (error) {
            return response.error(error.message);
        }
    )
});

Parse.Cloud.job("addOwnerToGame", function(request, response) {
    Parse.Cloud.useMasterKey();
    var promises = [];
    var owner;
    var quizling;
    var query = new Parse.Query("Game");
    query.include("quizling");
    query.equalTo("quizlingOwner", undefined);
    query.limit(500);
    query.find().then(
        function (statistics) {
            if (statistics.length == 0) {
                return Parse.Promise.as({message: "all games recounted"})
            }
            _.each(statistics, function(statistic) {
                if (statistic.get("quizling") && statistic.get("quizling").get("owner")) {
                    statistic.set("quizlingOwner", statistic.get("quizling").get("owner").id);
                } else {
                    statistic.set("quizlingOwner", "not found");
                }
                promises.push(statistic.save());
            });
            return Parse.Promise.when(promises);
        },
        function (error) {
            return response.error(error.message);
        }).then(
        function (success) {
            return response.success(success.message || "end");
        },
        function (error) {
            return response.error(error.message);
        }
    )
});
