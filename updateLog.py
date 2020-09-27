''' update the pipeline log by querying workflow service for status'''
#  IMPORTS
import sys
import pandas as pd
from samtoolsSBClient import samtoolsSBClient 
from DNAStackWESClient import DNAStackWESClient 
from GCPLSsamtools import GCPLSsamtools 


def main(argv):

	logTable = pd.read_table("./pipelineLog.txt")
	
	# edit these to indicate your 
	sbSystem = 'cgc'
	sbProject = 'id/project'
	
	wesClients = { 'samtoolsSBClient':samtoolsSBClient(sbSystem, sbProject),
					'DNAStackWESClient':DNAStackWESClient('~/.keys/DNAStackWESkey.json'),
					'GCPLSsamtools':GCPLSsamtools('gs://isbcgc-216220-life-sciences/fasand/')}
	
	for i, row in logTable.iterrows(): 
		wesClientClassName = row["wesClient"]
		run_id = row["pipeline_id"]
		#print(run_id, wesClientClassName)
		if run_id == 'paste here':
			logTable.at[i, 'status'] = 'no id'
		else:
			if pd.isna(row["status"]) or row["status"].lower() == 'running':
				wc = wesClients[wesClientClassName]
				status = wc.getTaskStatus(row["pipeline_id"])
				print('Updated run:{} status:{}'.format(run_id, status))
				logTable.at[i, 'status'] = status
			
	logTable.to_csv('pipeline_w_status.txt', sep='\t', index=False)
    
if __name__ == "__main__":
    main(sys.argv[1:])
    


	
	

	
	









