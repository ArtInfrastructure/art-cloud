{% load listtags %}
{% load imagetags %}
<div class="artist-item {% cycle 'even-row' 'odd-row' %}">
	{% if not hide_name %}<h3><a href="{{ profile.get_absolute_url }}">{{ profile.display_name }}</a></h3>{% endif %}
	<table>
		{% if profile.user.email %}
		<tr>
			<th>email:</th>
			<td>{{ profile.user.email }}</td>
		</tr>
		{% endif %}
		{% if profile.phone_number %}
		<tr>
			<th>phone:</th>
			<td>{{ profile.phone_number }}</td>
		</tr>
		{% endif %}
		{% ifnotequal profile.collaborators.count 0 %}
		<tr>
			<th>collaborators:</th>
			<td>
			{% for artist in profile.collaborators %}
				<a href="{{ artist.get_profile.get_absolute_url }}">{{ artist.get_profile.display_name }}</a>{% loop_comma %}
			{% endfor %}
			</td>
		</tr>
		{% endifnotequal %}
		{% ifnotequal profile.user.artistgroup_set.all.count 0 %}
		<tr>
			<th>groups:</th>
			<td>
				{% for artist_group in profile.user.artistgroup_set.all %}
					<a href="{{ artist_group.get_absolute_url }}">{{ artist_group }}</a>{% loop_comma %}
				{% endfor %}
			</td>
		</tr>
		{% endifnotequal %}
		{% if profile.bio %}
		<tr>
			<th>bio:</th>
			<td>{{ profile.bio }}</td>
		</tr>
		{% endif %}
		{% if profile.url %}
		<tr>
			<th>url:</th>
			<td><a href="{{ profile.url }}">{{ profile.url }}</a></td>
		</tr>
		{% endif %}
		<tr><th>artwork:</th>
		<td>
			{% for installation in profile.user.installation_set.all %}
			<a href="{{ installation.get_absolute_url }}">{{ installation.name }}</a>{% loop_comma %}
			{% endfor %}
			{% for artist_group in profile.user.artistgroup_set.all %}
				{% for installation in artist_group.installation_set.all %}
					<a href="{{ installation.get_absolute_url }}">{{ installation.name }}</a>{% loop_comma %}
				{% endfor %}
			{% endfor %}
		</td>
	</table>
</div>