from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User


class UserHydrationMeta:
	attributes = ['id', 'username']
User.HydrationMeta = UserHydrationMeta

#class UserAPIMeta:
#	authorization = Authorization(read_own=True, update_own=True)
#User.APIMeta = UserAPIMeta

class ImageHydrationMeta:
	element_name = 'image'
	attributes = ['name', 'width', 'height']
ImageFieldFile.HydrationMeta = ImageHydrationMeta
