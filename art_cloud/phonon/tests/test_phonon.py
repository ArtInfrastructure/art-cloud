import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.core.files import File

from phonon.models import *

APP_PATH = '/phone/'
API_PATH = '/api/phone/'

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_phonon_basics(self):
		call_guid = '232425262728'
		phone_number='2065551111'
		formatted_phone_number='206-555-1111'

		self.failUnless(PhoneCall.objects.all().count() == 0)
		self.failUnless(Phone.objects.all().count() == 0)
		response = self.client.post(API_PATH + 'intro/', {'CallGuid':call_guid, 'AccountGuid':'BOGUS222333', 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/no_auth.xml')

		response = self.client.post(API_PATH + 'intro/', {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/intro.xml')
		self.failUnless(response.content.count("<Say>") == 1)

		phone = Phone.objects.get(phone_number=phone_number)
		call = PhoneCall.objects.get(guid=call_guid)
		self.failUnless(call.completed == None)
		
		source_file = file('phonon/tests/data/test_intro.mp3', 'r')
		clip = AudioClip(name='Test Landing Clip', landing_clip=True)
		clip.audio.save(source_file.name, File(source_file), save=False)
		clip.save()

		response = self.client.post(API_PATH + 'intro/', {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/intro.xml')
		self.failUnless(response.content.count("<Play>") == 1)

		clip.landing_clip = False
		clip.save()
		response = self.client.post(API_PATH + 'intro/', {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/intro.xml')
		self.failUnless(response.content.count("<Say>") == 1)
		clip.landing_clip = True
		clip.save()

		response = self.client.post(API_PATH + 'info/', {'Digits':'1234', 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 302, 'status was %s' % response.status_code )
		
		node = InformationNode.objects.create(name="Test Node", code=1234, introduction=clip)
		response = self.client.post(API_PATH + 'info/', {'Digits':node.code, 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/information_node.xml', 'template was %s' % response.template.name)
		
