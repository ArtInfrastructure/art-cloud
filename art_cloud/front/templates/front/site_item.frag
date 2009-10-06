{% load listtags %}
{% load imagetags %}
<div class="site-item {% cycle 'even-row' 'odd-row' %}">
	{% if not hide_name %}<h3><a href="{{ installation_site.get_absolute_url }}">{{ installation_site.name }}</a></h3>{% endif %}
	<table>
		{% if installation_site.location %}
		<tr>
			<th>location:</th>
			<td>{{ installation_site.location }}</td>
		</tr>
		{% endif %}
		{% if installation_site.installation_set.all %}
		<tr>
			<th>artwork:</th>
			<td>
				{% for installation in installation_site.installation_set.all %}
					<a href="{{ installation.get_absolute_url }}">{{ installation }}</a>{% loop_comma %}
				{% endfor %}
			</td>
		</tr>
		{% endif %}
		{% if installation_site.equipment.all %}
		<tr>
			<th>equipment:</th>
			<td>
				{% for equipment in installation_site.equipment.all %}
					<a href="{{ equipment.get_absolute_url }}">{{ equipment.name }}</a>{% loop_comma %}
				{% endfor %}
			</td>
		</tr>
		{% endif %}
		{% if installation_site.notes %}
		<tr>
			<th>notes:</th>
			<td>{{ installation_site.notes }}</td>
		</tr>
		{% endif %}
		{% if installation_site.photos.all %}
		<tr>
			<th>image{{ installation_site.photos.all|pluralize }}:</th>
			<td>
				{% for photo in installation_site.photos.all %}
					<a href="{{ photo.get_absolute_url }}"><img alt="{{ photo.title }}" title="{{ photo.title }}" src="{{ photo.image.url|fit_image:"150x150" }}" /></a>
				{% endfor %}
			</td>
		</tr>
		{% endif %}
	</table>
</div>
