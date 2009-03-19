import os
import re
import traceback
import Image
import datetime
from art_cloud.calendar import Calendar

from django.template import Library
from django import template
from django.utils.html import linebreaks
from django.conf import settings

from art_cloud.datonomy.models import *

register = template.Library()

class CalNode(template.Node):
	def __init__(self, year, month):
		self.year_var = template.Variable(year)
		self.month_var = template.Variable(month)
	def render(self, context):
		try:
			self.year = int(self.year_var.resolve(context))
			self.month = int(self.month_var.resolve(context))
		except template.VariableDoesNotExist:
			print 'does not exist'
			return ''

		start = datetime.datetime(day=1, month=self.month, year=self.year)
		end = start + datetime.timedelta(days=31)

		cal = Calendar()
		dates = NamedDate.objects.filter(date__gt=start, date__lt=end)
		print dates
		html = '<table class="datonomy-cal">'
		html += '<tr><th>monday</th><th>tuesday</th><th>wednesday</th><th>thursday</th><th>friday</th><th>saturday</th><th>sunday</th></tr>'
		for week in cal.monthdatescalendar(self.year, self.month):
			html += '<tr class="datonomy-week">'
			for day in week:
				html += '<td class="datonomy-day">'
				if day.month == start.month:
					html += '<div class="datonomy-date">%s</div>' % day.day
					for date in dates:
						if day.month == start.month and date.date.day == day.day: 
							html += '<a class="datonomy-named-date" href="%s">%s: %s</a>' % (date.get_absolute_url(), date.content_object, date.name)
						elif day.month == start.month and date.date.day > day.day: 
							break
				html += '</td>'
			html += '</tr>'
		html += '</table>'
		return html

@register.tag(name="cal")
def cal(parser, token):
	try:
		tag_name, year, month = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError, "%r tag requires two arguments: year month" % token.contents.split()[0]
	return CalNode(year, month)
