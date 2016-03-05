/*
* This is the format we want to use to display student-score charts
* @author kkim110, shauk2
* @iteration 2
* This file is an example fetching file, but we just put this fetch in charts.js
* for the time being, and to keep things simple.
*/

$(document).ready(
	function(){
		$.ajax({
			url: "testing",
			method: "POST",
			dataType: "Text",
			data: "stuff",
		}).done(function(data) {
			  // alert( data );
				// loadScript("charts.js", buildBarGraph(data));
				loadScript("charts.js", queryToChart());
		});
	}
);
