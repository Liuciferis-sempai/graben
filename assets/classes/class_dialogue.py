import pygame as py
import assets.config as config
import assets.initialization as init
from assets.sprits import CHARACTERS

class Dialogue(py.sprite.Sprite):
	def __init__(self, dialogues, members):
		super().__init__()

		self.dialogue = dialogues
		self.members = members

		config.moving["forward"] = False
		config.moving["left"] = False
		config.moving["right"] = False
		config.moving["back"] = False
		config.moving["taking aim"] = False
		config.moving["run"] = False
		config.moving["fire"] = False

		config.moving["cut scene"] = True

		self.line = 0

		self.text_field = py.surface.Surface([config.window_size[0], config.CELL_SIZE*1.5])
		self.text_field.fill(config.COLOR_GREY)

		self.members_right = CHARACTERS[members[1].name.upper()]["PORTRAIT"]

		self.members_left = CHARACTERS[members[0].name.upper()]["PORTRAIT"]

		self.my_font = py.font.SysFont('Comic Sans MS', 30)

		self.speaker_name_surface = self.my_font.render(self.dialogue[self.line][1], False, config.COLOR_BLACK)
		self.text_surface = self.my_font.render(self.dialogue[self.line][0], False, config.COLOR_BLACK)
		
		init.dialogue = self
	
	def next(self):
		'''
		Следующий диалог
		'''
		self.line += 1
		if self.line >= len(self.dialogue):
			init.scripts.end_of_cut_scene()
			init.dialogue = None
			config.moving["cut scene"] = False
			self.kill()
			return
		self.speaker_name_surface = self.my_font.render(self.dialogue[self.line][1], False, config.COLOR_BLACK)
		self.text_surface = self.my_font.render(self.dialogue[self.line][0], False, config.COLOR_BLACK)

	def last(self):
		'''
		Предыдущий диалог
		'''
		self.line -= 1
		if self.line >= len(self.dialogue) or self.line < 0:
			return
		self.speaker_name_surface = self.my_font.render(self.dialogue[self.line][1], False, config.COLOR_BLACK)
		self.text_surface = self.my_font.render(self.dialogue[self.line][0], False, config.COLOR_BLACK)
	
	def draw(self):
		init.screen.blit(self.members_left, [0, config.window_size[1]-config.CELL_SIZE*3.5])
		init.screen.blit(self.members_right, [config.window_size[0]-config.CELL_SIZE, config.window_size[1]-config.CELL_SIZE*3.5])
		init.screen.blit(self.text_field, [0, config.window_size[1]-config.CELL_SIZE*1.5])
		init.screen.blit(self.speaker_name_surface, [config.CELL_SIZE//2, config.window_size[1]-config.CELL_SIZE*1.3])
		init.screen.blit(self.text_surface, [config.CELL_SIZE//2, config.window_size[1]-config.CELL_SIZE*1])