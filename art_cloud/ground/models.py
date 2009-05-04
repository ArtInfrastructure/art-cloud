from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User


class UserHydrationMeta:
	attributes = ['id', 'username']
User.HydrationMeta = UserHydrationMeta

class ImageHydrationMeta:
	element_name = 'image'
	attributes = ['name', 'width', 'height']
ImageFieldFile.HydrationMeta = ImageHydrationMeta
