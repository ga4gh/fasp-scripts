#  IMPORTS
import sys, getopt
import json
import datetime
import subprocess 

# a utility 
from FASPLogger import FASPLogger

# The implementations we're using
from Gen3DRSClient import crdcDRSClient
from GCPLSsamtools import GCPLSsamtools
from BigQuerySearchClient import BigQuerySearchClient


class FASPRunner1:

	def __init__(self, program, pipelineLogFile):
		# A log is helpful to keep track of the computes we've submitted
		self.pipelineLogger = FASPLogger(pipelineLogFile, program)
    	
	def runQuery(self, query, note):

		# Step 1 - Discovery
		# query for relevant DRS objects
		searchClient = BigQuerySearchClient()

		query_job = searchClient.runQuery(query)  # Send the query
	
		# Step 2 - DRS - set up a DRS Client
		drsClient = crdcDRSClient('~/.keys/CRDCAPIKey.json')
		
		# Step 3 - set up a class that runs samtools for us
		# providing the location where we the results to go
		mysam = GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')
	
		# workaround - see below
		commands = []
		
		# repeat steps 2 and 3 for each row of the query
		for row in query_job:

			print("subject={}, drsID={}".format(row[0], row[1]))
		
			# Step 2 - Use DRS to get the URL
			objInfo = drsClient.getObject(row[1])
			fileSize = objInfo['size']
			# we've predetermined we want to use the gs copy in this case
			url = drsClient.getAccessURL(row[1], 'gs')
		
			# Step 3 - Run a pipeline on the file at the drs url
			outfile = "{}.txt".format(row[0])
			#This should have allowed us to submit a pipeline - but the pipelines fail
			#response = mysam.runStats(url, outfile)
			#pipeline_id = response['name']
			# via = 'py'
			# This is the workaround - just create a shell script
			commands.append(mysam.statsCommandLine(url, outfile))
			via = 'sh'
			pipeline_id = 'paste here'

			time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
			self.pipelineLogger.logRun(time, via, note,  pipeline_id, outfile, str(fileSize),
				searchClient, drsClient, mysam)

		# Submit the jobs using our workaround
		shellscriptPath = "./workaround.sh"
		shellScript = open(shellscriptPath, "w")
		for line in commands:
			shellScript.write(line)
			shellScript.write("\n")
		shellScript.close()
		# finally! submit all our hard work
		subprocess.call(['sh', shellscriptPath])
	
		self.pipelineLogger.close()
    
if __name__ == "__main__":

	fastRunner = FASPRunner1(os.path.basename(__file__), "./pipelineLog.txt")

	query = """
	SELECT mut.case_barcode subject, meta.file_gdc_id as drs_id, 
  	meta.file_gdc_url as tumor_bam_file_path,
	clin.race, clin.age_at_diagnosis, clin.ethnicity,  
	FROM `isb-cgc.TCGA_hg38_data_v0.Somatic_Mutation` as mut 
	join `isb-cgc.TCGA_bioclin_v0.Clinical` as clin 
	on clin.case_barcode = mut.case_barcode 
	join `isb-cgc.GDC_metadata.rel24_GDCfileID_to_GCSurl` as meta 
	on meta.file_gdc_id = mut.tumor_bam_uuid #OR meta.file_gdc_id = mut.normal_bam_uuid 
	where mut.Hugo_Symbol = "JMJD1C" and clin.race = "ASIAN"
	order by mut.case_barcode
	limit 3"""
	fastRunner.runQuery(query, 'JMJD1C query ')

    


	
	

	
	









