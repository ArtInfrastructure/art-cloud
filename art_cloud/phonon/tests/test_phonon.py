from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail

from phonon.models import *

APP_PATH = '/phone/'

class BasicViewsTest(TestCase):
	fixtures = ["auth.json", "sites.json"]
	
	def setUp(self):
		self.client = Client()

	def tearDown(self):
		pass
	
	def test_phonon_basics(self):
      pass
