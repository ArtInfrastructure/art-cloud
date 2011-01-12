from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.conf import settings

from malleus.incus_client import IncusClient
from hydration import dehydrate_to_xml

class IncusClientTest(TestCase):
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_client(self):
		incus_client = IncusClient(settings.ART_SERVER_HOST, settings.ART_SERVER_PORT)
		devices = incus_client.fetch_devices()
		self.assertTrue(len(devices) > 0)
		device = incus_client.fetch_device(devices[0].id)
		self.assertTrue(device != None)
		self.assertTrue(len(device.channel_groups) > 0)
		group = incus_client.fetch_group(device.channel_groups[0].id)
		print dehydrate_to_xml(group)