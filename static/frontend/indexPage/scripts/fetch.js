alert("hello");
$(document).ready(
	function sendAJAX(){
	$.ajax({
		method: 'POST',
		url: 'testing',
		context: document.body,
		data: 'hello'
	});
);
