{% load listtags %}
{% load imagetags %}
<div class="installation-item {% cycle 'even-row' 'odd-row' %}">
	{% if not hide_title %}<h3><a href="{{ installation.get_absolute_url }}">{{ installation.name }}</a></h3>{% endif %}
	<table>
		{% if installation.artists.all or installation.groups.all %}
		<tr>
			<th>artists:</th>
			<td>
				{% for artist in installation.artists.all %}
					<a href="{{ artist.get_profile.get_absolute_url }}">{{ artist.get_profile.display_name }}</a>{% loop_comma %}{% endfor %}{% ifnotequal installation.artists.all.count 0 %}{% ifnotequal installation.groups.all.count 0 %},{%endifnotequal%}{%endifnotequal%}
				{% for artist_group in installation.groups.all %}
					{% for artist in artist_group.artists.all %}<a href="{{ artist.get_profile.get_absolute_url }}">{{ artist.get_profile.display_name }}</a>{% loop_comma %}{% endfor %}
				{% endfor %}
			</td>
		</tr>
		{% endif %}
		{% ifnotequal installation.groups.all.count 0 %}
		<tr>
			<th>groups:</th>
			<td>
				{% for artist_group in installation.groups.all %}
						<a href="{{ artist_group.get_absolute_url }}">{{ artist_group }}</a>{% loop_comma %}
				{% endfor %}
			</td>
		</tr>
		{% endifnotequal %}
		{% if installation.site %}
		<tr>
			<th>location:</th>
			<td><a href="{{ installation.site.get_absolute_url }}">{{ installation.site }}</a></td>
		</tr>
		{% endif %}
		{% if installation.opened %}
		<tr>
			<th>opened:</th>
			<td>{{ installation.opened|date:"F j, Y \a\t g:i A" }}</td>
		</tr>
		{% endif %}
		{% if installation.closed %}
		<tr>
			<th>closed:</th>
			<td>{{ installation.closed|date:"F j, Y \a\t g:i A" }}</td>
		</tr>
		{% endif %}
		{% if installation.notes %}
		<tr>
			<th>notes:</th>
			<td>{{ installation.notes }}</td>
		</tr>
		{% endif %}
		{% if installation.heartbeat_set.all %}
		<tr>
			<th>heartbeat:</th>
			<td>
				{% with installation.heartbeat_set.all|first as heartbeat %}
					{{ heartbeat.created|date:"F j \a\t g:i A" }}
					{% if heartbeat.info %}<p>{{ heartbeat.trimmed_info }}</p>{% endif %}
				{% endwith %}
				[<a href="{% url front.views.installation_heartbeats installation.id %}">all</a>]
			</td>
		</tr>
		{% endif %}
		{% if installation.tags or edit_tags %}
		<tr>
			<th>tags:</th>
			<td>
				{% for tag in installation.tags %}
				<a href="{% url front.views.tag tag.name %}">{{ tag.name }}</a>{% loop_comma %}
				{% endfor %}
				{% if edit_tags and tags_form %}
				<form action="." method="post">{% for field in tags_form %}{{ field }}{% endfor %}</form>
				{% endif %}
			</td>
		</tr>
		{% endif %}
		{% if installation.wiki_name %}
		<tr>
			<th>wiki:</th>
			<td><a href="{% url wiki.views.wiki installation.wiki_name %}">{{ installation.wiki_name }}</a></td>
		</tr>
		{% endif %}
		{% if installation.photos.all %}
		<tr>
			<th>photos:</th>
			<td>
				{% for photo in installation.photos.all %}
					<a href="{{ photo.get_absolute_url }}"><img src="{{ photo.image.url|fit_image:"50x50" }}" /></a>
				{% endfor %}
			</td>
		</tr>
		{% endif %}
		{% if installation.named_dates.all %}
		<tr>
			<th>dates:</th>
			<td>
				<table class="date-list">
				{% for date in installation.named_dates.all %}
					<tr class="hover-tr {% cycle 'even-row' 'odd-row' %}">
					<td>{{ date.name }} / {{ date.date|date:"Y-m-j" }}</td>
					<td>{% if named_date_form %}<span class="hover-td">[<a href="." onclick="deleteNamedDate({{ date.id }}); return false;">delete</a>]</span>{% endif %}</td>
					</tr>
				{% endfor %}
				</table>
			</td>
		</tr>
		{% endif %}
		{% if named_date_form %}
		<tr>
			<th>&nbsp;</th>
			<td>
				<a href="." onclick="showAddNamedDateForm(); return false;">add date</a>
			</td>
		</tr>
		{% endif %}
	</table>
</div>