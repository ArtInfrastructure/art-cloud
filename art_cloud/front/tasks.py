from scripts.scheduler import Task
import traceback
import logging
import pprint
import sys
import datetime

class HeartbeatTask(Task):
	"""The schedule task which updates the stored images for each of the artcams."""
	def __init__(self, loopdelay=86400, initdelay=15):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from models import Heartbeat
		for heartbeat in Heartbeat.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(days=180)):
			heartbeat.delete()

