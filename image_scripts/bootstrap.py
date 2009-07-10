#!/usr/bin/python
"""This script is the bootstrap run at the end of rc.local."""
import logging
import urllib2
import sys
import os, os.path
import time

from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from boto.s3.key import Key

logger = logging.getLogger("bootstrapper")

METADATA_BASE_URL = 'http://169.254.169.254/2009-04-04/'
USER_DATA_PATH = '/mnt/user-data.txt'

WEBAPP_VOLUME_DEVICE = '/dev/sdh'
WEBAPP_MOUNT_POINT = '/webapp/'

def generate_user_data(volume_id, access_key_id, secret_access_key):
	return '%s,%s,%s' % (role, volume_id, access_key_id, secret_access_key)

def parse_user_data(user_data):
	tokens = user_data.split(',')
	if len(tokens) != 3: raise IOError('Could not parse the user data: %s' % user_data)
	return { 'volume_id':tokens[0], 'access_key_id':tokens[1], 'secret_access_key':tokens[2] }

def read_user_data_file(): return parse_user_data(open(USER_DATA_PATH).read())

def copy_from_bucket(bucket_name, key_name, access_key_id, secret_access_key, destination_path):
	s3_connection = S3Connection(access_key_id, secret_access_key)
	bucket = s3_connection.get_bucket(bucket_name, validate=True)
	key = Key(bucket)
	key.key = key_name
	key.get_contents_to_filename(destination_path)
	
def install_user_data():
	logger.debug("Installing user data")
	user_data = urllib2.urlopen('%suser-data' % METADATA_BASE_URL).read()
	parse_user_data(user_data) # sanity check
	f = open(USER_DATA_PATH, 'w')
	f.write(user_data)
	f.flush()
	f.close()

def fetch_instance_id():
	return urllib2.urlopen('%smeta-data/instance-id/' % METADATA_BASE_URL).read() 
	
class Bootstrapper:
	def __init__(self):
		self.user_data = read_user_data_file()
		self.ec2_connection = EC2Connection(self.user_data['access_key_id'], self.user_data['secret_access_key'])

	def mount_webapp(self):
		if os.path.exists(WEBAPP_MOUNT_POINT):
			logger.warning('The webapp mount point, %s, already exists.  Not mounting again.' % WEBAPP_MOUNT_POINT)
			return
		logger.debug('Mounting the webapp directory')
		try:
			self.ec2_connection.attach_volume(self.user_data['volume_id'], fetch_instance_id(), WEBAPP_VOLUME_DEVICE)
		except:
			logger.error('Could not attach the webapp volume %s to /dev/sdh' % self.user_data['volume_id'])
			return
		time.sleep(5)
		os.makedirs(WEBAPP_MOUNT_POINT)
		os.system('mount %s' % WEBAPP_MOUNT_POINT)
		
	def boot(self):
		self.mount_webapp()	
		os.system('service postgresql start')
		os.system('service httpd start')

if __name__ == "__main__":
	logger.setLevel(logging.DEBUG)
	logger.addHandler(logging.StreamHandler())
	try:
		install_user_data()
		bootstrapper = Bootstrapper()
		bootstrapper.boot()
	except:
		logger.exception('Error in flounder bootstrapper')
