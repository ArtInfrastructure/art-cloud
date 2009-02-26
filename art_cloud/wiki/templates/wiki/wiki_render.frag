{% load imagetags %}
<div class="wiki-control-links">
	[<a href="{% url wiki.views.wiki_history page.name %}">page history</a>]
	[<a href="{% url wiki.views.wiki_edit page.name %}">edit this page</a>]
</div>
{% if not hide_title %}<h1><a href="{% url wiki.views.index %}">Wiki</a>: {{ page }} </h1>{% endif %}

{% if page.rendered %}
	<div class="rendered-page">{{ page.rendered|safe }}</div>
{% endif %}

<div class="wiki-control-links">[<a href="{% url wiki.views.wiki_add page.name %}">add file or photo</a>]</div>


{% if page.wikiphoto_set.all %}
<h3>Photos:</h3>
{% endif %}
{% for photo in page.wikiphoto_set.all %}
	<div class="wiki-photo-item">
		<a href="{{ photo.get_absolute_url }}">
			<img alt="{{ photo.title }}" title="{{ photo.title }}" src="{{ photo.image.url|fit_image:"150x150" }}" />
		</a>
	</div>
{% endfor %}

{% if page.wikifile_set.all %}
<h3>Files:</h3>
{% endif %}
{% for file in page.wikifile_set.all %}
	<div class="wiki-file-item">
		<a href="{{ file.file.url }}">{{ file.title }}</a> <span class="wiki-control-link">[<a href="{{ file.get_absolute_url }}">info</a>]</span>
	</div>
{% endfor %}
