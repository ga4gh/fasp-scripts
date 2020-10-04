import pyega3.pyega3 as ega
import os

class htsgetTest():
    
    def __init__(self, credentialsPath):
        *credentials, self.key = ega.load_credential(os.path.expanduser(credentialsPath))
        self.credentials = credentials
        self.token = ega.get_token(credentials)
    
    def testhtsget(self, identifier, ref, start, end, type, saveTo ):
        display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(self.token, identifier) 
        genomic_range_args = (ref, check_sum, start, end, type)
        print(display_file_name)
        ega.download_file_retry(self.credentials, identifier, display_file_name, file_name, file_size, check_sum, 3, self.key,
        saveTo, genomic_range_args, -1, 10)


if __name__ == "__main__":
    tester = htsgetTest('~/.keys/ega.credentials')
    # pyega3  fetch -r chr1 -s 100000 -e 102000 -f BAM  --saveto test.bam  EGAF00001554180


    # try a file from the test account dataset
    tester.testhtsget('EGAF00001753744', 'chr1', 100000, 102000, 'CRAM', '~/EGAF00001753744.cram')

    # try a controlled access file
    tester.testhtsget('EGAF00001554145', 'chr1', 100000, 102000, 'BAM', '~/EGAF00001554145.bam')
   
