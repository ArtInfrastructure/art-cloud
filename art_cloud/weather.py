"""A library for fetching weather information from the National Oceanic and Atmospheric Administration 

Example dehydrated result: 
<?xml version="1.0" ?>
<weatherquery coverage="definitely" date="2009-05-05 10:52:13.011519" icon_url="http://www.nws.noaa.gov/weather/images/fcicons/ra70.jpg" intensity="light" latitude="47.6218" location_name="Seattle" longitude="-122.3503" max_temp="57" min_temp="50" weather_type="rain">
	<hazards>
		<dict>
			<item key="phenomena" value="Wind"/>
			<item key="hazard_type" value="long duration"/>
			<item key="significance" value="Advisory"/>
		</dict>
	</hazards>
</weatherquery>
"""
import pprint
import urllib 
import datetime
from xml.dom import minidom
from xml.dom.minidom import Node
from django.core.cache import cache
import logging

LOCATION_TRIPLETS = (('San Jose', 37.3201, -121.8776), ('Seattle', 47.62180, -122.35030), ('Portland', 45.52361, -122.675), ('Spokane', 47.65889, -117.425), ('Boise', 43.61361, -116.2025), ('Pendleton', 45.67222, -118.7875))

NOAA_FORECAST_URL_FORMAT = "http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdXMLclient.php?lat=%s&lon=%s&product=time-series&maxt=maxt&mint=mint&wspd=wspd&wdir=wdir&sky=sky&wx=wx&icons=icons"
#NOAA_FORECAST_URL_FORMAT = "http://www.weather.gov/forecasts/xml/sample_products/browser_interface/ndfdBrowserClientByDay.php?lat=%s&lon=%s&format=24+hourly&startDate=%s&numDays=1&wspd=wspd"
NOAA_CACHE_KEY = "noaa_weather"

GEOCODER_ZIP_API_URL_FORMAT = "http://geocoder.us/service/csv/geocode?zip=%s"
GEOCODER_CACHE_KEY = 'geocoder_zip'

AIRPORT_CODE_API_URL_FORMAT = "http://www.weather.gov/xml/current_obs/%s.xml"
AIRPORT_CODE_CACHE_KEY = 'airport_code'

ICAO_AIRPORT_OBSERVATION_URL_FORMAT = "http://weather.noaa.gov/pub/data/observations/metar/decoded/%s.TXT" #the ICAO code must be ALL CAPS
ICAO_AIRPORT_OBSERVATION_CACHE_KEY = 'icao_airport_obs'

NO_SUCH_CODE_CACHE_VALUE = 'no such code'

def icao_airport_observation(code):
	"""pass in a four letter ICAO airport code and receive NOAA's text information for that airport.
	For example, passing in 'rjaa' (or 'RJAA') would return something like this:
	New Tokyo Inter-National Airport, Japan (RJAA) 35-46N 140-23E 44M
	Jan 20, 2010 - 01:00 PM EST / 2010.01.20 1800 UTC
	Wind: from the SW (220 degrees) at 22 MPH (19 KT) gusting to 36 MPH (31 KT):0
	Visibility: greater than 7 mile(s):0
	Sky conditions: mostly cloudy
	Temperature: 60 F (16 C)
	Dew Point: 51 F (11 C)
	Relative Humidity: 72%
	Pressure (altimeter): 29.68 in. Hg (1005 hPa)
	ob: RJAA 201800Z 22019G31KT 9999 FEW030 SCT180 BKN/// 16/11 Q1005 NOSIG RMK 1CU030 3AC180 A2970 P/FR
	cycle: 18	
	"""
	result = cache.get(create_icao_airport_observation_cache_key(code))
	if result:
		if result == NO_SUCH_CODE_CACHE_VALUE: return None
		return result
	logging.debug("missed the non-us airport observation cache for %s" % code)

	url = ICAO_AIRPORT_OBSERVATION_URL_FORMAT % code.upper()
	try:
		result = urllib.urlopen(url).read()
		if result.find('<title>404 Not Found</title>') != -1: result = NO_SUCH_CODE_CACHE_VALUE
	except:
		logging.exception('Error fetching non us airport observation for %s' % code)
		result = NO_SUCH_CODE_CACHE_VALUE
	cache.set(create_icao_airport_observation_cache_key(code), result, 1700)
	if result == NO_SUCH_CODE_CACHE_VALUE: return None
	return result

