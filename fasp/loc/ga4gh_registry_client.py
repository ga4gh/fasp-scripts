import requests
import sys, getopt


class GA4GHRegistryClient:

	def __init__(self, url='https://registry.ga4gh.org/v1', debug=False):
		self.hostURL = url
		self.debug = debug
		
	# Look for registered DRS services
	def getRegisteredServices(self, type=None):
		registryURL = "{}/services".format(self.hostURL)
		if type == None:
			type = 'all'
		else:
			registryURL = 'https://registry.ga4gh.org/v1/services?type={}:*'.format(type)
		print('Searching the GA4GH registry for {} services'.format(type))
		if self.debug: print('Request url {}'.format(registryURL)) 
		response = requests.get(registryURL)
		services = response.json()
		return services




def usage():
	print (sys.argv[0] +' -a all -t type')

def main(argv):

	rc = GA4GHRegistryClient()

	try:
		opts, args = getopt.getopt(argv, "hat:", ["help", "all", "type"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()
	    elif opt in ("-a", "--all"):
	        services = rc.getRegisteredServices()
	        for s in services:
	        	print(s['name'])
	    elif opt in ("-t", "--type"):
	        services = rc.getRegisteredServices(arg)
	        for s in services:
	        	print(s['name'])



			
if __name__ == "__main__":
    main(sys.argv[1:])

