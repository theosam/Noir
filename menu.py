import pygame, sys
import script
from pygame.locals import *

class menu_item:
	menu_text = ""
	link_num = 0
	font = 0
	item_surface = 0
	def __init__(self, text, lnum):
		self.item_surface = pygame.Surface((36,36))
		self.font = pygame.font.Font(None, 36)
		self.menu_text = text
		self.link_num = lnum
		self.item_surface = self.font.render(self.menu_text,1,(255,0,0))

#TODO - Make menu look prettier
#TODO - Flexibility in user input

class Menu:
	menu_script = 0
	item_num = 0
	menu_item = []
	menu_surface = 0
	cur_item = 0
	
	
	def __init__(self, script_fname):
		print "Intitializing menu"
		self.menu_surface = pygame.Surface((640,480))
		self.menu_script = script.Script(script_fname)
		self.item_num = self.menu_script.get_nvalue("NUMITEMS","int","=")
		print self.item_num
		for i in range(1,self.item_num+1):
			tmp_string = "ITEM" + str( i )
			item_string = self.menu_script.get_nvalue(tmp_string, "string", "=")
			tmp_item = menu_item(item_string, i)
			self.menu_item.append(tmp_item)
			
	def get_menu_surface(self):
		#TODO: Remove newline boxes
		for i in range(0, self.item_num):
			pygame.Surface.blit(self.menu_surface, self.menu_item[i].item_surface, (100,100+i*36))
		pygame.draw.rect(self.menu_surface, (0,255,0),(90,100+self.cur_item*36,1000,36),1)
		return self.menu_surface
	
	def do_menu_action(self, menuID):
		a = 0
	
	def direct_item(self, event):
		if event.type == KEYUP:
			#print self.item_num
			if event.key == K_s:
				if self.cur_item+1 < self.item_num:
					self.cur_item = self.cur_item + 1
			if event.key == K_w:
				if self.cur_item > 0:
					self.cur_item = self.cur_item - 1
			#print self.cur_item
			#if event.key == K_ENTER:
			#	do_menu_action(self.cur_item)
	