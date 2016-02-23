/*
* This is the format we want to use to display student-score charts
* @author kkim110, shauk2
* @iteration 2
*/

google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(buildBarGraph);

var fetched_json;

/**
* @description This chunk of code shall run first, fetching and saving
* the data from the database in a global variable.
*
*/
$(document).ready(
	function fetchData(){
		$.ajax({
			url: "testing",
			method: "POST",
			dataType: "Text",
			data: "stuff",
		}).done(function(data) {
        fetched_json = data;
			  // buildBarGraph( data );
		});
	}
);

/**
* @description Used for basic testing, to check validity of data from Jasmine.js
*/
function getFetchedData() {
	return fetched_json;
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
function buildBarGraph(jobj) {

  // alert("data in buildBarGraph is: " + jobj);
  // alert("fetched_json is: " + fetched_json);//[0]["name"]);

	// fetched_json = fetched_json.replace(/'/, '"').replace(/'/, '"')

	// alert(fetched_json)

	// fetched_json = JSON.parse(fetched_json.result[0])

	// obj = eval(fetched_json);
	// fetched_json = JSON.parse({fetched_json})

	// fetched_json = JSON.parse(fetched_json);

	// var result = '{"time": 3, "_id": {"$oid": "56cbadf81bad1a44954a2575"}, "type": "quiz_result", "score": 99, "name": "testQuizName3"}', '{"time": 2, "_id": {"$oid": "56cbadf81bad1a44954a2574"}, "type": "quiz_result", "score": 80, "name": "testQuizName2"}', '{"time": 1, "_id": {"$oid": "56cbadf81bad1a44954a2573"}, "type": "quiz_result", "score": 90, "name": "testQuizName1"}'

	// var jresult = JSON.parse(result);

	// alert("result is " + result);

	// alert("fetched_json[0]: " + fetched_json[0]);

	var jstring = "{\'name\':\'testQuizName1\',\'score\':90,\'type\':\'quiz_result\',\'time\':1}";

	var jstring3 = '{"name":"testQuizName1","score":90,"type":"quiz_result","time":1}';

	jstring3 = JSON.parse(jstring3);

	// alert("jstring3 is " + jstring3.name);


	// JSON.parse(jstring);
	// alert(jstring);

  // for(var i = 0; i < fetched_json.length; i++) {
  //   alert(fetched_json[i].name)
  // }

  var test_json = [{
    "student": "Adam",
    "score": 100
  },
  {
    "student": "Brian",
    "score": 95
  }]

  var data = new google.visualization.arrayToDataTable([
    ['Quiz', 'Percentage'],
    [test_json[0].student, test_json[0].score],
    [test_json[1].student, test_json[1].score],
    [test_json[0].student, test_json[0].score]
  ]);

  var options = {
    title: 'Peformance History',
    width: 350,
    height: 300,
    legend: { position: 'none' },
    chart: { subtitle: 'scores by percentage' }
  };

  var chart2 = new google.charts.Bar(document.getElementById('top_x_div'));
  // Convert the Classic options to Material options.
  chart2.draw(data, google.charts.Bar.convertOptions(options));
};

function riyadSpike() {
  var x = document.forms["chartBuilder"]["x-axis"].value;
  var y = document.forms["chartBuilder"]["y-axis"].value;
  alert("x-axis is: " + x + ", y-axis is: " + y);
  return false;
}
