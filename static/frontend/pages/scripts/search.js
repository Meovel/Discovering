
$(document).ready(function(){
		$( "#filter" ).change(function () {
			var val = $( "#filter option:selected" ).attr("value");
			alert(val);
			$.ajax({
				url: "/filterArea",
				method: "POST",
				dataType: "Text",
				data: val
			}).done(function(data) {
				
			});
		});
	}
);
