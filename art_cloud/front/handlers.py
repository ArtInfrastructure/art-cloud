import re

from django.contrib.auth.models import User

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from weather import WeatherQuery, zip_to_lat_lon, airport_code_to_observation

class WeatherHandler(BaseHandler):
	methods_allowed = ('GET',)
	def read(self, request, zip_code):
		zip_result = zip_to_lat_lon(zip_code)
		if not zip_result:
			return rc.NOT_FOUND
		wq = WeatherQuery(['%s, %s' % (zip_result[2], zip_result[3]), zip_result[0], zip_result[1]])
		wq.populate()
		return wq

class AirportObservationHandler(BaseHandler):
	methods_allowed = ('GET',)
	def read(self, request, airport_code):
		result = airport_code_to_observation(airport_code)
		if not result: return rc.NOT_FOUND
		return result

