$(document).ready(
	function(){
		$.ajax({
			url: "testing",
			method: "POST",
			dataType: "Text",
			data: "stuff",
		}).done(function(data) {
			  alert( data );
		});
	}
);

