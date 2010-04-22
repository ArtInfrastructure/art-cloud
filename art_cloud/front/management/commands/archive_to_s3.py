# Copyright 2010 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import os
import time
import urllib
import sys
import datetime
from boto.s3.connection import S3Connection
from boto.s3.key import Key

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
	help = "Copy a file up to an S3 bucket defined in the settings file."
	args = "[file_to_archive]"
	requires_model_validation = False

	def handle(self, *labels, **options):
		if not hasattr(settings, 'AWS_ACCESS_KEY'): raise CommandError('You must define AWS_ACCESS_KEY in settings.py')
		if not hasattr(settings, 'AWS_SECRET_KEY'): raise CommandError('You must define AWS_SECRET_KEY in settings.py')
		if not hasattr(settings, 'BACKUP_S3_BUCKET'): raise CommandError('You must define BACKUP_S3_BUCKET in settings.py')

		if not labels or len(labels) != 1: raise CommandError('Enter one argument, the file copy to S3.')
		source_path = os.path.realpath(labels[0])
		if not os.path.exists(source_path): raise CommandError('There is no file at "%s"' % source_path)
		if not os.path.isfile(source_path): raise CommandError('"%s" is not a file.' % source_path)

		s3_connection = S3Connection(settings.AWS_ACCESS_KEY, settings.AWS_SECRET_KEY)
		bucket = s3_connection.lookup(settings.BACKUP_S3_BUCKET)
		if bucket == None:
			bucket = s3_connection.create_bucket(settings.BACKUP_S3_BUCKET)
		k = Key(bucket)
		k.key = os.path.basename(source_path)
		k.set_contents_from_filename(source_path)


