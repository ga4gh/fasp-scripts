import applescript
import os
import time
import subprocess, sys
import random
import json

class Creditor():
	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None):
		return
		
	@classmethod
	def creditorFactory(cls, showCredits=None, pauseSecs=1):
		"""Instantiate a class that will issue credits for the steps of a FASP run."""
		with open(os.path.expanduser('./FASPSettings.json')) as json_file:
   			 settings = json.load(json_file)		
		if showCredits == None:
			showCredits = (settings['showCredits'])
		if showCredits:
			return DemoCredits('./credits/credits.json', speak=True, pauseSecs=pauseSecs)
		else:
			return  SilentCreditor()


class SilentCreditor(Creditor):
	"""Most examples should use this implementation of Creditor"""
	
	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None, closeImage=True):
		return

	def creditFromList(self, what, voice=None, closeImage=True):
		return
		
	def creditClass(self, classToCredit, voice=None):
		return

class DemoCredits(Creditor):
	'''Created for Sept 2020 plenary demos. Not written to have any general use beyond that. Dependent on local machine specifics. Beware!
	This is a candidate for generalization if it would prove useful to others
	'''
	
	def __init__(self, creditsFile, voice='Victoria', speak=False, pauseSecs=0):
		with open(os.path.expanduser(creditsFile)) as json_file:
   			 data = json.load(json_file)
		self.imageDir = data['imageDir']
		self.credits = data['credits']
		self.speak = speak
		self.pauseSecs = pauseSecs
		self.voice = voice
		self.debug = False
		
		self.issuedCredits = []
		#self.updateCreditsFile()

	def updateCreditsFile(self):	
		newCredits = {}
		for key, credit in self.credits.items():
			newCredit = {"imageFile":credit[0], "textCredit":credit[1], "phoneticCredit":credit[1],
			 "workStream":"ws", "driverProject":"dp", "g4ghStd":True}
			newCredits[key] = newCredit
		newDict = {'imageDir':self.imageDir, 'credits':newCredits}
		with open(os.path.expanduser('~/newCredits.json'), 'w') as json_file:
   			 json.dump(newDict, json_file)
   			 
	def runAppleScript(self, applescript):
		args = [item for x in [("-e",l.strip()) for l in applescript.split('\n') if l.strip() != ''] for item in x]
		proc = subprocess.Popen(["osascript"] + args ,stdout=subprocess.PIPE )
		progname = proc.stdout.read().strip()
		sys.stdout.write(str(progname))
		
	def formatCells(self, style):
		script = """
					set style object of (cell 2 of row 3 of sheet 1 of workbook "DemoBanner.xlsx") to style "{}" of workbook "DemoBanner.xlsx"
				""".format(style)
		r = applescript.tell.app("Microsoft Excel", script)


	def giveCredit(self, credit, speak=False, pauseSecs=0, voice=None, closeImage=True):
		if voice == None:
			voice = self.voice
		
		# Show a picture	
		imagePath = os.path.expanduser('{}/{}'.format(self.imageDir, credit['imageFile']))
		script = 'set x to open POSIX file "{}"'.format(imagePath)
		if self.debug:
			print(script)
		r= applescript.tell.app("Preview", script)
		
		# show some text
		print(credit['textCredit'])
		for k in  ['Work Stream','Driver Project']:
			if k in credit:
				print('{}:{}'.format(k, credit[k]))
		
		# show some text
		if 'Driver Project' in credit:
			script = 'set value of cell 2 of row 1 of sheet 1 of workbook "DemoBanner.xlsx" to "{}"'.format(credit['Driver Project'])
			r= applescript.tell.app("Microsoft Excel", script)
		if 'Work Stream' in credit:
			script = 'set value of cell 2 of row 2 of sheet 1 of workbook "DemoBanner.xlsx" to "{}"'.format(credit['Work Stream'])
			r= applescript.tell.app("Microsoft Excel", script)
		if 'Implementation' in credit:
			script = 'set value of cell 2 of row 3 of sheet 1 of workbook "DemoBanner.xlsx" to "{}"'.format(credit['Implementation'])
			r= applescript.tell.app("Microsoft Excel", script)
			if credit['g4ghStd']:
				self.formatCells('GA4GHStd')
			else:
				self.formatCells('GeneralAPI')				


		
		# speak the credit if asked
		if speak:
			#command = '/usr/bin/say "{}"'.format(credit)
			#os.system(command)
			script = 'say "{}" using "{}"'.format(credit['phoneticCredit'], voice)
			if self.debug:
				print (script)
			r= applescript.run(script)
			self.runAppleScript(script)
			
		# hold as requested
		if pauseSecs == 0:
			input ( "press any key to continue" )
		else:
			time.sleep(pauseSecs)
		
		# move on
		if closeImage:
			r= applescript.tell.app("Preview", 'close window 1')
		r= applescript.tell.app("Microsoft Excel", 'set value of range "B1:B3" of sheet 1 of workbook "DemoBanner.xlsx" to ""')
		self.formatCells('gaPlain')

	def creditFromList(self, what, voice=None, closeImage=True):
		if what in self.issuedCredits:
			return
		if what in self.credits:
			credit = self.credits[what]
		else:
			genericMessage = 'I don\'t know how to give credit for {}'.format(what)
			credit = [self.credits['generic'],genericMessage]
		self.giveCredit(credit, speak=self.speak, pauseSecs=self.pauseSecs, voice=voice, closeImage=closeImage)
		self.issuedCredits.append(what)
			
		
	def creditClass(self, classToCredit, voice=None):
		# for now classes will be in the same list
		self.creditFromList(classToCredit.__class__.__name__, voice)


if __name__ == "__main__":
	creditor = Creditor.creditorFactory(showCredits=True, pauseSecs=1)
	voices = ["Victoria", "Alex", "Karen","Veena","Fiona", "Moira","Daniel"]
	for credit in creditor.credits.keys():
		creditor.creditFromList(credit, voice=random.choice(voices))