def create_icao_airport_observation_cache_key(code): return '%s_%s' % (ICAO_AIRPORT_OBSERVATION_CACHE_KEY, code)

def airport_code_to_observation(code):
	"""Return NOAA observation xml string for an airport code, cached so we don't overstay our welcome"""
	result = cache.get(create_airport_code_cache_key(code))
	if result:
		if result == NO_SUCH_CODE_CACHE_VALUE: return None
		return result
	print "missed the airport code cache"

	url = AIRPORT_CODE_API_URL_FORMAT % code
	try:
		result = urllib.urlopen(url).read()
		dom = minidom.parseString(result)
		if len(dom.getElementsByTagName('current_observation')) == 0: raise Exception
	except:
		result = NO_SUCH_CODE_CACHE_VALUE
	
	cache.set(create_airport_code_cache_key(code), result, 1700)
	if result == NO_SUCH_CODE_CACHE_VALUE: return None
	return result

def create_airport_code_cache_key(code): return '%s_%s' % (AIRPORT_CODE_CACHE_KEY, code)

def zip_to_lat_lon(zip):
	"""Fetch the lat/lon and city/state for a zip, cached so we don't overstay our welcome"""
	result = cache.get(create_zip_cache_key(zip))
	if result:
		if result == 'no such zip': return None
		return result
	print "missed the zip cache"

	url = GEOCODER_ZIP_API_URL_FORMAT % zip
	fields = urllib.urlopen(url).read().split(', ')
	if len(fields) != 5:
		cache.set(create_zip_cache_key(zip), 'no such zip', 10000000)
		return None
	result = [float(fields[0]), float(fields[1]), fields[2], fields[3]]
	cache.set(create_zip_cache_key(zip), result, 10000000)
	return result

def create_zip_cache_key(zip):
	return '%s_%s' % (GEOCODER_CACHE_KEY, zip)

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
		self.__weather_type = None
		self.__coverage = None
		self.__intensity = None
		self.__hazards = []
		self.__cloud_cover = None
		self.__wind_direction = None
		self.__wind_speed = None
	def populate(self):
		if self.populated: return
		try:
			weather = noaa_weather((self.location_name, self.latitude, self.longitude), self.date)
			self.__summary = weather['summary']
			self.__min_temp = weather['min_temp']
			self.__max_temp = weather['max_temp']
			self.__icon_url = weather['icon_url']
			self.__cloud_cover = weather['cloud_cover']
			self.__wind_direction = weather['wind_direction']
			self.__wind_speed = weather['wind_speed']
			if 'weather_type' in weather: self.__weather_type = weather['weather_type']
			if 'coverage' in weather: self.__coverage = weather['coverage']
			if 'intensity' in weather: self.__intensity = weather['intensity']
			if 'hazards' in weather: self.__hazards = weather['hazards']
		except:
			logging.exception('Error fetching weather')
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
	def __get_weather_type(self):
		self.populate()
		return self.__weather_type
	def __set_weather_type(self, weather_type): pass
	weather_type = property(__get_weather_type, __set_weather_type)	
	def __get_coverage(self):
		self.populate()
		return self.__coverage
	def __set_coverage(self, coverage): pass
	coverage = property(__get_coverage, __set_coverage)	
	def __get_intensity(self):
		self.populate()
		return self.__intensity
	def __set_intensity(self, intensity): pass
	intensity= property(__get_intensity, __set_intensity)	
	def __get_hazards(self):
		self.populate()
		return self.__hazards
	def __set_hazards(self, hazards): pass
	hazards = property(__get_hazards, __set_hazards)	
	def __get_cloud_cover(self):
		self.populate()
		return self.__cloud_cover
	def __set_cloud_cover(self, cloud_cover): pass
	cloud_cover = property(__get_cloud_cover, __set_cloud_cover)	
	def __get_wind_direction(self):
		self.populate()
		return self.__wind_direction
	def __set_wind_direction(self, wind_direction): pass
	wind_direction = property(__get_wind_direction, __set_wind_direction)	
	def __get_wind_speed(self):
		self.populate()
		return self.__wind_speed
	def __set_wind_speed(self, wind_speed): pass
	wind_speed = property(__get_wind_speed, __set_wind_speed)	

	class HydrationMeta:
		attributes = ['location_name', 'summary', 'latitude', 'longitude', 'date', 'error_message', 'min_temp', 'max_temp', 'icon_url', 'weather_type', 'coverage', 'intensity', 'cloud_cover', 'wind_speed', 'wind_direction']
		nodes = ['hazards']

