''' base class for a WES Client'''
class WESClient:

    
	def __init__(self, api_url_base):
		self.api_url_base = api_url_base


	def runWorkflow(self, fileurl):
		# use a temporary file to write out the input file
		inputJson = {"md5Sum.inputFile":fileurl}
		return None
