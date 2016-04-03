function quizListToHTML(jobj) {
    var qList = jobj["data"];
    var resultHTML = '';
    var rowTag = '<div class="row">';
    var rowTagEnd = '</div>';
    for (i = 0; i < qList.length; i++) {
        var htmlString = '<div class="col-md-4"><div class="portlet light"><div class="portlet-title"><div class="caption font-purple-plum"><img class="organization_avatar" src="./../static/organizations/book.png"><span class="caption-subject bold uppercase">';
        htmlString = htmlString + qList[i]["name"] + '</span></div></div><div class="portlet-body"><div id="context" data-toggle="context" data-target="#context-menu"><p><span class="creator">Creator</span>: ';
        htmlString = htmlString + qList[i]["owner"] + '</p><p><span>Plays: ';
        htmlString = htmlString + qList[i]["questionCount"] + '</span><span style="float: right">Avg: ';
        htmlString = htmlString + qList[i]["avgScore"] + '</span></p><hr/><p>';
        if (qList[i].hasOwnProperty("summary") && !(qList[i]["summary"] === "")) {
            htmlString = htmlString + qList[i]["summary"];
        } else {
            htmlString = htmlString + "Description";
        }
        htmlString = htmlString + '</p></div></div><div class="playButton"><a href="http://webplay.quizlingapp.com/app#/quizzes/';
        htmlString = htmlString + qList[i]["id"] + '" style="text-decoration: none;"><button class="btn blue btn-block">Play</button></a></div></div></div>';
        //var htmlString = '<div class="col-md-4"><div class="portlet light"><div class="portlet-title"><div class="caption font-purple-plum"><img class="organization_avatar" src="./../static/organizations/book.png"><span class="caption-subject bold uppercase">';
        //htmlString = htmlString+qList[i]['name']+'</span></div></div><div class="portlet-body"><div id="context" data-toggle="context" data-target="#context-menu"><p>';
        //var endString = '</p></div></div><div style="height:25px; margin-top:25px"><a class="button" style="float:left">Follow</a><a class="button" style="float:right">Quiz</a></div></div><!-- END PORTLET--></div>';
        //htmlString = htmlString + qList[i]['summary'] + endString;
        if (i % 3 === 0) {
            htmlString = rowTag + htmlString;
        } else if (i % 3 === 2 || qList.length - 1 === i) {
            htmlString = htmlString + rowTagEnd;
        }
        resultHTML = resultHTML + htmlString;
    }
    return resultHTML
}


$(document).ready(function () {
        $(".followBtn").click(function () {
            var userId = $(this).attr("data-value");
            var path = "/follow/" + userId;
            var btn = document.getElementById(userId);
            var type = "follow";
            if (btn.innerText == "UNFOLLOW") {
                type = "cancel";
            }
            $.getJSON(path, {
                type: type
            }, function (data) {
                if (btn.innerText == "FOLLOW") {
                    btn.innerText = "Unfollow";
                    btn.className = "btn red btn-block followBtn"
                } else {
                    btn.innerText = "Follow";
                    btn.className = "btn green btn-block followBtn"
                }
            });

        });
        $("#areaFilter").children(".dropdown-menu").children(".submit").click(function () {
            var name = $(this).children().html();
            $("#areaFilter").children("#dropDownDisplay").html(name);
            $.ajax({
                url: "/filterArea",
                method: "POST",
                dataType: "Text",
                data: val
            }).done(function (data) {
                $("#quizList").html(quizListToHTML(JSON.parse(data)));
            });
        });
        $("#ageFilter").children(".dropdown-menu").children(".submit").click(function () {
            var val = $(this).attr("data-value");
            var name = $(this).children().html();
            $("#ageFilter").children("#dropDownDisplay").html(name);
            $.ajax({
                url: "/filterAge",
                method: "POST",
                dataType: "Text",
                data: val
            }).done(function (data) {
                $("#quizList").html(quizListToHTML(JSON.parse(data)));
            });
        });
        $("#sortResult").children(".dropdown-menu").children(".submit").click(function () {
            var requestJSON = {};
            var arrow = $(this).parent().siblings("#sortArrow").children("i");
            var className = arrow.attr("class");
            if (className.indexOf("fa-angle-down") >= 0) {
                requestJSON["order"] = "ascending";
            } else {
                requestJSON["order"] = "descending";
            }
            var val = $(this).attr("data-value");
            requestJSON["field"] = val;
            var name = $(this).children().html();
            $("#sortResult").children("#dropDownDisplay").html(name);
            $("#sortResult").children("#dropDownDisplay").attr("data-value", val);
            $.ajax({
                url: "/sortQuizzes",
                method: "POST",
                dataType: "Text",
                data: JSON.stringify(requestJSON)
            }).done(function (data) {
                $("#quizList").html(quizListToHTML(JSON.parse(data)));
            });
        });
        $("#sortResult").children("#dropDownDisplay").click(function () {
            var requestJSON = {};
            var arrow = $(this).siblings("#sortArrow").children("i");
            var className = arrow.attr("class");
            if (className.indexOf("fa-angle-down") >= 0) {
                arrow.removeClass("fa fa-angle-down");
                arrow.addClass("fa fa-angle-up");
                requestJSON["order"] = "descending";
            } else {
                arrow.removeClass("fa fa-angle-up");
                arrow.addClass("fa fa-angle-down");
                requestJSON["order"] = "ascending";
            }
            var val = $(this).attr("data-value");
            requestJSON["field"] = val;
            $.ajax({
                url: "/sortQuizzes",
                method: "POST",
                dataType: "Text",
                data: JSON.stringify(requestJSON)
            }).done(function (data) {
                $("#quizList").html(quizListToHTML(JSON.parse(data)));
            });
        });
    }
);

