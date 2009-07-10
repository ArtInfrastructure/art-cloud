#!/usr/bin/python
import os
import sys
from datetime import date

def main():
	pem_file = '/mnt/pk.pem'
	cert_file = '/mnt/cert.pem'
	platform = 'i386'

	try:
		bucket = sys.argv[1]
		account_id = sys.argv[2]
		access_key = sys.argv[3]
		secret_key = sys.argv[4]
	except IndexError:
		print 'usage: makeImage.py <BUCKET_NAME> <USER_ID> <ACCESS_KEY> <SECRET_KEY>'
		return 

	ec2_path = '/usr/local/bin/' #use trailing slash

	days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
	manifest = days[date.today().weekday()]

	step_1 = 'rm -f /mnt/%s*' % (manifest,)
	step_2 = '%sec2-bundle-vol -p %s -d /mnt -k %s -c %s -u %s -r %s -e /root/.bash_history' % (ec2_path, manifest, pem_file, cert_file, account_id, platform)
	step_3 = '%sec2-upload-bundle -b %s -m /mnt/%s.manifest.xml -a %s -s %s' % (ec2_path, bucket, manifest, access_key, secret_key)

	print step_1
	os.system(step_1)
	print step_2
	os.system(step_2)
	print step_3
	os.system(step_3)

if __name__ == '__main__':
	main()

