$(document).ready(function () {
	$(".dropdown-menu").on("click","a",function(){
		if($(this).attr("id") === "markAsRead"){
			var array = [];
			$("tbody#messageList > tr").each(function(){
				if($(this).find("#checkBox").parent().attr("class")==="checked"){
					array.push($(this).attr("data-messageid"));
					//alert($(this).attr("data-messageid"))
				}
			});
			var jobj = {"result":array};
			$.ajax({
					url: "/inbox/markasread",
					method: "POST",
					dataType: "Text",
					data: JSON.stringify(jobj)
			}).done(function (data) {
					for (m in array) {
						document.getElementById(array[m]).className = ""
					}
			});
		}else if($(this).attr("id") === "delete"){
			var array = [];
			$("tbody#messageList > tr").each(function(){
				if($(this).find("#checkBox").parent().attr("class")==="checked"){
					array.push($(this).attr("data-messageid"));
					//alert($(this).attr("data-messageid"))
				}
			});
			var jobj = {"result":array};
			$.ajax({
					url: "/inbox/delete",
					method: "POST",
					dataType: "Text",
					data: JSON.stringify(jobj)
			}).done(function (data) {
					for (m in array) {
						document.getElementById(array[m]).innerHTML = ""
					}
			});
		}
	});
	
})