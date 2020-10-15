''' update the pipeline log by querying workflow service for status'''
#  IMPORTS
import sys
import pandas as pd
from fasp.workflow import samtoolsSBClient 
from fasp.workflow import DNAStackWESClient 
from fasp.workflow import GCPLSsamtools 
from fasp.runner import FASPRunner 


def main(argv):

	faspRunner = FASPRunner()
	settings = faspRunner.settings
	logTable = pd.read_table(faspRunner.pipelineLogFile , dtype={'status':str})
	sbSystem = settings['SevenBridgesInstance']
	sbProject = settings['SevenBridgesProject']

	location = 'projects/{}/locations/{}'.format(settings['GCPProject'], settings['GCPPipelineRegion'])
	gcsam = GCPLSsamtools(location, settings['GCPOutputBucket'])
	wesClients = { 'samtoolsSBClient':samtoolsSBClient(sbSystem, sbProject),
					'DNAStackWESClient':DNAStackWESClient('~/.keys/DNAStackWESkey.json'),
					'GCPLSsamtools': gcsam}
	
	for i, row in logTable.iterrows(): 
		wesClientClassName = row["wesClient"]
		run_id = row["pipeline_id"]
		if run_id == 'paste here':
			logTable.at[i, 'status'] = 0
		else:
			if pd.isna(row["status"]) or row["status"].lower() == 'running':
				wc = wesClients[wesClientClassName]
				status = wc.getTaskStatus(row["pipeline_id"])
				print('Updated run:{} status:{}'.format(run_id, status))
				logTable.at[i, 'status'] = status
			
	logTable.to_csv('pipeline_w_status.txt', sep='\t', index=False)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









