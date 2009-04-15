{% if can_edit_dates %}
<div id="add-named-date">
	<div style="position: absolute; right: 5px; top: 5px;">[<a href="." onclick="hideAddNamedDateForm(); return false;">close</a>]</div>
	<h4>Add a date:</h4>
	<table>
	<tr>
		<form id="dated_name_form" action="." method="post">
			{% for field in named_date_form %}
				<td>{{ field }}</td>
			{% endfor %}
			<td><input type="hidden" name="named-date-form" value="true" />&nbsp;&nbsp;<input type="submit" value="add date" /></td>
		</form>
	</tr>
	</table>
	<div style="text-align: center; width: 400px;">
		<b>or</b><br/>
		<h4>Choose a recent date:</h4>
		<form action="." method="post">
		<table>
			{% for recent_date in recent_dates.all|slice:":10" %}
			<tr><td><input type="checkbox" name="recent_dates" value="{{ recent_date.id }}"/>{{ recent_date.name }} / {{ recent_date.date }}</td></tr>
			{% endfor %}
			<tr><td><input type="hidden" name="named-date-form" value="true" /><input type="submit" value="add dates" /></td></tr>
		</table>
		</form>

	</div>
</div>
{% endif %}