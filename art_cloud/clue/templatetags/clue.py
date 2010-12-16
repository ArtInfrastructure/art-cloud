import traceback
from django import template
from django.conf import settings
from django.template.loader import render_to_string

register = template.Library()

from art_cloud.clue.models import HelpText

def strip_quotes(input):
	if not input: return input
	if input[0] == '"': input = input[1:]
	if input[-1] == '"': input = input[0:-1]
	return input

class HelpTextNode(template.Node):
	def __init__(self, help_name):
		self.help_name = help_name
	def render(self, context):
		if HelpText.objects.filter(name=self.help_name).count() == 0: return 'There is no help text for this name: "%s"' % self.help_name
		return render_to_string('clue/help_text.frag', {'rendered': HelpText.objects.get(name=self.help_name).rendered })

@register.tag(name="help_text")
def help_text(parser, token):
	try:
		help_name = strip_quotes(token.split_contents()[1])
	except ValueError:
		raise template.TemplateSyntaxError, "help_text tag requires one argument, the name of the help text"
	return HelpTextNode(help_name)

# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
