import os

import pyega3.pyega3 as ega

class EGAFileClient():
    ''' Class to handle EGA files. Simulates DRS GetObject'''
    
    def __init__(self, credentialsPath):
        *credentials, self.key = ega.load_credential(os.path.expanduser(credentialsPath))
        self.credentials = credentials
        self.token = ega.get_token(credentials)
    
    def getSize(self, identifier):
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier)
        return file_size
       
    def get_object(self, identifier):
        ''' DRS formatted details of an EGA file '''
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier)

        response = {
		   "access_methods": [
		      {
		         "access_id": "ega",
		         "region": "",
		         "type": "pyega3"
		      }
		   ],
		   "checksums": [
		      {
		         "checksum": check_sum,
		         "type": "md5"
		      }
		   ],
		   "created_time": "2020-02-26T18:01:43.252269",
		   "id": identifier,
		   "mime_type": "application/json",
		   "description": file_name,
		   "name": display_file_name,
		   "self_uri": "drs://egasim/{}".format(identifier),
		   "size": file_size,
		   "updated_time": "2020-02-26T18:01:43.252275"
		}
        return response

        
    def htsget(self, identifier, ref, start, end, type, saveTo ):
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier) 
        genomic_range_args = (ref, check_sum, start, end, type)
        print(display_file_name)
        print(genomic_range_args)
        ega.download_file_retry(self.credentials, identifier, display_file_name, file_name, file_size, check_sum, 3, self.key,
        saveTo, genomic_range_args, -1, 10)
