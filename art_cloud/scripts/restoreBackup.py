#!/usr/bin/python
import os
import datetime
import sys
import tempfile
import settings
import shutil

from common_script import *

"""Restores the media and database from a backupfile created by makeBackup.py"""

DEBUG = False
def main():
	
	if len(sys.argv) == 1:
		print 'Usage: restoreBackup.py <backup-file.gz>'
		return
	backup_path = os.path.realpath(sys.argv[1])
	if not os.path.exists(backup_path):
		'does not exist: %s' % backup_path
	print 'restoring from %s' % backup_path

	# create the working directory
	working_dir = tempfile.mkdtemp('backup-temp')

	try:

		# untar the backup file, which should result in two files: sql and media
		command = 'cd "%s" && tar -xzf "%s"' % (working_dir, backup_path)
		if not call_system(command):
			print 'aborting'
			return

		# create a sub directory for the media, and untar it
		media_dir = '%s/media' % working_dir
		os.mkdir(media_dir)
		command = 'cd "%s" && tar -xzf %s/*-media.tgz' % (media_dir, working_dir)
		if not call_system(command):
			print 'aborting'
			return

		# move each media dir from the temp media dir into the project media dir
		for new_media_dir in os.listdir(media_dir):
			target_dir = '%s%s' % (settings.MEDIA_ROOT, new_media_dir)
			if os.path.exists(target_dir): shutil.rmtree(target_dir)
			shutil.move('%s/%s' % (media_dir, new_media_dir), target_dir)

		# now delete and recreate the database
		command = 'echo "drop database %s; create database %s; grant all on database %s to %s;" | psql -U %s' % (settings.DATABASE_NAME, settings.DATABASE_NAME, settings.DATABASE_NAME, settings.DATABASE_USER, settings.DATABASE_USER)
		if not call_system(command):
			print 'aborting'
			return

		# now load the SQL into the database
		command = 'gunzip -c %s/*-sql.gz | psql -U %s %s' % (working_dir, settings.DATABASE_USER, settings.DATABASE_NAME)
		if not call_system(command):
			print 'aborting'
			return

	finally:
		pass
		#shutil.rmtree(working_dir)
if __name__ == "__main__":
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.