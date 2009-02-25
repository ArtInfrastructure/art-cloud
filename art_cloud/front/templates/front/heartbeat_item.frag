<div class="heartbeat-item">
	{% if not hide_installation %}
		<a href="{% url front.views.installation_heartbeats heartbeat.installation.id %}">{{ heartbeat.installation.name }}</a>:
	{% endif %}
	{{ heartbeat.created|date:"g:i A" }}{% if heartbeat.info %}: {{ heartbeat.info }}{% endif %}
</div>