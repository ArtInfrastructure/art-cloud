{% load imagetags %}
{% load wikitags %}
{% if page.public or request.user.is_staff %}
	<div class="wiki-control-links">
		{% if request.user.is_staff %}[<a href="{% url wiki.views.wiki_history page.name %}">page history</a>]{% endif %}
		[<a href="{% url wiki.views.wiki_print page.name %}">print version</a>]
		{% if request.user.is_staff %}[<a href="{% url wiki.views.wiki_edit page.name %}">edit this page</a>]{% endif %}
	</div>
	{% if not hide_title %}<h1><a href="{% url wiki.views.index %}">Wiki</a>: {{ page.name }} </h1>{% endif %}

	{% if page.rendered %}
		<div class="rendered-page">{{ page.rendered|include_constants|safe }}</div>
	{% endif %}

	{% if page.wikifile_set.all %}
	<h3>Files:</h3>
	{% endif %}
	{% for file in page.wikifile_set.all %}
		<div class="wiki-file-item">
			<a href="{{ file.file.url }}">{{ file.display_name }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
		</div>
	{% endfor %}
{% else %}
   <p>This page exists but is only available to staff.</p>
{% endif %}
