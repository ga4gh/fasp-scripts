import sys
from fasp.loc import sbcgcDRSClient

sb_api_key_path = sys.argv[1]

client = sbcgcDRSClient(sb_api_key_path, "s3")
response = client.get_object('62b077884e3edb6b1c23c6f9')
file_name = response['name']
print(file_name)
if file_name == 'references-hs37d5-hs37d5.fasta':
    print ("Success!")