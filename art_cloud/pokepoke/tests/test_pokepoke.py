import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.core.files import File
from django.conf import settings
from django.core.urlresolvers import reverse

from pokepoke.models import AlertPermission, AlertLog

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_sending(self):
		self.failUnless(AlertPermission.objects.all().count() == 0)
		self.failUnless(AlertLog.objects.all().count() == 0)
		
		perm = AlertPermission.objects.create(name='Test Source')
		self.assertEquals(len(mail.outbox), 0)
		message1 = 'Test Message One'
		subject1 = 'Test Subject One'
		perm.send_alert(message1, subject1)
		self.assertEquals(len(mail.outbox), 1)
		self.assertEquals(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX+subject1)
		self.assertEquals(mail.outbox[0].body, message1)
		self.assertTrue(AlertLog.objects.all().count() == 1)
		alert = AlertLog.objects.all()[0]
		self.assertEqual(alert.subject, subject1)
		self.assertEqual(alert.message, message1)
		
		perm.send_alert(message1)
		self.assertEquals(len(mail.outbox), 2)
		self.assertTrue(mail.outbox[1].subject.startswith(settings.EMAIL_SUBJECT_PREFIX))
		self.assertEquals(mail.outbox[1].body, message1)
		self.assertTrue(AlertLog.objects.all().count() == 2)
		alert = AlertLog.objects.all()[1]
		self.assertEqual(alert.subject, 'No subject')
		self.assertEqual(alert.message, message1)

		api_path = reverse('pokepoke.api_views.alert', args=[], kwargs={})
		response = self.client.post(api_path, {'secret':perm.secret, 'subject':subject1, 'message':message1})
		self.failUnlessEqual(response.status_code, 200, 'status was %s' % response.status_code )
		self.assertEquals(len(mail.outbox), 3)
		self.assertEquals(mail.outbox[0].subject, settings.EMAIL_SUBJECT_PREFIX+subject1)
		self.assertEquals(mail.outbox[2].body, message1)
		self.assertTrue(AlertLog.objects.all().count() == 3)
		alert = AlertLog.objects.all()[2]
		self.assertEqual(alert.subject, subject1)
		self.assertEqual(alert.message, message1)
