import re

from django.contrib.auth.models import User

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from weather import WeatherQuery

class WeatherHandler(BaseHandler):
	methods_allowed = ('GET',)
	def read(self, request): 
		wq = WeatherQuery()
		wq.populate()
		return wq
	