import json
import requests
import pprint
import sys, getopt


class GA4GHRegistryClient:

	def __init__(self):
		self.hostURL = 'https://registry.ga4gh.org/v1'
	
	# Look for registered DRS services
	def getRegisteredServices(self, serviceType=None):
		servicesURL = "{}/services".format(self.hostURL)
		if serviceType == None:
			serviceType = 'all'
		else:
			servicesURL = '{}/services?type={}:*'.format(self.hostURL, serviceType)
		print('Searching the GA4GH registry for {} services'.format(serviceType))
		response = requests.get(servicesURL)
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

