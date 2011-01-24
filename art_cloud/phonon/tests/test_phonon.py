import datetime

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.core.files import File
from django.core.urlresolvers import reverse

from phonon.models import *

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_emergency_call(self):
		if settings.PRODUCTION: raise Error("I won't test the emergency system because this is production!")
		call_guid = '232425262728'
		phone_number='2065551111'

		response = self.client.post(reverse('phonon.api_views.emergency_intro'), {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/emergency_intro.xml')

		response = self.client.post(reverse('phonon.api_views.emergency_code'), {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 302, 'status was %s' % response.status_code )

		response = self.client.post(reverse('phonon.api_views.emergency_code'), {'Digits':'1234', 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 302, 'status was %s' % response.status_code )

		response = self.client.post(reverse('phonon.api_views.emergency_code'), {'Digits':'111111', 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 302, 'status was %s' % response.status_code )

		response = self.client.post(reverse('phonon.api_views.emergency_code'), {'Digits':'123456', 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/emergency_activated.xml') # Right digits means play the activation message
	
	def test_phonon_basics(self):
		if settings.PRODUCTION: raise Error("I won't test the phonon system because this is production!")
		call_guid = '232425262728'
		phone_number='2065551111'
		formatted_phone_number='206-555-1111'

		self.failUnless(PhoneCall.objects.all().count() == 0)
		self.failUnless(Phone.objects.all().count() == 0)
		response = self.client.post(reverse('phonon.api_views.tour_intro'), {'CallGuid':call_guid, 'AccountGuid':'BOGUS222333', 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/no_auth.xml')

		response = self.client.post(reverse('phonon.api_views.tour_intro'), {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/tour_intro.xml')
		self.failUnless(response.content.count("<Say>") == 1)

		phone = Phone.objects.get(phone_number=phone_number)
		call = PhoneCall.objects.get(guid=call_guid)
		self.failUnless(call.completed == None)
		
		source_file = file('phonon/tests/data/test_intro.mp3', 'r')
		clip = AudioClip(name='Test Landing Clip', landing_clip=True)
		clip.audio.save(source_file.name, File(source_file), save=False)
		clip.save()

		response = self.client.post(reverse('phonon.api_views.tour_intro'), {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/tour_intro.xml')
		self.failUnless(response.content.count("<Play>") == 1)
		#print response.content 

		clip.landing_clip = False
		clip.save()
		response = self.client.post(reverse('phonon.api_views.tour_intro'), {'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/tour_intro.xml')
		self.failUnless(response.content.count("<Say>") == 1)
		clip.landing_clip = True
		clip.save()

		response = self.client.post(reverse('phonon.api_views.information_node'), {'Digits':'1234', 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 302, 'status was %s' % response.status_code )
		
		node = InformationNode.objects.create(name="Test Node", code=1234, introduction=clip)
		response = self.client.post(reverse('phonon.api_views.information_node'), {'Digits':node.code, 'CallGuid':call_guid, 'AccountGuid':settings.TWILIO_ACCOUNT_GUID, 'CallStatus':'in-progress', 'Caller':phone_number })
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.failUnless(response.template.name == 'phonon/phone/information_node.xml', 'template was %s' % response.template.name)
		
