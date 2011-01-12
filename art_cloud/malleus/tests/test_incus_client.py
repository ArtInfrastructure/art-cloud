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
		self.assertTrue(group != None)
		#print dehydrate_to_xml(group)

		old_gain = float(group.master_gain)
		if old_gain > 90:
			new_gain = old_gain - 10
		else:
			new_gain = old_gain + 10
		response_gain = incus_client.set_group_gain(group.id, new_gain)
		self.assertTrue(new_gain, response_gain)
		self.assertTrue(new_gain, incus_client.get_group_gain(group.id))
		response_gain = incus_client.set_group_gain(group.id, old_gain)
		self.assertTrue(old_gain, response_gain)
		self.assertTrue(old_gain, incus_client.get_group_gain(group.id))
		
		self.assertTrue(len(group.channels) > 0)
		channel = group.channels[0]
		old_gain = float(channel.gain)
		self.assertEqual(old_gain, incus_client.get_channel_gain(channel.id))
		if old_gain > 90.0:
			new_gain = 85.0
		else:
			new_gain = 10.0
		response_gain = incus_client.set_channel_gain(channel.id, new_gain)
		self.assertEqual(response_gain, new_gain)
		self.assertEqual(new_gain, incus_client.get_channel_gain(channel.id))
		response_gain = incus_client.set_channel_gain(channel.id, old_gain)
		self.assertEqual(response_gain, old_gain)
		self.assertEqual(old_gain, incus_client.get_channel_gain(channel.id))
