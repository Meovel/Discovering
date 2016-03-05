$(".follow-button").click(function(){
	alert($(this).attr("id"));
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