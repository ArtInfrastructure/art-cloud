import datetime

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from django.core.files import File
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from clue.models import HelpText

class BasicViewsTest(TestCase):

	def setUp(self):
		self.client = Client()
		self.content1 = """This is really fun.
I like traffic lights.

http://trevor.smith.name/"""
		self.content2 = 'This is content 2'

	def tearDown(self):
		pass
	
	def test_rendering(self):
		help_text_html = render_to_string('clue/test1.frag', { })
		self.assertTrue(help_text_html.count('"test 1"') == 1)
		self.assertTrue(help_text_html.count('"test 2"') == 1)
		self.assertTrue(help_text_html.count('"no_quotes_test"') == 1)

		help_text1 = HelpText.objects.create(name='test 1', content=self.content1)
		self.assertTrue(help_text1.content != None and len(help_text1.content) > 0)
		self.assertTrue(help_text1.rendered != None and len(help_text1.rendered) > 0)

		help_text_html = render_to_string('clue/test1.frag', { })
		self.assertTrue(help_text_html.count('"test 1"') == 0)
		self.assertTrue(help_text_html.count(help_text1.rendered) == 1)
		self.assertTrue(help_text_html.count('"test 2"') == 1)
		self.assertTrue(help_text_html.count('"no_quotes_test"') == 1)

		help_text2 = HelpText.objects.create(name='no_quotes_test', content=self.content2)
		help_text_html = render_to_string('clue/test1.frag', { })
		self.assertTrue(help_text_html.count('"no_quotes_test"') == 0)
		self.assertTrue(help_text_html.count(help_text1.rendered) == 1)
		self.assertTrue(help_text_html.count(help_text2.rendered) == 1)

