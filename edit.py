import os.path, pygame, map
from pygame.locals import *	


#Major TODOs:
#1. Click and add
#2. Save and Load

class Edit:
	#0 - main map, 1 - layer selection
	info_surf = 0
	info_font = 0
	key_cont = 0
	mode = 0
	show_info = 1
	num_maps = 0
	ed_map = 0
	ui = 0
	grab_id = -1
	#use n-1 for list
	cur_map = 1
	cur_lay = 1
	
	def __init__(self, nmap, num_maps):
		self.info_surf = pygame.Surface((200,200))
		self.info_font = pygame.font.SysFont("Ariel", 35, False, False)
		print "Initilizing editor"
		self.num_maps = num_maps
		self.ed_map = nmap
		self.ui = pygame.Surface((1024,600))
	
	def toggle_map(self, direction):
		#1 - left , 2 - right
		if direction == 2:
			if self.cur_map < self.num_maps:
				self.cur_map = self.cur_map + 1
		if direction == 1:
			if self.cur_map > 0:
				self.cur_map = self.cur_map - 1
	
	def handle_events(self, e):
		key = pygame.key.get_pressed()
		if key[K_LEFT]:
			self.ed_map.dx = self.ed_map.dx + 1
		if key[K_RIGHT]:
			self.ed_map.dx = self.ed_map.dx - 1
		if key[K_UP]:
			self.ed_map.dy = self.ed_map.dy + 1
		if key[K_DOWN]:
			self.ed_map.dy = self.ed_map.dy - 1
			
		if e.type == KEYDOWN:
			if e.key == K_z:
				self.toggle_map(1)
			elif e.key == K_x:
				self.toggle_map(2)
			elif e.key == K_s:
				print "saving"
				self.ed_map.save_map()
			elif e.key == K_i:
				self.show_info = 0
			elif e.key == K_m:
				self.mode = 0
			elif e.key == K_l:
				self.mode = 1
			elif e.key == K_1:
				self.cur_lay = 1
			elif e.key == K_2:
				self.cur_lay = 2
			return 1
		elif e.type == MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			tx = self.ed_map.dx
			ty = self.ed_map.dy
			if pos[0] <= self.ed_map.w*32 and pos[1] <= self.ed_map.h*32:
				if self.mode == 0:
					if self.grab_id > -1:
						cell = self.ed_map.layer[self.cur_lay-1]
						#Consecutive Cells
						#f(x,y) = width * y - (width - x)
						c = self.ed_map.h * ((pos[0]-tx)/32) - (self.ed_map.h - ((pos[1]-ty)/32)) + self.ed_map.h
						cell[c].id = self.grab_id
						self.ed_map.layer[self.cur_lay-1] = cell
				elif self.mode == 1:
					wh = self.ed_map.tinfo[self.cur_lay-1]
					self.grab_id = (wh[1]/32) * (pos[1]/32) - ((wh[1]/32) - (pos[0]/32)) + (wh[1]/32)
				return 1
		self.cont_key = 0 
		return 0

#	def get_graph_click(pos):
#		if( pos
	
		
	
	def get_ui_surface(self):
		ts = self.ed_map.tw
		if self.mode == 0:
			self.ui.blit(self.ed_map.get_map_surf(self.cur_lay),(0,0))
			tx = self.ed_map.dx
			ty = self.ed_map.dy
			for i in range(0, self.ed_map.h):
				pygame.draw.line(self.ui,(255,255,255),(0+tx,i*ts+ty),(self.ed_map.w*ts+tx,i*ts+ty))
			for j in range(0, self.ed_map.w):
				pygame.draw.line(self.ui,(255,255,255),(j*ts+tx,0+ty),(j*ts+tx,self.ed_map.h*ts+ty))
		elif self.mode == 1:
			wh = self.ed_map.tinfo[self.cur_lay-1]
			c = 0
			tgfx = self.ed_map.layer_gfx[self.cur_lay - 1]
			for i in range(0, wh[0] / ts):
				for j in range(0, wh[1]/ts):
					if c < len(tgfx):
						self.ui.blit(tgfx[c], (j*ts, i*ts))
						c = c + 1
			for i in range(0, wh[1]):
				pygame.draw.line(self.ui,(255,255,255),(0,i*ts),(wh[1]*ts,i*ts))
			for j in range(0, wh[0]):
				pygame.draw.line(self.ui,(255,255,255),(j*ts,0),(j*ts,wh[0]*ts))
		tmplaygfx = self.ed_map.layer_gfx[self.cur_lay-1]
		self.ui.blit(tmplaygfx[self.grab_id],pygame.mouse.get_pos())
		pygame.draw.rect(self.ui,(0,0,0),pygame.Rect(0,0,200,150))
		infotxt = str(pygame.mouse.get_pos()) 
		self.ui.blit(self.info_font.render((infotxt), True,(0,255,0)),(0,0))
		infotxt =  "Mode: " + str(self.mode)
		self.ui.blit(self.info_font.render((infotxt), True, (0,255,0)),(0,30))
		infotxt = "Layer: " + str(self.cur_lay - 1)	
		self.ui.blit(self.info_font.render((infotxt), True, (0,255,0)),(0,60))
		return self.ui
	
	#Get rid of the surfacce so we can update frame
	def trash_surface(self):
		self.ui.fill((0,0,0))
		self.ed_map.trash_surface()