{% load imagetags %}
{% load wikitags %}

{% block sub-head %}
<script type="text/javascript">
var isPublic = {% if page.public %}true{% else %}false{% endif %};
function togglePublic(){
	$.ajax({
		type: 'POST',
		url: '.',
		data: ({'public':!isPublic}),
		success: function(data) { isPublic = !isPublic; },
		error: function(request, status, error) {  }
	});
	return true;
}
</script>
{% endblock %}

{% if page.public or request.user.is_staff %}
	<div class="wiki-control-links">
		[<a href="{% url wiki.views.wiki_history page.name %}">page history</a>]
		[<a href="{% url wiki.views.wiki_print page.name %}">print version</a>]
		[<a href="{% url wiki.views.wiki_edit page.name %}">edit this page</a>]
		{% if not hide_public %}
			{% if request.user.is_staff %}public: <form action="." method="post" onsubmit="return false;"><input onclick="togglePublic();" type="checkbox" {% if page.public %}checked="checked"{% endif %} name="public"/>{% csrf_token %}</form>{% endif %}
		{% endif %}
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
   <p>This page exists but is not public.</p>
{% endif %}
