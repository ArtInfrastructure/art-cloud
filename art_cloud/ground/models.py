from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User


class UserHydrationMeta:
	"""Sets up hydration for the Django auth User model"""
	attributes = ['id', 'username']
User.HydrationMeta = UserHydrationMeta

#class UserAPIMeta:
#	authorization = Authorization(read_own=True, update_own=True)
#User.APIMeta = UserAPIMeta

class ImageHydrationMeta:
	"""Sets up hydration for Django's image field"""
	element_name = 'image'
	attributes = ['name', 'width', 'height']
ImageFieldFile.HydrationMeta = ImageHydrationMeta
