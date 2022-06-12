import os
import json
from PIL import Image, ImageDraw

class Creditor():
	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None):
		return
		
	@classmethod
	def creditorFactory(cls, settings=None, showCredits=None, pauseSecs=1):
		"""Instantiate a class that will issue credits for the steps of a FASP run."""
		if settings == None:
			with open(os.path.expanduser('./FASPSettings.json')) as json_file:
				settings = json.load(json_file)		
				
		if showCredits == None:
			showCredits = (settings['showCredits'])
		if showCredits:
			return EndCreditor()
		else:
			return  SilentCreditor()

	def __init__(self):
		creditsFile = os.path.dirname(os.path.abspath(__file__)) + '/credits/credits.json'
		with open(creditsFile) as json_file:
			data = json.load(json_file)
		self.imageDir = data['imageDir']
		self.credits = data['credits']
		self.debug = False
		self.issuedCredits = []
		
	def addRun(self):
		return
	
	def closeRun(self):
		return
		
	def creditClass(self, classToCredit):
		# for now classes will be in the same list
		self.creditFromList(classToCredit.__class__.__name__)


class SilentCreditor(Creditor):
	"""Most examples should use this implementation of Creditor"""
	
	def giveCredit(self, image, credit, speak=False, pauseSecs=0, voice=None, closeImage=True):
		return

	def creditFromList(self, what, voice=None, closeImage=True):
		return
		
	def creditClass(self, classToCredit, voice=None):
		return
	
	def rollCredits(self):
		return
	
class EndCreditor(Creditor):
	"""A Creditor to accumulate a list of credits to display an icon showing GA4GH standards used"""
	
	def __init__(self):
		super().__init__()
		self.allCredits = []
	
	def creditFromList(self, what):
		if what not in self.issuedCredits:
			self.issuedCredits.append(what)
		
	def rollCredits(self):
		''' List the credits '''
		#for c in self.allCredits[0]:
		for r in range(0,3):
			rowString = ''
			for runCredits in self.allCredits:
				c = runCredits[r]
				if c in self.credits:
					g4ghStd = self.credits[c]['g4ghStd']
				else:
					g4ghStd = False
				rowString += c.ljust(25)
			print(rowString)

	def __iconCell(self, cw=30, ch=20, lw=1, color=None):
		im = Image.new('RGB', (cw,ch), color=color)
		draw = ImageDraw.Draw(im) 
		draw.line((0,ch-lw, cw,ch-lw), fill='white', width=lw)
		draw.line((cw-lw,0, cw-lw,ch-lw), fill='white', width=lw)
		return im
		
	def getFASPicon(self, filePath=None):
		cols = len(self.allCredits)
		rows = 3
		ch =20  #cellHeight
		cw =rows*ch  #cellWidth
		ga4ghIcon = self.__iconCell(cw, ch, color="blue")
		nonIcon = self.__iconCell(cw, ch, color="lightgrey")
		final_im = Image.new('RGB', (cw * cols, ch * rows))
		x_offset = 0
		for rn in self.allCredits:
			y_offset = 0
			for cr in rn:
				if cr in self.credits:
					ga4ghStd = self.credits[cr]['g4ghStd']
				else:
					ga4ghStd = False
				if ga4ghStd:
					im = ga4ghIcon
				else:
					im = nonIcon
				final_im.paste(im, (x_offset,y_offset))
				y_offset += im.size[1]
			x_offset += cw

		if filePath != None: final_im.save(filePath)
		return final_im

	def addRun(self):
		self.issuedCredits = []
		
	def closeRun(self):
		self.allCredits.append(self.issuedCredits)		


if __name__ == "__main__":
	FASP_SETTINGS = os.getenv('FASP_SETTINGS')
	creditor = Creditor.creditorFactory(showCredits=True, pauseSecs=1, settings=FASP_SETTINGS)
	print ("Credits run by {}".format(type(creditor).__name__))
	for credit in creditor.credits.keys():
		creditor.creditFromList(credit)
	creditor.rollCredits()