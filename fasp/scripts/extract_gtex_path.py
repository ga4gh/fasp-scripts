import pandas as pd
import sys
import getopt


def extract_tree(filepath):
	df = pd.read_csv(filepath, sep='\t')
	#print(df)
	
	for v in df['specimen_id']:
		print(v)

def usage():
	print (sys.argv[0] +' -t tsvfile ')

def main(argv):


	try:
		opts, args = getopt.getopt(argv, "ht:", ["help", "tsvfile"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
	    if opt in ("-h", "--help"):
	        usage()
	        sys.exit()

	    elif opt in ("-t", "--table"):
	        extract_tree(arg)


			
if __name__ == "__main__":
    main(sys.argv[1:])
