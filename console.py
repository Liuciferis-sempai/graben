import assets.initialization as init
import assets.config as config
from assets.classes.class_character import *
from assets.classes.class_button import *
from assets.classes.class_weapon import *
from assets.classes.class_obstacle import *
import json
import pygame_textinput
import assets.sprits as sprits

class Console:
	'''
	Консоль для ввода команд
	'''
	def __init__(self):
		self.console_input_field = pygame_textinput.TextInputVisualizer(font_color=config.COLOR_RED)
		self.console_background = py.Surface([config.window_size[0], config.CELL_SIZE])
		self.console_background.fill(config.COLOR_GREY)
	
	def __processing_input(self):
		'''
		Обрабатывает ввод в консоль
		'''
		request = self.console_input_field.value.split()
		self.console_input_field.value = ""
		print(request)

		try:
			if request[0] == "godmode":
				if request[1] == "0":
					init.settings["chits"]["undead"] = False
				elif request[1] == "1":
					init.settings["chits"]["undead"] = True
			elif request[0] == "noclip":
				if request[1] == "0":
					init.settings["chits"]["noclip"] = False
				elif request[1] == "1":
					init.settings["chits"]["noclip"] = True
			init.scripts.save_settings()
		except IndexError:
			pass
	
	def opened(self):
		'''
		Обработка консоли
		'''
		events = py.event.get()

		clicked = False
		self.console_input_field.update(events)

		for event in events:
			if event.type == py.QUIT:
				config.running = False
			if event.type == py.MOUSEBUTTONDOWN:
				if event.button == 1:
					clicked = True
			if event.type == py.KEYDOWN:
				if event.key == py.K_CARET:
					self.console_input_field.value = ""
					if config.is_console_open:
						config.is_console_open = False
					else:
						config.is_console_open = True
				elif event.key == py.K_RETURN:
					self.__processing_input()

		buttons_group = None
		if config.state_of_the_game["main menu"]:
			buttons_group = init.buttons_on_main_menu
		elif config.state_of_the_game["game mode selection"]:
			buttons_group = init.buttons_game_mode_selection
		elif config.state_of_the_game["level selection"]:
			buttons_group = init.buttons_level_selection
		elif config.state_of_the_game["menu"]:
			buttons_group = init.buttons_menu
		
		if buttons_group != None:
			for button in buttons_group:
				button.draw()
				if clicked:
					if button.rect.collidepoint(py.mouse.get_pos()):
						button.click()

		init.screen.blit(self.console_background, (0, 0))
		init.screen.blit(self.console_input_field.surface, (config.CELL_SIZE, config.CELL_SIZE//2))