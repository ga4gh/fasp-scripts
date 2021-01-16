import datetime
import os


from fasp.search import BigQuerySearchClient

class FASPLogger:


	def __init__(self,  filePath, program):
		self.program = program
		self.full_path = os.path.expanduser(filePath)
		if not os.path.exists(self.full_path):
			log = open(self.full_path, "w")
			# write a header
			header = '{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format('time','status','via',
			'script', 'note', 'pipeline_id', 'outfile', 'fileSize',
			'ssearchClient','drsClient','wesClient')
			log.write(header)
			log.write("\n")


	def logRun(self, time, via, note, pipeline_id, outfile, fileSize, 
		searcher, finder, computer):
		
		searchClass = searcher.__class__.__name__
		drsClass = finder.__class__.__name__
		computeClass = computer.__class__.__name__
		
		log = open(self.full_path, "a")
		
		logline = '{}\t\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(time, via,
			self.program, note, pipeline_id, outfile, fileSize,
			searchClass, drsClass, computeClass)
		log.write(logline)
		log.write("\n")
		log.close()
				

if __name__ == "__main__":
	dummy = BigQuerySearchClient()		
	fl = FASPLogger( './testlog.txt', 'me')
	via = 'py'
	note = 'testing'
	time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
	pipeline_id = '123456'
	outfile = 'text.txt'
	fileSize = 100;
	fl.logRun(time, via, note, pipeline_id, outfile, fileSize, dummy, dummy, dummy)