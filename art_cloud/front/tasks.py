from scripts.scheduler import Task
import traceback
import logging
import pprint
import sys
import datetime

class HeartbeatTask(Task):
	"""The schedule task which updates the stored images for each of the artcams."""
	def __init__(self, loopdelay=300, initdelay=1):
		Task.__init__(self, self.do_it, loopdelay, initdelay)
	def do_it(self):
		from models import Heartbeat, Installation
		for heartbeat in Heartbeat.objects.filter(created__lt=datetime.datetime.now() - datetime.timedelta(days=180)):
			heartbeat.delete()

		message = ""
		should_send = False
		for installation in Installation.objects.all():
			if installation.is_opened():
				heartbeats = Heartbeat.objects.filter(installation=installation)
				if len(heartbeats) == 0: continue #no heartbeat in days?  ignoring
				if heartbeats[0].timed_out():
					message += 'No heartbeat for %s since %s.\n' % (installation.name, heartbeats[0].created)
					should_send = True
		if should_send:
			self.send_alert('Heartbeat Failure', message)
