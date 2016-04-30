/*
* This is the format we want to use to display student-score charts
* @author kkim110, shauk2
* @iteration 2
*/

// var $ = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js";
Parse.initialize("1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD", "kRyIxZkeC08jvlwSwbUdmBysWL9j6bLi0lB9RUan");

/**
* @description Initializes the Google Charts API object, so that chart can be drawn
*/
function initializeGoogleCharts(array, divId) {
	google.charts.load('current', {'packages':['bar']});
	google.charts.setOnLoadCallback(queryToChart);

}
initializeGoogleCharts([], "top_x_div");

// template-code taken from the docs: https://parse.com/docs/js/guide#queries
/**
* @description Queries Parse database for relevent data
* @summary Calls a method to build the graph, sending an Array of JSON objects
* @param str – should relevant parameterization for queryToChart to correctly handle
* @TODO Generalize queryToChart to extract relevant data based on its input parameter
*/
function queryToChart(obj_id, str) {
	console.log("queryToChart str is: " + str)

	var obj = document.getElementById('obj_id').getAttribute('objectId');
	obj = obj.replace(/\<a\>/,'');
	obj = obj.replace(/\<\/a\>/,'');
	console.log('obj: ' + obj);

	var data_array = []
	console.log("In queryToChart")
	var ChartData = Parse.Object.extend("QuizPersonalStatistics");
	var UserData = Parse.Object.extend("User");
	var query = new Parse.Query(ChartData);

	// "WrWZRnIDbv"
	var user_dev10_objectId = obj;
	query.equalTo("user", {
        __type: "Pointer",
        className: "_User",
        objectId: user_dev10_objectId
    });
	query.limit(100);
	query.include("user");
	query.include("quizling");
	query.find({
	  success: function(results) {
	    // alert("Successfully retrieved " + results.length + " entries.");
			console.log(results)
			// Do something with the returned Parse.Object values
	    for (var i = 0; i < results.length; i++) {
	      var object = results[i];
				if(object.get('quizling') == null) continue
				data_array.push({user: object.get('user').get('username'), quizling: object.get('quizling').get('name'), averageScore: object.get('averageScore')})
				var myUser = object.get('user')
	      console.log(object.id + ' - ' + object.get('averageScore') + ' - ' + (object.get('user')).get('username') ) ;
	    }
			console.log(data_array)
			buildBarGraph(data_array, "quizling", "averageScore")
			console.log("hello, this is the line after calling buildBarGraph in queryToChart")
			return data_array // simply for front-end testing
	  },
	  error: function(error) {
	    alert("Error: " + error.code + " " + error.message);
	  }
	});
}

/**
* @description This should simply build the bar graph (i.e. of student-score data)
* @param json_array – This should be passed in from the database
* @TODO Consider creating a generalized graph-builder wrapper
*/
function buildBarGraph(json_array, key1, key2, divId) {

	divId = "chart_div"

	var charts_array = []
	charts_array.push(['Quiz', 'Score'])
	for(var i = 0; i < json_array.length; i++) {
		charts_array.push(
			[json_array[i][key1.toString()], json_array[i][key2.toString()]]
		)
	}

	var data = new google.visualization.arrayToDataTable(charts_array);

  var options = {
    title: 'Peformance History',
    width: 350,
    height: 300,
    legend: { position: 'none' },
    chart: { subtitle: 'scores by points' }
  };

	var divBlah = "top_x_div"
  var chart2 = new google.charts.Bar(document.getElementById(divBlah.toString()))//getElementById(divId.toString()));
  // Convert the Classic options to Material options.
  chart2.draw(data, google.charts.Bar.convertOptions(options));
	var chart3 = new google.charts.Bar(document.getElementById(divId.toString()))
  chart3.draw(data, google.charts.Bar.convertOptions(options));
};

/**
* @description This is simply a spike solution to retrieve/display some values
* taken from the form.
*/
function riyadSpike() {
  var x = document.forms["chartBuilder"]["x-axis"].value;
  var y = document.forms["chartBuilder"]["y-axis"].value;
  // alert("x-axis is: " + x + ", y-axis is: " + y);
  return false;
}
