{% load listtags %}
{% if not hide_title %}<h3><a href="{{ artist_group.get_absolute_url }}">{{ artist_group.name }}</a></h3>{% endif %}
<table>
	<tr>
		<th>members:</th>
		<td>
			{% for artist in artist_group.artists.all %}<a href="{{ artist.get_profile.get_absolute_url }}">{{ artist.get_profile.display_name }}</a>{% loop_comma %}{% endfor %}
		</td>
	</tr>
	{% if artist_group.url %}
	<tr>
		<th>url:</th>
		<td>
			<a href="{{ artist_group.url }}">{{ artist_group.url }}</a>
		</td>
	</tr>
	{% endif %}
	{% if artist_group.installation_set.all %}
	<tr>
		<th>artwork:</th>
		<td>
			{% for installation in artist_group.installation_set.all %}
			<a href="{{ installation.get_absolute_url }}">{{ installation.name }}</a>{% loop_comma %}
			{% endfor %}
		</td>
	</tr>
	{% endif %}
</table>

