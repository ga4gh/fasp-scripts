""" Script to submit a task

        To set your CGC credentials on the API, you will need an authentication token, which you can obtain from
        https://cgc.sbgenomics.com/account/#developer. 
        This code assumes you store your key in ~/.sevenbridges
        

        for questions contact: Ian Fore
"""

import time
import json
import sevenbridges as sbg


class samtoolsSBClient:

	def __init__(self, instance, project):
		#self.outdir = outdir
		self.project_id = project
		config = sbg.Config(profile=instance)
		self.api = sbg.Api(config=config)
#		try:
		project = self.api.projects.get(id=self.project_id)
		print ("Found " + project.name)
#		except SbgError as e:
#			print (e.message)

	def runWorkflow(self, bamURL, outfile):
		api = self.api
		# Task name in my project
		name = 'samtools_test'

		# App I want to use to run a task
		app = 'forei/gecco/samtools-stats-1-8-url'

		# Inputs
		inputs = {}
		
		inputs['alignment_file_url'] = bamURL
		inputs['output_file_path'] = outfile
		# static for now
		inputs['reference_file'] = api.files.get('5bad6c83e4b0abc138917143')

		task = api.tasks.create(name=name, project=self.project_id, app=app, inputs=inputs, run=True)
		return task.id


if __name__ == "__main__":
	sbApp = 'cgc'	# NCI Cancer Genomics Cloud
	project = 'forei/gecco'
	
	myClient = samtoolsSBClient(sbApp, project)

	drsurl = "s3://sddp-phs001554/117438.recal.cram"
	task = myClient.runWorkflow(drsurl)
	print('task.id: {}'.format(task))


