function quizListToHTML(jobj){
	var qList = jobj["data"];
	var resultHTML= '';
	var rowTag = '<div class="row">';
	var rowTagEnd = '</div>';
	for(i=0;i<qList.length;i++){
		var htmlString = '<div class="col-md-4"><div class="portlet light"><div class="portlet-title"><div class="caption font-purple-plum"><img class="organization_avatar" src="./../static/organizations/book.png"><span class="caption-subject bold uppercase">';
		htmlString = htmlString+qList[i]['name']+'</span></div></div><div class="portlet-body"><div id="context" data-toggle="context" data-target="#context-menu"><p>';
		var endString = '</p></div></div><div style="height:25px; margin-top:25px"><a class="button" style="float:left">Follow</a><a class="button" style="float:right">Quiz</a></div></div><!-- END PORTLET--></div>';
		htmlString = htmlString + qList[i]['summary'] + endString;
		if(i%3 === 0){
			htmlString = rowTag + htmlString;
		}else if(i%3 === 2 || qList.length-1 === i){
			htmlString = htmlString + rowTagEnd;
		}
		resultHTML = resultHTML + htmlString;
	}
	return resultHTML
}


$(document).ready(function(){
		$( "#filter" ).change(function () {
			var val = $( "#filter option:selected" ).attr("value");
			$.ajax({
				url: "/filterArea",
				method: "POST",
				dataType: "Text",
				data: val
			}).done(function(data){
				$("#quizList").html(quizListToHTML(JSON.parse(data)));
			});
		});
		$( "#filter-age" ).change(function () {
			var val = $( "#filter-age option:selected" ).attr("value");
			$.ajax({
				url: "/filterAge",
				method: "POST",
				dataType: "Text",
				data: val
			}).done(function(data){
				$("#quizList").html(quizListToHTML(JSON.parse(data)));
			});
		});
	}
);

