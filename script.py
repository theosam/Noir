import sys

class Script:
	file = 0
	
	def __init__(self, filename=0):
		self.file = open(filename)
	
	#From a textfile. Return a value seperated by a chracter
	#flag = int for number, otherwise string
	def get_nvalue( self, name, flag, delimiter):
		for line in self.file:
			term = line.split(delimiter, 1)
			if term[0] == name:
				if flag == "int":
					self.file.seek(0,0)
					return int(term[1])
				else:
					self.file.seek(0,0)
					return term[1]
		self.file.seek(0,0)