def noaa_weather(location_triplet, date=datetime.datetime.now()):
	"""Fetch the day's forecast from the NOAA, cached so we don't overstay our welcome"""
	weather = cache.get(create_noaa_cache_key(location_triplet[1], location_triplet[2], date))
	if weather: return weather
	print "missed the weather cache"
	
	url = NOAA_FORECAST_URL_FORMAT % (location_triplet[1], location_triplet[2])
	dom = minidom.parse(urllib.urlopen(url))
	return noaa_dom_to_weather(location_triplet, date, dom)
	
def noaa_dom_to_weather(location_triplet, date, dom):
	weather = {}
	for node in dom.getElementsByTagName('temperature'):
		if node.getAttribute('type') == 'maximum': weather['max_temp'] = node.childNodes.item(3).firstChild.nodeValue.strip()
		if node.getAttribute('type') == 'minimum': weather['min_temp'] = node.childNodes.item(3).firstChild.nodeValue.strip()
	weather['summary'] = dom.getElementsByTagName('weather-conditions')[0].getAttribute('weather-summary')
	weather['icon_url'] = dom.getElementsByTagName('icon-link')[0].firstChild.nodeValue.strip()
	weather['location_name'] = location_triplet[0]
	weather['latitude'] = location_triplet[1]
	weather['longitude'] = location_triplet[2]
	tci_element = dom.getElementsByTagName('weather-conditions')[0].childNodes.item(1)
	if tci_element:
		weather['weather_type'] = tci_element.getAttribute('weather-type')
		weather['coverage'] = tci_element.getAttribute('coverage')
		weather['intensity'] = tci_element.getAttribute('intensity')
	
	weather['cloud_cover'] = int(dom.getElementsByTagName('cloud-amount')[0].childNodes.item(3).firstChild.nodeValue.strip())
	weather['wind_direction'] = int(dom.getElementsByTagName('direction')[0].childNodes.item(3).firstChild.nodeValue.strip())
	weather['wind_speed'] = int(dom.getElementsByTagName('wind-speed')[0].childNodes.item(3).firstChild.nodeValue.strip())
	
	for hazard in dom.getElementsByTagName('hazard'):
		if not hasattr(weather, 'hazards'):
			weather['hazards'] = []
		weather['hazards'].append({ 'hazard_type': hazard.getAttribute('hazardType'), 'phenomena':hazard.getAttribute('phenomena'), 'significance':hazard.getAttribute('significance') })
		print 'hazards ', weather['hazards']
	cache.set(create_noaa_cache_key(location_triplet[1], location_triplet[2], date), weather, 3600)
	return weather

def create_noaa_cache_key(latitude, longitude, date):
	return "%s_%s_%s_%s" % (NOAA_CACHE_KEY, latitude, longitude, date.strftime('%Y-%m-%d'))
