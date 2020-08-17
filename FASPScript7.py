#  IMPORTS

from FASPRunner1 import FASPRunner1

fastRunner = FASPRunner1('FASPScript7', "./pipelineLog.txt")

query = """
SELECT mut.case_barcode subject, meta.file_gdc_id as drs_id, 
meta.file_gdc_url as tumor_bam_file_path,
clin.race, clin.age_at_diagnosis, clin.ethnicity
  
FROM `isb-cgc.TCGA_hg38_data_v0.Somatic_Mutation` as mut 
join `isb-cgc.TCGA_bioclin_v0.Clinical` as clin 
on clin.case_barcode = mut.case_barcode 
join `isb-cgc.GDC_metadata.rel24_GDCfileID_to_GCSurl` as meta 
on meta.file_gdc_id = mut.tumor_bam_uuid #OR meta.file_gdc_id = mut.normal_bam_uuid 

where mut.Hugo_Symbol = "JMJD1C" and clin.race = "ASIAN"

order by meta.file_gdc_id
limit 3"""

fastRunner.runQuery(query, 'JMJD1C query ')

    


	
	

	
	









