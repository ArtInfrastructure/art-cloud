import pprint
import urllib 
import datetime
from xml.dom import minidom
from xml.dom.minidom import Node
from django.core.cache import cache

LOCATION_TRIPLETS = (('Seattle', 47.62180, -122.35030), ('Portland', 45.52361, -122.675), ('Spokane', 47.65889, -117.425), ('Boise', 43.61361, -116.2025), ('Pendleton', 45.67222, -118.7875))

NOAA_FORECAST_URL_FORMAT = "http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?lat=%s&lon=%s&format=24+hourly&startDate=%s&numDays=1"
NOAA_CACHE_KEY = "noaa_weather"

class WeatherQuery:
	"""A lazily populated weather forecast object.  Uses the noaa_weather function, which will cache if possible to limit connections to the NOAA."""
	def __init__(self, location_triplet=LOCATION_TRIPLETS[0], date=datetime.datetime.now()):
		self.location_name = location_triplet[0]
		self.latitude = location_triplet[1]
		self.longitude = location_triplet[2]
		self.date = date
		self.error_message = None
		self.populated = False
		
		self.__min_temp = None
		self.__max_temp = None
		self.__summary = None
		self.__icon_url = None
	def populate(self):
		if self.populated: return
		try:
			weather = noaa_weather((self.location_name, self.latitude, self.longitude), self.date)
			self.__summary = weather['summary']
			self.__min_temp = weather['min_temp']
			self.__max_temp = weather['max_temp']
			self.__icon_url = weather['icon_url']
		except:
			error_message = "Failed to fetch the weather in %s." % self.location_name
		self.populated = True
	def __get_summary(self):
		self.populate()
		return self.__summary
	def __set_summary(self, summary):
		self.__summary = summary
	summary = property(__get_summary, __set_summary)
	def __get_max_temp(self):
		self.populate()
		return self.__max_temp
	def __set_max_temp(self, max_temp):
		self.__max_temp = max_temp
	max_temp = property(__get_max_temp, __set_max_temp)
	def __get_min_temp(self):
		self.populate()
		return self.__min_temp
	def __set_min_temp(self, min_temp):
		self.__min_temp = min_temp
	min_temp = property(__get_min_temp, __set_min_temp)
	def __get_icon_url(self):
		self.populate()
		return self.__icon_url
	def __set_icon_url(self, icon_url):
		self.__icon_url = icon_url
	icon_url = property(__get_icon_url, __set_icon_url)	

	class HydrationMeta:
		attributes = ['location_name', 'latitude', 'longitude', 'date', 'error_message', 'min_temp', 'max_temp', 'icon_url']


def noaa_weather(location_triplet, date=datetime.datetime.now()):
	"""Fetch the day's forecast from the NOAA, cached so we don't overstay our welcome"""
	weather = cache.get(create_cache_key(location_triplet[1], location_triplet[2], date))
	if weather: return weather
	print "missed the weather cache"
	
	url = NOAA_FORECAST_URL_FORMAT % (location_triplet[1], location_triplet[2], date.strftime('%Y-%m-%d'))
	dom = minidom.parse(urllib.urlopen(url))
	weather = {}
	for node in dom.getElementsByTagName('temperature'):
		if node.getAttribute('type') == 'maximum': weather['max_temp'] = node.childNodes.item(3).firstChild.nodeValue
		if node.getAttribute('type') == 'minimum': weather['min_temp'] = node.childNodes.item(3).firstChild.nodeValue
	print "%s" % dom.toprettyxml()
	weather['summary'] = dom.getElementsByTagName('weather-conditions')[0].getAttribute('weather-summary')
	weather['icon_url'] = dom.getElementsByTagName('icon-link')[0].firstChild.nodeValue
	weather['location_name'] = location_triplet[0]
	weather['latitude'] = location_triplet[1]
	weather['longitude'] = location_triplet[2]
	cache.set(create_cache_key(location_triplet[1], location_triplet[2], date), weather, 3600)
	return weather

def create_cache_key(latitude, longitude, date):
	return "%s_%s_%s_%s" % (NOAA_CACHE_KEY, latitude, longitude, date.strftime('%Y-%m-%d'))
