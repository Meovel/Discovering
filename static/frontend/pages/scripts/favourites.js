$(document).ready(function () {
	$("#following").on("click","button",function(){
		var orgId = $(this).attr("id");
		var jobj = {"type":"cancel"};
		$.ajax({
			url: "/follow/"+orgId,
			method: "POST",
			dataType: "Text",
			data: JSON.stringify(jobj)
		}).done(function (data) {
			alert("done");
		});
	});
	$("#follower").on("click","button",function(){
		var usrId = $(this).attr("id");

		$.ajax({
			url: "/deleteFollower/"+usrId,
			method: "POST",
		}).done(function (data) {
			alert(data);
		});
	});
});