#Given width, heigth, x, and y.
#To find consecutive number at x and y
#Use y*h - (w - x) if and only if h = w
import os, sys, pickle, script, pygame
from pygame.locals import *	

class Cell:
	id = 0
	
	def __init__(self,id):
		self.id = id
#dx - Scrolling to x. Hence, dx the change of x
#dy - Scrolling of y. "         " dy "                   " y
#lnum - layernumbers
#tw - tile width
#th - tile height
#cell - one tile entity
#layer_gfx - actual tile graphic
class Map:
	tinfo = []
	dx = 0
	dy = 0
	id = 0
	lnum = 4
	fname = ""
	tw = 32
	th = 32
	w = 30
	h = 10
	cell = []
	layer_gfx = []
	map_surf =  pygame.Surface((1024,600))
	wImg = []
	layer = [] # 0 - bg, 1 - soft, 2 - hard, 3 - item, 4 - character
	
	def __init__(self, id):
		print "Gathering map scripts"
		self.id = id
		tmpstr = "resources/map" + str(id)
		infoScript = script.Script(tmpstr + "/map.txt")
		self.w = infoScript.get_nvalue("WIDTH","int","=")
		self.h = infoScript.get_nvalue("HEIGHT","int","=")
		tmpstr = tmpstr + "/map.nmp"
		#TODO: Make opening map faster
		print "opening test map"
		if os.path.exists(tmpstr) == 0:
			self.fname = open(tmpstr, 'w+')
			for i in range(0,self.lnum):
				tmpmaplst = []
				for j in range(0,self.w):
					for k in range(0,self.h):
						tmpcell = Cell(0)
						tmpmaplst.append(tmpcell)
				self.layer.append(tmpmaplst)
			pickle.dump(self.layer,self.fname)
			print "no exists"
		else:
			print "exists"
			self.fname = open(tmpstr,'r+')
			self.layer= pickle.load(self.fname)
		#pull tiles off of images
		#TODO: When finish testing: 0 to self.lnum
		print "Gathering tiles"
		for i in range(1, 3):
			gfx_set = []
			tmpstr = "resources/map" + str(id)
			tmp_wImg = pygame.image.load( tmpstr +"/layer" + str(i) + ".png")
			self.tinfo.append((tmp_wImg.get_height(),tmp_wImg.get_width()))
			for j in range(0, tmp_wImg.get_height()/self.tw):
				for k in range(0, tmp_wImg.get_width()/self.th):
					gfx_set.append(self.slice_section(tmp_wImg,k*self.tw, j*self.tw, self.tw))
			self.wImg.append(tmp_wImg)
			self.layer_gfx.append(gfx_set)
			
	def save_map(self):
		tmpstr = "resources/map" + str(self.id)
		tmpstr = tmpstr + "/map.nmp"
		self.fname = open(tmpstr, 'w+')
		pickle.dump(self.layer,self.fname)
			
	def get_map_surf(self, lay_mode):
		#TODO: When finish testing: 0 to self.lnum
		for i in range(1, lay_mode + 1):
			c = 0
			tcell = self.layer[i-1]
			tgfx = self.layer_gfx[i-1]
			for j in range(0, self.w):
				for k in range(0, self.h):
					self.map_surf.blit(tgfx[tcell[c].id],(j*self.tw+self.dx,k*self.tw+self.dy))
					c = c + 1 
		return self.map_surf
	
	#Seperates big image files into seperate tiles.
	def slice_section(self,wImg, x, y, s):
		nSurface = pygame.Surface((s,s))
		for i in range(0, s):
			for j in range(0, s):
				nSurface.set_at((i,j),wImg.get_at((x+i,y+j)))
		return nSurface

	def trash_surface(self):
		self.map_surf.fill((0,0,0))
		
				