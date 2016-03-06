$(".follow-btn").click(function(){
	event.preventDefault();

	var followBtn = $(this);
	var organizationId = $(this).attr("id");
	var path = "/follow/" + organizationId;

	if(followBtn.hasClass("follow-btn")){
		$.getJSON(path,{
			type: "follow"
			}, function(data){
				if(data.result == "success"){
					followBtn.removeClass("follow-btn");
					followBtn.addClass("cancel-btn");
					followBtn.html("<i class=\"fa fa-minus\"></i> Cancel");
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
					followBtn.html("<i class=\"fa fa-plus\"></i> Follow");
			}
		});
	}
});


$('a[href^="#"]').on('click',function (e) {
	    e.preventDefault();

	    var target = this.hash;
	    var $target = $(target);

	    $('html, body').stop().animate({
	        'scrollTop': $target.offset().top
	    }, 500, 'swing', function () {
	        window.location.hash = target;
	    });
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