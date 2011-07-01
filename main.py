#\!/usr/bin/env python
import pygame, sys
import map, player, script, menu, edit
from pygame.locals import *	

#Major TODOs:
#1. Timer (easy on CPU)

class Game:
	# 0 - Menu, 1 - Edit, 2 - Options?, 3 - New Game?, 4 - Load Game?
	mode = 1
	map_num = 0
	general_script = 0
	main_menu = 0
	edit_mode = 0
	mapp = []
	
	def __init__(self):
		print "reading scripts"
		self.main_menu = menu.Menu("scripts/main_menu.txt")
		self.general_script = script.Script("scripts/general.txt")
		self.map_num = self.general_script.get_nvalue("MAPNUM","int","=")
		print "intilizing game objects"
		self.player = player.Player()
		self.map = map.Map(1)
		self.edit_mode = edit.Edit(self.map, self.map_num)

def init():
	pygame.init()
	pygame.time.set_timer(USEREVENT+1, 1)
	windowSurface = pygame.display.set_mode((1024, 768), 0, 32)
	windowSurface.fill((0,0,0))
	pygame.display.update()
			
def process():
	init()
	#if pygame.display.mode_ok((1024,768), FULLSCREEN):
	screen = pygame.display.set_mode((1024,768),pygame.RESIZABLE,16)
	g = Game()
	while True:
		for event in pygame.event.get():
			g.edit_mode.handle_events(event)
			g.main_menu.direct_item(event)
			if(event.type == KEYUP):
				if event.key == K_q:
					return
			if (event.type == QUIT):
				pygame.quit()
				sys.exit()
		#Get rid of the surface by making screen black
		screen.fill((0,0,0))
		g.main_menu.menu_surface.fill((0,0,0))
		g.edit_mode.trash_surface()
		#Menu mode
		if g.mode == 0:
			screen.blit(g.main_menu.get_menu_surface(),(0,0))
		#Editing mode
		elif g.mode == 1:
			screen.blit(g.edit_mode.get_ui_surface(),(0,0))
			g.edit_mode.ui.scroll(-100,0)
		pygame.display.flip()
			
init()
process()

