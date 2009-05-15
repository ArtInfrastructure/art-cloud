import os
import re
import traceback
import Image
from django.template import Library
from django import template
from django.utils.html import linebreaks
from django.conf import settings

from art_cloud.imaging import fit,fit_crop

register = template.Library()

def __dir(thing):
	"""List the attributes of an object by calling dir() on it."""
	return dir(thing)
register.filter('dir', __dir)