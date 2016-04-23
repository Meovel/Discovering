var username;
var target_id;
var numOfLikes;

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
	var organizationId = target_id;
	var path = "/follow/" + target_id;

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


//like
$("#like-image").click(function(){
	alert($(this).attr("src"));
	var path = "";

	// click to unlike
	if($(this).attr("src") == "../static/images/like.jpg"){
		$(this).attr("src", "../static/images/unlike.jpg");
		path = "/unlike/" + target_id
		$.getJSON(path, function(data){
				if(data.result == "OK"){
					numOfLikes--;
					$("#likes").text(numOfLikes)
			}
		});
	}
	// click to like
	else{
		path = "/like/" + target_id;
		$(this).attr("src", "../static/images/like.jpg");
		$.getJSON(path, function(data){
				if(data.result == "OK"){
					numOfLikes++;
					$("#likes").text(numOfLikes)
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
	var path = "/comment/" + target_id;
	$.getJSON(path, {
		content: content,
		poster: username
	}, function(data){
		if(data.result == "OK"){
			var html = "<div class='comment'>" + 
			"<p class='normal-text'>" + content + "</p>" + 
			"<p class='sub-text'>By: " + username + "</p>" +
			"</div>";
			$("#comments").prepend(html);
			$("#post-comment").fadeOut();
			$("#comments").fadeIn();
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



$("#quizzes-wrapper a").click(function(){
	event.preventDefault();

	path = "/quiz_information/" + $(this).attr("id");
	// send data to server using ajax
	 $.ajax({
            url: path,
            type: 'GET',
            success: function(response) {
            	if(response.result == "Failed"){
            		var html = "<h1>No one has taken this quiz yet!</h1>";
            		$("#quiz-detail").html(html);
            	}
            	else{
            		$("#quiz-detail").html(response);
            	}
            },
            error: function(error) {
                console.log(error);
            }
     });
});
