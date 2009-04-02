<td id="named-date-cell-{{ date.id }}">
	<span id="named-date-{{ date.id}}">{{ date.name }} / {{ date.date|date:"Y-m-j" }}</span>
	<form id="named-date-edit-form-{{ date.id }}" class="named-date-edit-form" action="." method="post">
		{% for field in date.edit_form %}
			{{ field }}
		{% endfor %}
		<input type="submit" value="save" />
	</form>
</td>
<td id="named-date-controls-{{ date.id }}">
{% if can_edit_dates %}
	<span class="hover-td">
		[<a href="." onclick="editNamedDate({{ date.id }}); return false;">edit</a>]
		[<a href="." onclick="deleteNamedDate({{ date.id }}); return false;">delete</a>]
	</span>
{% endif %}
</td>
