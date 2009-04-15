{% load listtags %}
{% load imagetags %}
<div class="installation-item {% cycle 'even-row' 'odd-row' %}">
	{% if not hide_title %}<h3><a href="{{ installation.get_absolute_url }}">{{ installation.name }}</a></h3>{% endif %}
	<table>
		<tr>
			<th>id number:</th>
			<td>{{ installation.id }}</td>
		</tr>
		{% if installation.artists.all or installation.groups.all %}
		<tr>
			<th>artist{{ installation.collaborators|pluralize }}:</th>
			<td>
				{% for artist in installation.collaborators %}
					<a href="{{ artist.get_profile.get_absolute_url }}">{{ artist.get_profile.display_name }}</a>{% loop_comma %}
				{% endfor %}
			</td>
		</tr>
		{% endif %}
		{% ifnotequal installation.groups.all.count 0 %}
		<tr>
			<th>group{{ installation.groups.all|pluralize }}:</th>
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
		{% if installation.notes or installation_notes_form %}
		<tr>
			<th>notes:</th>
			<td>
				<pre class="installation-notes" id="installation-notes-{{ installation.id }}">{{ installation.notes }}</pre>
				{% if installation_notes_form %}
				<div class="installation-notes-widget" id="installation-notes-widget-{{ installation.id }}">
					<div style="float: right;">
						[<a href="." onclick="$('#installation-notes-widget-{{ installation.id }}').hide(); $('#installation-notes-{{ installation.id }}').show(); return false;">close</a>]
					</div>
					<form action="." method="post">
						{% for field in installation_notes_form %}{{ field}}{% endfor %}
						<input type="hidden" name="installation_form_id" value="{{ installation.id }}" />
						<input type="submit" value="save note" />
					</form>
				</div>
				[<a href="." onclick="$('#installation-notes-{{ installation.id }}').hide(); $('#installation-notes-widget-{{ installation.id}}').show(); return false">edit</a>]
				{% endif %}
			</td>
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
			<th>tag{{ installation.tags|pluralize }}:</th>
			<td>
				<div id="tag-list">
					{% for tag in installation.tags %}
					<a href="{% url front.views.tag tag.name %}">{{ tag.name }}</a>{% loop_comma %}
					{% endfor %}
					{% if edit_tags and tags_form %}
					[<a href="." onclick="$('#tag-list').hide(); $('#tag-form').show(); return false;">edit</a>]
					{% endif %}
				</div>
				{% if edit_tags and tags_form %}
				<form id="tag-form" action="." method="post">{% for field in tags_form %}{{ field }}{% endfor %} <input type="submit" value="save tags"/><input type="hidden" name="tag-form" value="true" /></form>
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
		{% if installation.photos.all or installation_photo_form %}
		<tr>
			<th>photo{{ installation.photos.all|pluralize }}:</th>
			<td>
				{% for photo in installation.photos.all %}
					<a href="{{ photo.get_absolute_url }}"><img src="{{ photo.image.url|fit_image:"50x50" }}" /></a>
				{% endfor %}
				{% if installation_photo_form %}
				{% if installation.photos.all %}<br />{% endif %}
				<div id="add-installation-photo-widget">
					<div style="float: right;">[<a href="." onclick="hideAddInstallationPhotoWidget(); return false;">close</a>]</div>
					<table>
						<form enctype="multipart/form-data" action='.' method='post'>
							{{ installation_photo_form }}
							<tr><th></th><td><input type="hidden" name="photo-form" value="true" /><input type="submit" value="add photo"></td></tr>
						</form>
					</table>
				</div>
				[<a href="." onclick="showAddInstallationPhotoWidget(); return false;">add</a>]
				{% endif %}
			</td>
		</tr>
		{% endif %}
		{% if installation.named_dates.all or can_edit_dates %}
		<tr>
			<th>date{{ installation.named_dates.all|pluralize }}:</th>
			<td>
				<table class="date-list">
				{% for date in installation.named_dates.all %}
					<tr class="hover-tr {% cycle 'even-row' 'odd-row' %}">
						{% include "datonomy/editable_named_date.frag" %}
					</tr>
				{% endfor %}
				{% if can_edit_dates %}
					<tr>
						<td>
							{% include "datonomy/named_date_add_widget.frag" %}
							[<a href="." onclick="showAddNamedDateForm(); return false;">add</a>]

						</td>
					</tr>
				{% endif %}
				</table>

			</td>
		</tr>
		{% endif %}
	</table>
</div>