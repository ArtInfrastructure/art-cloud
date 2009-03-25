{% load imagetags %}
<div class="wiki-control-links">
	[<a href="{% url wiki.views.wiki_history page.name %}">page history</a>]
	[<a href="{% url wiki.views.wiki_edit page.name %}">edit this page</a>]
</div>
{% if not hide_title %}<h1><a href="{% url wiki.views.index %}">Wiki</a>: {{ page }} </h1>{% endif %}

{% if page.rendered %}
	<div class="rendered-page">{{ page.rendered|safe }}</div>
{% endif %}

{% if page.wikifile_set.all %}
<h3>Files:</h3>
{% endif %}
{% for file in page.wikifile_set.all %}
	<div class="wiki-file-item">
		<a href="{{ file.file.url }}">{{ file.display_name }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
	</div>
{% endfor %}