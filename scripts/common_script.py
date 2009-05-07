#!/usr/bin/python
import os
import datetime
import sys

import settings

DEBUG = False

def call_system(command):
	print command
	if DEBUG: return True
	return os.system(command) == 0