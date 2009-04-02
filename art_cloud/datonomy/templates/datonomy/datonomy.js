
var recentDates = new Array();
{% for date in recent_dates %}
recentDates[recentDates.length] = { "name":"{{ date.name}}", "date":"{{ date.date }}", "id": "{{ date.id }}" };
{% endfor %}

function datonomyInitialize(){
	$("#add-named-date").hide();
	$(".named-date-edit-form").hide();
}
$(document).ready(function() { datonomyInitialize(); });


function editNamedDate(namedDateID) {
	$("#named-date-" + namedDateID).hide();
	$("#named-date-controls-" + namedDateID).hide();
	$("#named-date-edit-form-" + namedDateID).show();
}

function deleteNamedDate(namedDateID) {
	document.location.href = '/datonomy/date/' + namedDateID + '/?action=delete';
}

function hideRecentDatesPopup(){
	var element = document.getElementById("recent-dates-popup");
	if(element){
		element.style.visibility = "hidden";
	}
}

function showRecentDatesPopup(){
	var popup = document.getElementById("recent-dates-popup");
	if(popup){
		popup.style.visibility = "visible";
		return;
	}
	
	var html = '<h1>Add Recent Dates:</h1>';
	html += '<div id="recent-dates-links">[<a href="." onclick="hideRecentDatesPopup(); return false;">close</a>]</div>';
	html += '<form action="." method="post">';
	for(var i=0; i < recentDates.length; i++){
		html += '<input type="checkbox" name="recent_dates" value="' + recentDates[i].id + '"/> ' + recentDates[i].name + ': ' + recentDates[i].date + '<br />';
	}
	html += '<br /><input type="submit" value="add dates" />'
	html += '</form>';

	var pulldown = document.createElement('div');
	pulldown.setAttribute('id', 'recent-dates-popup');
	pulldown.innerHTML = html;
	document.body.appendChild(pulldown);
}

function findPos(obj) {
	var curleft = curtop = 0;
	if (obj.offsetParent) {
		curleft = obj.offsetLeft
		curtop = obj.offsetTop
		while (obj = obj.offsetParent) {
			curleft += obj.offsetLeft
			curtop += obj.offsetTop
		}
	}
	return [curleft,curtop];
}