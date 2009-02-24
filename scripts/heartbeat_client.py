#!/usr/bin/python

# BEFORE RUNNING: Set this to your installation id, as provided by the art technician.

INSTALLATION_ID = 15

# This is a script which will generate a heartbeat call to the art infrastructure.
# If your piece does not send heartbeats the art technicial will be notified.


# From the command line: python heartbeat_client.py
# The script will periodically send the heartbeat to the art infrastructure and won't quit unless you stop the script.

# TROUBLESHOOTING
# If you run this script and get an error like "/usr/bin/python: bad interpreter: No such file or directory":
# Find the python interpreter and set the first line in this file to reflect it's full path.
# For example, if the python program is at /bin/python make the first line "#!/bin/python"

# If you run this script get an error like "ImportError: No module named urllib":
# Make certain that you have a full modern python (Python 2.5.1 at the time of writing) by running "python --version".
# If you have a python older than 2.4, you will need to upgrade to a newer version.

# If the script waits for a while and then spits out a bunch of errors that end with "Operation timed out":
# Double check that your system can connect to the web server defined by the PRODUCTION_HOST variable below.

# WRITING YOUR OWN HEARTBEAT CLIENT
# Any environment which can make HTTP requests can generate heartbeats by periodically making a GET request.
# The URL for the heartbeat receiver is: http://<hostname>/heartbeat/?installation_id=<id>
# The hostname is the one in the PRODUCTION_HOST variable below.
# The installation id should be provided by the art technician.
# Have your program GET that URL once a minute and the art infrastructure will handle the rest.

# OPTIONALLY, you can add an info parameter which will be included in the database for easy access
# via the art cloud web UI
# For example: http://<hostname>/heartbeat/?installation_id=101&info=my%20art%20is%20faboo

# Alternatively, you could load the heartbeat URL in your browser and manually hit reload every minute or so.

import urllib
import pprint
import traceback
import time

INSTALLATION_ID_PARAMETER = 'installation_id'
INFO_PARAMETER = "info"
PRODUCTION_HOST = "174.129.242.90"
PRODUCTION_HEARTBEAT_URL = "http://%s/heartbeat/?%s=%s" % (PRODUCTION_HOST, INSTALLATION_ID_PARAMETER, INSTALLATION_ID)
DEBUG_HOST = "127.0.0.1:8000"
DEBUG_HEARTBEAT_URL = "http://%s/heartbeat/?%s=%s" % (DEBUG_HOST, INSTALLATION_ID_PARAMETER, INSTALLATION_ID)

HOST = DEBUG_HOST
HEARTBEAT_URL = DEBUG_HEARTBEAT_URL

HEARTBEAT_TIMEOUT = 80 # in seconds
HEARTBEAT_PERIOD = HEARTBEAT_TIMEOUT / 2

def send_heartbeat():
	sock = urllib.urlopen(HEARTBEAT_URL)
	sock.read()
	sock.close()

if __name__ == "__main__":
	while True:
		try:
			send_heartbeat();
		except:
			print pprint.pformat(traceback.format_exc())
		time.sleep(HEARTBEAT_PERIOD)

# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
