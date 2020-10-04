""" Script to check a task submitted via the seven bridges API and use DRS to 

"""
#  IMPORTS
import sys, getopt, os
from requests import get

import sevenbridges as sbg
from SBDRSClient import sbcgcDRSClient



def download(url, file_name):
    with open(file_name, "wb") as file:
        response = get(url)
        file.write(response.content)
        
def getTaskOutputs(task_id, ddir):
	config = sbg.Config(profile='cgc')
	api = sbg.Api(config=config)

	try:
		task = api.tasks.get(id=task_id)
		if task.status != 'COMPLETED':
			print ('Task status:{}'.format(task.status))
			sys.exit()

		for okey, oitem in task.outputs.items():
			print (okey)
			if oitem.__class__ == sbg.File:
				print(oitem.id)
				print(oitem.name)
				
				drsClient = sbcgcDRSClient('~/.keys/sevenbridges_keys.json')
				drsResponse = drsClient.getObject(oitem.id)
				print(drsResponse) 
				drsURL = drsClient.getAccessURL(oitem.id, 's3')
				dPath = os.path.expanduser(ddir+oitem.name)
				if ddir != None:
					download(drsURL, dPath)
				
			else:
				print(oitem)

	except sbg.NotFound as e:
		print('Task not found')
	except sbg.SbgError as e:
		print(e.__class__)
		print (e.message)


def main(argv):
   task_id = ''
   ddir = None
   try:
      opts, args = getopt.getopt(argv,"ht:d:")
   except getopt.GetoptError:
      print ('samtoolsSBResultClient.py -t <task_id> -d <download_dir>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('samtoolsSBResultClient.py -t <task_id> -d <download_dir>')
         sys.exit()
      elif opt in ("-t", "--task"):
         task_id = arg
      elif opt in ("-d", "--download_dir"):
         ddir = arg
    
   getTaskOutputs(task_id, ddir)


if __name__ == "__main__":
   main(sys.argv[1:])
   