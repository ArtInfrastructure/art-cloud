
var recentDates = new Array();
{% for date in recent_dates %}
recentDates[recentDates.length] = { "name":"{{ date.name}}", "date":"{{ date.date }}" };
{% endfor %}

function deleteNamedDate(namedDateID) {
	document.location.href = '/datonomy/date/' + namedDateID + '/?action=delete';
}

function showRecentDatesPulldown(targetID){
	var element = document.getElementById(targetID);
	var html = '<ul id="recent-dates-pulldown">';
	for(var i=0; i < recentDates.length; i++){
		html += '<li>' + recentDates[i].name + '</li>';
	}
	html += '</ul>'
	var pulldown = document.createElement('div');
	pulldown.innerHTML = html;
	element.appendChild(pulldown);
}