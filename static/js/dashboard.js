var username;
var user_id;

$(".org-card-image-wrapper a").mouseenter(function(){
	// show blur and text
	$(this).children().eq(1).fadeIn();
	$(this).children().eq(2).fadeIn();
});

$(".org-card-image-wrapper a").mouseleave(function(){
	// show blur and text
	$(this).children().eq(1).fadeOut();
	$(this).children().eq(2).fadeOut();
});

$(".follow-btn").click(function(){
	event.preventDefault();

	var followBtn = $(this);
	var organizationId = user_id;
	var path = "/follow/" + user_id;

	if(followBtn.hasClass("follow-btn")){
		$.getJSON(path,{
			type: "follow"
			}, function(data){
				if(data.result == "success"){
					followBtn.removeClass("follow-btn");
					followBtn.addClass("cancel-btn");
					followBtn.html("UnFollow");
			}
		});
	}

	else if(followBtn.hasClass("cancel-btn")){
		$.getJSON(path,{
			type: "cancel"
			}, function(data){
				if(data.result == "success"){
					followBtn.removeClass("follow-btn");
					followBtn.addClass("cancel-btn");
					followBtn.html("Follow");
			}
		});
	}
});


// post comment
$("#make-comment").click(function(){
	$("#post-comment").fadeIn();
	$("#comments").fadeOut();
});


$("#post-comment-btn").click(function(){
	var content = $("#comment-content").val();
	var path = "/comment/" + user_id;
	$.getJSON(path, {
		content: content,
		poster: username
	}, function(data){
		if(data.result == "OK"){
			var html = "<div class='comment'>" + 
			"<p>" + content + "</p>" + 
			"<p>By: " + username + "<p>" +
			"</div>";
			$("#comments").prepend(html);
		}
	});
});

$("#back-btn").click(function(){
	$("#post-comment").fadeOut();
	$("#comments").fadeIn();
});


$(".organization-card").click(function(){
	var name = $(this).attr("id");
	var path = '/quiz/dev10';
	
	$.getJSON(path).done(function(data){
		quizzes = data.result;

		var innerHtml = "";
		// change the layout of html
		jQuery.each(quizzes, function(i, val) {
  			innerHtml += "<a href='#' onclick=\"updateQuizDetail('" + i + "')\" id='" + i + "'><p>" + val.name + "</p></a>\n"
		});

		$("#quizzes-list").html(innerHtml);
    });
});


$(".quiz-item").click(function(){
	event.preventDefault();

	alert("hello");

	var quizId = $(this).attr("id");
	var quiz = quizzes[quizId];

	var summary = quiz.summary;
	if(summary == "") summary = "This quiz has no summary currently";
	$("#quiz-description").text(quiz.summary);
});

function updateQuizDetail(quizId){
	event.preventDefault();

	var quiz = quizzes[quizId];

	var summary = quiz.summary;
	if(summary == "") summary = "This quiz has no summary currently";

	console.log(summary);

	$("#quiz-description").text(summary);
}