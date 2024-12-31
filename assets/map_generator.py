import pygame as py
from assets.classes.class_obstacle import *
import assets.config as config
import assets.sprits as sprits
import assets.initialization as init

class Map:
	def __init__(self):
		self.map_translation()

	def map_translation(self):
		'''
		переводит карту из текстового формата в список объектов
		'''
		init.obstacles.empty()
		self.cells_list = []
		coord = [0, 0]
		for y, line in enumerate(init.game_map["map"]):
			for x, cell in enumerate(line):
				if True:
					temp_coord = [config.zero_coordinate[0]+coord[0]*config.CELL_SIZE, config.zero_coordinate[1]+coord[1]*config.CELL_SIZE]
					if temp_coord[0] > 0 or temp_coord[0]+config.CELL_SIZE > 0:
						if temp_coord[0] > config.window_size[0] or temp_coord[1] > config.window_size[1]:
							break
						if temp_coord[1] > 0 or temp_coord[1]+config.CELL_SIZE > 0:
							cell = Obstacle(temp_coord, [x, y], cell)
							self.cells_list.append(cell)
							init.obstacles.add(cell)
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