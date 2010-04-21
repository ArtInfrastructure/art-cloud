# Copyright 2009,2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import re
from django import template
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags, linebreaks, urlize
from django.contrib.markup.templatetags.markup import markdown
register = template.Library()

WIKI_NAME = r'(?:[A-Z]+[a-z]+){2,}'
WIKIREGEX = re.compile(r'[^/]\b(%s)\b[^/]' % WIKI_NAME)

WIKI_HARD_NAME = r'(?:Link:([A-Z|a-z|_|-]+))'
WIKI_HARD_NAME_REGEX = re.compile(r'\b(%s)\b' % WIKI_HARD_NAME)


WIKI_PHOTO = r'(?:Photo([\d]+))'
WIKI_PHOTO_REGEX = re.compile(r'\b(%s)\b' % WIKI_PHOTO)

@register.filter
def wiki(text):
	"""Convert the text into HTML using markdown and image name replacement."""
	#text = strip_tags(text)
	text = urlize(text)
	text = markdown(text)
	text = WIKI_PHOTO_REGEX.sub(r'<a href="%sphoto-detail/\2/"><img src="%sphoto/\2/" width="150" /></a>' % (reverse('wiki.views.index', args=[], kwargs={}), reverse('wiki.views.index', args=[], kwargs={})), text)
	text = WIKIREGEX.sub(r' <a href="%s\1/">\1</a> ' % reverse('wiki.views.index', args=[], kwargs={}), text)
	text = WIKI_HARD_NAME_REGEX.sub(r'<a href="%s\2/">\2</a>' % reverse('wiki.views.index', args=[], kwargs={}), text)
	return text

@register.filter
def include_constants(text):
	from wiki.models import WikiConstant
	constants = WikiConstant.objects.all()
	for constant in constants:
		pattern = r'(?:\$%s\$)' % constant.name
		regex = re.compile(r'%s' % pattern)
		text = regex.sub(constant.constant, text)
		# handle the urlized constants which look like %24constant_name%24
		pattern = r'(?:%%24%s%%24)' % constant.name
		regex = re.compile(r'%s' % pattern)
		text = regex.sub(constant.constant, text)
	return text

@register.filter
def truncate(value, arg):
	"""
	Truncates a string after a given number of chars  
	Argument: Number of chars to truncate after
	From: http://www.djangosnippets.org/snippets/163/
	"""
	try:
		length = int(arg)
	except ValueError: # invalid literal for int()
		return value # Fail silently.
	if not isinstance(value, basestring):
		value = str(value)
	if (len(value) > length):
		return value[:length] + "..."
	else:
		return value

