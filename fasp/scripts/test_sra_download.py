import urllib.request
import shutil
import requests
...
# Download the file from `url` and save it locally under `file_name`:
    
from fasp.loc import sdlDRSClient


def download(url):

	print('in download')
	file_name = 'test_file.bam'
	

	req = requests.get(url)
	print (req)
	file = open(file_name, 'wb')
	for chunk in req.iter_content(100000):
		print('writing a chunk')
		file.write(chunk)
	file.close()

if __name__ == "__main__":
# 	client1 = sdlDRSClient('~/.keys/prj_14565.ngc')
# 	res = client1.getObject('SRR1999478.bam')
# 	print('--Get Info--')
# 	print (res)
# 	print('--Get a URL--')
# 	res = client1.getAccessURL('SRR1999478.bam','gs.us')
# 	print (res)
# 	print ('-----------------')
	client2 = sdlDRSClient('~/.keys/prj_11218_D17199.ngc', debug=True)
	res = client2.getObject('SRR5368359.sra')
	print('--Get Info--')
	print (res)
	print('--Get a URL--')
	res = client2.getAccessURL('SRR5368359.sra','gs.us')
	#print (json.dumps(res, indent=2))
	print (res['url'])
	download(res['url'])
