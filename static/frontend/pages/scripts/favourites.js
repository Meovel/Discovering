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
			document.getElementById(orgId).innerText = "Unfollowed"
			document.getElementById(orgId).className = "pull-right btn btn-sm btn-circle haze unfollow"
		});
	});
	$("#follower").on("click","button",function(){
		var usrId = $(this).attr("id");

		$.ajax({
			url: "/deleteFollower/"+usrId,
			method: "POST",
		}).done(function (data) {
			document.getElementById(usrId).innerText = "Deleted"
			document.getElementById(usrId).className = "pull-right btn btn-sm btn-circle haze delete"
		});
	});
});