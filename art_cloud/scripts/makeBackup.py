#!/usr/bin/python
import os
import datetime
import sys
import settings
from common_script import *

"""Creates a backup file of the form YYYY-MM-DD_HH-MM-SS-backup.tar in the directory specified by settings.BACKUP_ROOT.
	The file contains the media directories specified by settings.DYNAMIC_MEDIA_DIRS and a pg_dump of the database.
"""

def main():
	now = datetime.datetime.now()
	file_token = '%d-%02d-%02d_%02d-%02d-%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)

	sql_file = '%s-sql.gz' % file_token
	sql_path = '%s%s' % (settings.BACKUP_ROOT, sql_file)
	command = 'pg_dump -U %s %s | gzip > "%s"' % (settings.DATABASE_USER, settings.DATABASE_NAME, sql_path)
	if not call_system(command):
		print 'aborting'
		return

	media_file = '%s-media.tgz' % file_token
	media_path = '%s%s' % (settings.BACKUP_ROOT, media_file)
	command = 'cd "%s" && tar -czf "%s" %s' % (settings.MEDIA_ROOT, media_path, ' '.join(['"%s"' % media_dir for media_dir in settings.DYNAMIC_MEDIA_DIRS]))
	if not call_system(command):
		print 'aborting'
		return
	
	backup_file = '%s%s-backup.tar' % (settings.BACKUP_ROOT, file_token)
	command = 'cd "%s" && tar -czf "%s" "%s" "%s"' % (settings.BACKUP_ROOT, backup_file, media_file, sql_file)
	if not call_system(command):
		print 'aborting'
		return
	
	command = 'rm -f "%s" "%s"' % (media_path, sql_path)
	if not call_system(command): print 'Could not erase temp backup files'
	
	
	
if __name__ == '__main__':
	main()

# Copyright 2009 GORBET + BANERJEE (http://www.gorbetbanerjee.com/) Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.