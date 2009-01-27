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

SCALE_WIDTH = 'w'
SCALE_HEIGHT = 'h'
RESIZED_IMAGE_DIR = 'resized_image'

def calc_scale(max_x, pair):
	x, y = pair
	new_y = (float(max_x) / x) * y
	return (int(max_x), int(new_y))

def crop(file, size_param="300x255"):
	"""Crop an image (no resizing)"""
	width_param, height_param = size_param.split('x')
	width = int(width_param)
	height = int(height_param)

	filename, miniature_filename, miniature_dir, miniature_url = determine_resized_image_paths(file, size_param)
	if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
	if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename): os.unlink(miniature_filename)

	if not os.path.exists(miniature_filename):
		image = Image.open(filename)
		image.save(miniature_filename, image.format)
		fit_crop(miniature_filename, width, height)
	return miniature_url
register.filter('crop', crop)

def squarecrop(file, size_param='100'):
	"""Crop a square image"""
	size = int(size_param.strip())

	filename, miniature_filename, miniature_dir, miniature_url = determine_resized_image_paths(file, "sq" + size_param)
	if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
	if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename): os.unlink(miniature_filename)

	# if the image wasn't already resized, resize it
	if not os.path.exists(miniature_filename):
		image = Image.open(filename)
		image.save(miniature_filename, image.format)
		fit_crop(miniature_filename, size, size)
	return miniature_url
register.filter('squarecrop', squarecrop)

def fit_image(file, size_param="300x300"):
	"""Fit an image into the dimensions with no change in height/width ratio"""
	if not file: return None
	width_param, height_param = size_param.split('x')
	width = int(width_param)
	height = int(height_param)

	filename, miniature_filename, miniature_dir, miniature_url = determine_resized_image_paths(file, 'fit_' + size_param)
	if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
	if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename): 
		os.unlink(miniature_filename)

	if not os.path.exists(miniature_filename):
		try:
			image = Image.open(filename)
			image.save(miniature_filename, image.format)
			fit(miniature_filename, width, height)
		except:
			print "Could not load %s" % filename
	return miniature_url
register.filter('fit_image', fit_image)

# Thumbnail filter based on code from http://batiste.dosimple.ch/blog/2007-05-13-1/
def thumbnail(file, size='300w'):
	if (size.lower().endswith(SCALE_HEIGHT)):
		mode = SCALE_HEIGHT
	else:
		mode = SCALE_WIDTH
	size = size[:-1]
	max_size = int(size.strip())

	filename, miniature_filename, miniature_dir, miniature_url = determine_resized_image_paths(file, size)
	if not os.path.exists(miniature_dir): os.makedirs(miniature_dir)
	if os.path.exists(miniature_filename) and os.path.getmtime(filename) > os.path.getmtime(miniature_filename): os.unlink(miniature_filename)

	if not os.path.exists(miniature_filename):
		try:
			image = Image.open(filename)
			image_x, image_y = image.size  
			if mode == SCALE_HEIGHT:
				image_y, image_x = calc_scale(max_size, (image_y, image_x))
			else:
				image_x, image_y = calc_scale(max_size, (image_x, image_y))
			image = image.resize((image_x, image_y), Image.ANTIALIAS) # .convert("L") is the Black and White hack
			image.save(miniature_filename, image.format)		
		except:
			print "Could not load image %s" % filename
	return miniature_url
register.filter('thumbnail', thumbnail)

def determine_resized_image_paths(file, size_mark):
	if file.find('.') == -1:
		basename = file
		format = ''
	else:
		basename, format = file.rsplit('.', 1)
	miniature = basename + "_" + size_mark + '.' + format
	miniature_nomedia = miniature[len(settings.MEDIA_URL):]
	file_nomedia = file[len(settings.MEDIA_URL):]
	filename = os.path.join(settings.MEDIA_ROOT, file_nomedia)

	resized_image_dir = os.path.join(settings.MEDIA_ROOT, RESIZED_IMAGE_DIR)
	miniature_filename = os.path.join(resized_image_dir, miniature_nomedia)
	miniature_dir = miniature_filename.rsplit('/', 1)[0]
	miniature_url = settings.MEDIA_URL + RESIZED_IMAGE_DIR + '/' + miniature_nomedia
	return (filename, miniature_filename, miniature_dir, miniature_url)
