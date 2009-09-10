#!/usr/bin/python

"""
This is a script which will fetch the current weather at the airport.

From the command line: python weather_client.py

TROUBLESHOOTING
If you run this script and get an error like "/usr/bin/python: bad interpreter: No such file or directory":
Find the python interpreter and set the first line in this file to reflect it's full path.
For example, if the python program is at /bin/python make the first line "#!/bin/python"

If you run this script get an error like "ImportError: No module named urllib":
Make certain that you have a full modern python (Python 2.5.1 at the time of writing) by running "python --version".
If you have a python older than 2.4, you will need to upgrade to a newer version.

If the script waits for a while and then spits out a bunch of errors that end with "Operation timed out":
Double check that your system can connect to the web server defined by the PRODUCTION_HOST variable below.

WRITING YOUR OWN WEATHER CLIENT
Any environment which can make HTTP requests and parse XML can GET the weather data.
The URL for the heartbeat receiver is: http://<hostname>/api/weather.api
The hostname is the one in the PRODUCTION_HOST variable below.
"""

import urllib
import pprint
import traceback
import datetime
import time

PRODUCTION_HOST = "174.129.3.149"
PRODUCTION_WEATHER_URL = "http://%s/api/weather.xml" % PRODUCTION_HOST
DEBUG_HOST = "127.0.0.1:8000"
DEBUG_WEATHER_URL = "http://%s/api/weather.xml" % DEBUG_HOST

WEATHER_URL = PRODUCTION_WEATHER_URL
HOST = PRODUCTION_HOST
HOST = DEBUG_HOST
WEATHER_URL = DEBUG_WEATHER_URL

WEATHER_TIMEOUT = 80 # in seconds

def fetch_weather_xml():
	sock = urllib.urlopen(WEATHER_URL)
	xml = sock.read()
	sock.close()
	return xml

if __name__ == "__main__":
	try:
		print fetch_weather_xml();
	except:
		print "Could not fetch the weather: %s" % datetime.datetime.now()
		print pprint.pformat(traceback.format_exc())

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
