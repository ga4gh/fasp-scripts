import applescript
import os
import time
import subprocess, sys
import random
import json

class Creditor():
	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None):
		return

class SilentCreditor(Creditor):

	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None):
		return

	def creditFromList(self, what, voice=None):
		return
		
	def creditClass(self, classToCredit, voice=None):
		return

class DemoCredits(Creditor):
	
	def __init__(self, creditsFile, voice='Victoria', speak=False, pauseSecs=0):
		with open(os.path.expanduser(creditsFile)) as json_file:
   			 data = json.load(json_file)
		self.imageDir = data['imageDir']
		self.credits = data['credits']
		self.speak = speak
		self.pauseSecs = pauseSecs
		self.voice = voice

		self.issuedCredits = []
	
	def runAppleScript(self, applescript):
		args = [item for x in [("-e",l.strip()) for l in applescript.split('\n') if l.strip() != ''] for item in x]
		proc = subprocess.Popen(["osascript"] + args ,stdout=subprocess.PIPE )
		progname = proc.stdout.read().strip()
		sys.stdout.write(str(progname))

	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None):
		if voice == None:
			voice = self.voice
		
		# Show a picture	
		script = 'set x to open file "{}:{}"'.format(self.imageDir, image)
		r= applescript.tell.app("Preview", script)
		
		# show some text
		print(credit)
		
		# speak the credit if asked
		if speak:
			#command = '/usr/bin/say "{}"'.format(credit)
			script = 'say "{}" using "{}"'.format(credit, voice)
			#os.system(command)
			#print (script)
			#r= applescript.run(script)
			self.runAppleScript(script)
			
		# hold as requested
		if pauseSecs == 0:
			input ( "press any key to continue" )
		else:
			time.sleep(pauseSecs)
		
		# move on
		r= applescript.tell.app("Preview", 'close window 1')

	def creditFromList(self, what, voice=None):
		if what in self.issuedCredits:
			return
		if what in self.credits:
			credit = self.credits[what]
		else:
			genericMessage = 'I don\'t know how to give credit for {}'.format(what)
			credit = [self.credits['generic'],genericMessage]
		self.giveCredit(credit[0], credit[1], speak=self.speak, pauseSecs=self.pauseSecs, voice=voice)
		self.issuedCredits.append(what)
			
		
	def creditClass(self, classToCredit, voice=None):
		# for now classes will be in the same list
		self.creditFromList(classToCredit.__class__.__name__, voice)


if __name__ == "__main__":
	creditor = DemoCredits('./credits.json', speak=True, pauseSecs=1)

	voices = ["Victoria", "Alex", "Karen","Veena","Fiona", "Moira","Daniel"]
	for credit in creditor.credits.keys():
		creditor.creditFromList(credit, voice=random.choice(voices))