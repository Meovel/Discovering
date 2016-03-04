
$(document).ready(
 	function(){
 		$.ajax({
 			url: "filterArea",
 			method: "GET",
 			dataType: "Text",
 			data: "stuff",
 		}).done(function(data) {
 			alert("sent data");
 		});
 	}
);
