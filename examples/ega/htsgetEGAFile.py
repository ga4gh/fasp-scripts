import pyega3.pyega3 as ega
import os

if __name__ == "__main__":
    
    # Command line equivalent is
    # pyega3  fetch -r chr1 -s 100000 -e 102000 -f BAM  --saveto test.bam  EGAF00001554180

    identifier = 'EGAF00001554145'
    *credentials, key = ega.load_credential(os.path.expanduser('~/.keys/ega.credentials'))
    token = ega.get_token(credentials)
    display_file_name, file_name, file_size, check_sum = ega.get_file_name_size_md5(token, identifier) 
    genomic_range_args = ('chr1', check_sum, 100000, 102000, 'BAM')
    print(display_file_name)
    
    ega.download_file_retry(credentials, identifier, display_file_name, file_name, file_size, check_sum, 3, key,
        '~/test.bam', genomic_range_args, -1, 10)

              
