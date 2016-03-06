/*
* This is the format we want to use to display student-score charts
* @author kkim110, shauk2
* @iteration 2
*/

Parse.initialize("1piMFdtgp0tO1LPHXsSOG7uBGiDiuXTUAN91g7VD", "kRyIxZkeC08jvlwSwbUdmBysWL9j6bLi0lB9RUan");


function initializeGoogleCharts(array, divId) {
	google.charts.load('current', {'packages':['bar']});
	// google.charts.setOnLoadCallback(buildBarGraph([], divId));
	google.charts.setOnLoadCallback(queryToChart);
}
initializeGoogleCharts([], "top_x_div");

// template-code taken from the docs: https://parse.com/docs/js/guide#queries
function queryToChart(str) {
	console.log("queryToChart str is: " + str)
	var data_array = []
	console.log("In queryToChart")
	var ChartData = Parse.Object.extend("QuizPersonalStatistics");
	//var ChartData = Parse.Object.extend("LearningAreas");
	var UserData = Parse.Object.extend("User");
	var query = new Parse.Query(ChartData);

	var user_dev10_objectId = "WrWZRnIDbv"
	// query.equalTo("user", user_dev10_objectId)
	query.equalTo("user", {
        __type: "Pointer",
        className: "_User",
        objectId: user_dev10_objectId
    });
	query.limit(100);
	query.include("user");
	query.include("quizling");
	// query.equalTo("objectId", "95aSXQ3xMo")
	// query.equalTo("objectId", {
	// 	"__type": "Pointer",
	// 	"className": "ChartData",
	// 	"objectId": "WrWZRnIDbv"
	// });
	query.find({
	  success: function(results) {
	    alert("Successfully retrieved " + results.length + " entries.");
			console.log(results)
			// Do something with the returned Parse.Object values
	    for (var i = 0; i < results.length; i++) {
	      var object = results[i];
				data_array.push({user: object.get('user'), quizling: object.get('quizling'), averageScore: object.get('averageScore')})
				var myUser = object.get('user')
	      console.log(object.id + ' - ' + object.get('averageScore') + ' - ' + (object.get('user')).get('username') ) ;
	    }
			console.log(data_array)
			buildBarGraph(data_array)
	  },
	  error: function(error) {
	    alert("Error: " + error.code + " " + error.message);
	  }
	});
}

/**
* from http://stackoverflow.com/questions/9036429/convert-object-string-to-json
*/
function JSONize(str) {
  return str
    // wrap keys without quote with valid double quote
    .replace(/([\$\w]+)\s*:/g, function(_, $1){return '"'+$1+'":'})
    // replacing single quote wrapped ones to double quote
    .replace(/'([^']+)'/g, function(_, $1){return '"'+$1+'"'})
}

/**
* @description This should simply build the bar graph (i.e. of student-score data)
* @param json – This should be passed in from the database
* @TODO Hook this up to the database (i.e. Mongo)
* @TODO Hook this up to the front-end HTML form via GET/POST
*/
function buildBarGraph(json, key1, key2, divId) {

	// queryToChart()

	console.log("json is: " + json)

  var test_json = [{
    "student": "Adam",
    "score": 100
  },
  {
    "student": "Brian",
    "score": 95
  }]

	key1 = "student"
	key2 = "score"

  var data = new google.visualization.arrayToDataTable([
    ['Quiz', 'Percentage'],
    [test_json[0][key1.toString()], test_json[0][key2.toString()]],
    [test_json[1][key1.toString()], test_json[1][key2.toString()]],
    [test_json[0][key1.toString()], test_json[0][key2.toString()]]
  ]);

  var options = {
    title: 'Peformance History',
    width: 350,
    height: 300,
    legend: { position: 'none' },
    chart: { subtitle: 'scores by percentage' }
  };

	var divBlah = "top_x_div"
  var chart2 = new google.charts.Bar(document.getElementById(divBlah.toString()))//getElementById(divId.toString()));
  // Convert the Classic options to Material options.
  chart2.draw(data, google.charts.Bar.convertOptions(options));
	var chart3 = new google.charts.Bar(document.getElementById("chart_div"))//getElementById(divId.toString()));
  chart3.draw(data, google.charts.Bar.convertOptions(options));
};

function riyadSpike() {
  var x = document.forms["chartBuilder"]["x-axis"].value;
  var y = document.forms["chartBuilder"]["y-axis"].value;
  alert("x-axis is: " + x + ", y-axis is: " + y);
  return false;
}
