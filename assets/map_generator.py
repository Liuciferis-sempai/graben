import pygame as py
from assets.classes.class_obstacle import *
import assets.config as config
import assets.sprits as sprits
import assets.initialization as init

class Map:
	def __init__(self):
		self.cells_list = []
		self.blit_map()
	
	def map_translation(self):
		'''
		переводит карту из текстового формата в список объектов
		'''
		print("map translated")
		self.cells_list = []
		coord = [0, 0]
		for y, line in enumerate(init.game_map["map"]):
			for x, cell in enumerate(line):
				cell = Obstacle([coord[0]*config.CELL_SIZE, coord[1]*config.CELL_SIZE], [x, y], cell)
				if cell.coords in init.game_map["checkpoints"].values():
					cell.group = "2"
				elif cell.type in ["R", "t", "T", "z", "Z"]:
					cell.group = "4"
				self.cells_list.append(cell)
				coord[0] += 1
			coord[0] = 0
			coord[1] += 1

	def blit_map(self):
		'''
		Отрисовывает карту
		'''
		init.chr_collision.empty()
		init.bullet_collision.empty()
		init.chr_collision_and_bullet_collision.empty()
		init.no_collision.empty()
		init.interactive_cells.empty()

		coord = [0, 0]
		for y, line in enumerate(init.game_map["map"]):
			coord_y = config.zero_coordinate[1]+coord[1]*config.CELL_SIZE
			if coord_y + config.CELL_SIZE > 0 and coord_y < config.window_size[1]:
				for x in range(len(line)):
					temp_coord = [config.zero_coordinate[0]+coord[0]*config.CELL_SIZE, coord_y]
					if 0 <= temp_coord[0]+config.CELL_SIZE and temp_coord[0] < config.window_size[0]:
						for cell_in_list in self.cells_list:
							if cell_in_list.coords == [x, y]:
								cell_in_list.add_to_group()
								cell_in_list.rect.topleft = temp_coord
					coord[0] += 1
			coord[0] = 0
			coord[1] += 1
#o - dirt

#T - trench V
#t - trench G

#A - trench F

#Q - trench T1
#W - trench T2
#E - trench T3
#R - trench T4

#Z - trench G1
#U - trench G2
#I - trench G3
#P - trench G4

#l - dirt with barbwire (V)