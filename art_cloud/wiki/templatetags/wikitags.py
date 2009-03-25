import re
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags, linebreaks, urlize
from django.contrib.markup.templatetags.markup import markdown
register = template.Library()

WIKI_NAME = r'(?:[A-Z]+[a-z]+){2,}'
WIKIREGEX = re.compile(r'\b(%s)\b' % WIKI_NAME)

WIKI_PHOTO = r'(?:Photo([\d])+)'
WIKI_PHOTO_REGEX = re.compile(r'\b(%s)\b' % WIKI_PHOTO)

@register.filter
def wiki(text):
	#text = strip_tags(text)
	text = markdown(text)
	text = urlize(text)
	text = WIKI_PHOTO_REGEX.sub(r'<a href="%sphoto-detail/\2/"><img src="%sphoto/\2/" width="150" /></a>' % (reverse('wiki.views.index', args=[], kwargs={}), reverse('wiki.views.index', args=[], kwargs={})), text)
	text = WIKIREGEX.sub(r'<a href="%s\1/">\1</a>' % reverse('wiki.views.index', args=[], kwargs={}), text)
	return text
