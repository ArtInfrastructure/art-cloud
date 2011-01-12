import urllib
import pprint
import traceback
from datetime import datetime
import time
import sys
from lxml import etree

from hydration import hydrate_from_xml, dehydrate_to_xml

def get_resource(url):
	sock = urllib.urlopen(url)
	xml = sock.read()
	sock.close()
	return xml

class ABDeviceInfo:
	"""Wraps the ABDevice"""
	def __init__(self, id=None, name=None, ip=None, port=None, channel_groups=None):
		self.id = id
		self.name = name
		self.ip = ip
		self.port = port
		self.channel_groups = channel_groups or []
	def __repr__(self): return '%s' % self.name
	class HydrationMeta:
		element_name = 'abdevice'
		attributes = ['id', 'name', 'ip', 'port']
		nodes = ['channel_groups']
	def hydrate(self, data): 
		hydrate_from_xml(self, data)
		self.channel_groups = [ABChannelGroupInfo().hydrate(etree.tostring(element, pretty_print=True)) for element in etree.fromstring(data).xpath('.//abchannelgroup')]
		return self
		
class ABChannelGroupInfo:
	"""Wraps the ABChannelGroup"""
	def __init__(self, id=None, name=None, master_gain=None, channels=None):
		self.id = id
		self.name = name
		self.master_gain = master_gain
		self.channels = channels or []
	class HydrationMeta:
		element_name = 'abchannelgroup'
		attributes = ['id', 'name', 'master_gain']
		nodes = ['channels']
	def hydrate(self, data):
		hydrate_from_xml(self, data)
		self.channels = [ABChannelInfo().hydrate(etree.tostring(element, pretty_print=True)) for element in etree.fromstring(data).xpath('.//abchannel')]
		return self

class ABChannelInfo:
	"""Wraps the ABChannel"""
	def __init__(self, id=None, number=None, gain=None):
		self.id = id
		self.number = number
		self.gain = gain
	class HydrationMeta:
		element_name = 'abchannel'
		attributes = ['id', 'number', 'gain']
	def hydrate(self, data): return hydrate_from_xml(self, data)

class IncusClient(object):
	def __init__(self, host, port=80):
		self.host = host
		self.port = port
		
	def fetch_devices(self):
		try:
			xml = get_resource(self.ab_devices_url)
			device_elements = etree.fromstring(xml).xpath('//abdevice')
			return [ABDeviceInfo().hydrate(etree.tostring(element, pretty_print=True)) for element in device_elements]
		except:
			traceback.print_exc()
			return None
	
	def fetch_device(self, id):
		try:
			xml = get_resource(self.ab_device_url(id))
			device_elements = etree.fromstring(xml).xpath('//abdevice')
			return ABDeviceInfo().hydrate(etree.tostring(device_elements[0], pretty_print=True))
		except:
			traceback.print_exc()
			return None
	
	def fetch_group(self, id):
		try:
			xml = get_resource(self.ab_group_url(id))
			device_elements = etree.fromstring(xml).xpath('//abchannelgroup')
			return ABChannelGroupInfo().hydrate(etree.tostring(device_elements[0], pretty_print=True))
		except:
			traceback.print_exc()
			return None
	
	@property
	def api_url(self): return 'http://%s:%s/api/audio/' % (self.host, self.port)
	
	@property
	def ab_devices_url(self): return '%sab-device/' % self.api_url

	def ab_device_url(self, id): return '%s%s/' % (self.ab_devices_url, id)

	def ab_group_url(self, id): return '%sab-group/%s/' % (self.api_url, id)
