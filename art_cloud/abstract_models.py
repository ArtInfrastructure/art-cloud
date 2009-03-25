# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import Image
import urllib
import datetime, calendar
import random
import time
import re
import feedparser
import unicodedata
import traceback
import logging
import pprint

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import models

class ThumbnailedModel(models.Model):
	"""An abstract base class for models with an ImageField named "image" """
	def thumb(self):
		if not self.image: return ""
		import art_cloud.front.templatetags.imagetags as imagetags
		import art_cloud.imaging as imaging
		try:
			file = settings.MEDIA_URL + self.image.path[len(settings.MEDIA_ROOT):]
			filename, miniature_filename, miniature_dir, miniature_url = imagetags.determine_resized_image_paths(file, "admin_thumb")
			if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
			if not os.path.exists(miniature_filename): imaging.fit_crop(filename, 100, 100, miniature_filename)
			return """<img src="%s" /></a>""" % miniature_url
		except:
			traceback.print_exc()
			return None
	thumb.allow_tags = True
	class Meta:
		abstract = True

