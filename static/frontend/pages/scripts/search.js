
$(document).ready(function(){
		$( "#filter" ).change(function () {
			var val = $( "#filter option:selected" ).attr("value");
			$.ajax({
				url: "/filterArea",
				method: "POST",
				dataType: "Text",
				data: val
			}).done(function(data){
				document.write(data);
			});
		});
	}
);
