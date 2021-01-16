''' Query to illustrate Anne's use case for variants related to a gene involved in a rare pediatric brain cancer'''
#  IMPORTS
import sys 

from fasp.runner import FASPRunner

# The implementations we're using
from fasp.loc import crdcDRSClient
from fasp.workflow import GCPLSsamtools
from fasp.search import BigQuerySearchClient


faspRunner = FASPRunner(pauseSecs=0)
settings = faspRunner.settings

searchClient = BigQuerySearchClient()
drsClient = crdcDRSClient('~/.keys/crdc_credentials.json','gs')
location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
mysam = GCPLSsamtools(location, settings['GCPOutputBucket'])	

faspRunner.configure(searchClient, drsClient, mysam)

query = """
SELECT mut.case_barcode subject, meta.file_gdc_id as drs_id, 
meta.file_gdc_url as tumor_bam_file_path,
clin.race, clin.age_at_diagnosis, clin.ethnicity
  
FROM `isb-cgc.TCGA_hg38_data_v0.Somatic_Mutation` as mut 
join `isb-cgc.TCGA_bioclin_v0.Clinical` as clin 
on clin.case_barcode = mut.case_barcode 
join `isb-cgc.GDC_metadata.rel24_GDCfileID_to_GCSurl` as meta 
on meta.file_gdc_id = mut.tumor_bam_uuid #OR meta.file_gdc_id = mut.normal_bam_uuid 

where mut.Hugo_Symbol = "JMJD1C" 

order by meta.file_gdc_id
limit 3"""

faspRunner.runQuery(query, 'JMJD1C query ')

    


	
	

	
	









