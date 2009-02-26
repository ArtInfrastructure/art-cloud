import re
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

register = template.Library()

WIKI_NAME = r'(?:[A-Z]+[a-z]+){2,}'
WIKIREGEX = re.compile(r'\b(%s)\b' % WIKI_NAME)

@register.filter
def wiki(text):
	text = strip_tags(text)
	return WIKIREGEX.sub(r'<a href="%s\1/">\1</a>' % reverse('wiki.views.index', args=[], kwargs={}), text)
