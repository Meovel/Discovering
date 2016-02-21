/*
* This is the format we want to use to display student-score charts
* @author kkim110_shauk2
* @iteration 2
*/
google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(buildBarGraph);

/**
* @description This should simply build the bar graph (i.e. of student-score data)
* @param json – This should be passed in from the database
* @TODO Hook this up to the database (i.e. Mongo)
* @TODO Hook this up to the front-end HTML form via GET/POST
*/
function buildBarGraph(jobj) {
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
