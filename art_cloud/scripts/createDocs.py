#!/usr/bin/python
"""Creates the HTML documentation for the art-cloud APIs."""
import os
import datetime
import sys

from common_script import *

APP_NAME = 'Art Cloud'
SETTINGS = 'art_cloud.settings'

def main():
	command = 'export PYTHONPATH=.; export DJANGO_SETTINGS_MODULE=%s; epydoc --html . -v -o ../../docs/ --name "%s API Docs"' % (SETTINGS, APP_NAME)
	if not call_system(command):
		print 'aborting'
		return

if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.