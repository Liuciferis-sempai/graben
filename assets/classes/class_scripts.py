import assets.config as config
import pygame as py
import assets.initialization as init
from assets.classes.class_dialogue import Dialogue
import json
import os
from assets.classes.class_character import *
from assets.maps import *
from assets.classes.class_button import *
import copy
from assets.image_loader import resource_path

class Scripts:
	def __init__(self):
		self.script_index = 0

		self.scripts_chekpoints = {
			"was_commissioners_speech": False,
			"was_descent_into_the_trenches": False,
			"was_meet_world_eater": False,
			"was_end_fight_with_world_eater": False
		}
		self.maps = {}
		self.boss = None
		self.once = {}

	def map_loader(self):
		'''
		Загружает карты из нужной папки
		'''
		self.maps = {}
		files = [f for f in os.listdir("maps") if f.endswith("_map.json")]
		for i, file_name in enumerate(files, start=1):
			path = resource_path(os.path.join("maps", file_name))
			with open(path, "r", encoding="utf-8") as file:
				self.maps[i] = json.load(file)
	
	def player_action(self):
		'''
		Когда игрок хочет с чем то провзаимодействовать
		'''
		if init.board.group_for_action != []:
			if hasattr(init.board.group_for_action[0], "type"):
				if init.board.group_for_action[0].type in ["Q", "e"]:
					init.player.main_weapon.ammo_in_pocket = init.player.main_weapon.ammo_in_pocket_max
					init.player.main_weapon.ammo_in_weapon = init.player.main_weapon.ammo_in_weapon_max
					init.player.second_weapon.ammo_in_pocket = init.player.second_weapon.ammo_in_pocket_max
					init.player.second_weapon.ammo_in_weapon = init.player.second_weapon.ammo_in_weapon_max
					init.player.grenade_count = init.player.grenade_count_max
				elif init.board.group_for_action[0].type in ["E", "r"]:
					init.player.hp = config.PlAYER_MAX_HP
			elif hasattr(init.board.group_for_action[0], "weapon"):
				if init.board.group_for_action[0].weapon.name != init.player.active_weapon.name:
					init.player.active_weapon = init.board.group_for_action[0].weapon
			init.board.group_for_action.remove(init.board.group_for_action[0])
	
	def player_tracking(self):
		'''
		Отслеживает состояние игрока
		'''
		if init.game_map["map_name"] == "Tutorial":
			for text in init.texts:
				if text.content == "CELL ACTION EXPLANATION":
					if init.player.main_weapon.ammo_in_pocket == init.player.main_weapon.ammo_in_pocket_max and self.once.get("ammo_tracking", True):
						init.player.hp = 1
						self.once["ammo_tracking"] = False
						self.tutorial(9)
			if init.player.hp == config.PlAYER_MAX_HP and self.once.get("hp_tracking", True) and not self.once.get("ammo_tracking", True):
				self.once["hp_tracking"] = False
				self.tutorial(10)
	
	def tied_to_the_script_handler(self):
		'''
		Отслеживает количество особых противников (в особой категории enemies_tied_to_the_script) и при определённом количестве, вызывает определённый скрипт
		'''
		for checkpoint in init.game_map["tracked_checkpoints"]:
			if init.game_map["map_name"] == "Tutorial":
				if init.game_map["tracked_checkpoints"][checkpoint] == len(init.enemies_tied_to_the_script):
					if checkpoint == "tracked_checkpoint_1" and self.once.get("tracked_checkpoint_1", True):
						self.once["tracked_checkpoint_1"] = False
						self.tutorial(3)
					elif checkpoint == "tracked_checkpoint_2" and self.once.get("tracked_checkpoint_2", True):
						self.once["tracked_checkpoint_2"] = False
						self.tutorial(5)
					elif checkpoint == "tracked_checkpoint_3" and self.once.get("tracked_checkpoint_3", True):
						self.once["tracked_checkpoint_3"] = False
						self.tutorial(7)
	
	def tutorial(self, index: int):
		'''
		Выводит подсказки для обучения. Подсказка зависит от index
		'''
		if index == 0:
			init.player.grenade_count = 0
			init.player.main_weapon.ammo_in_weapon = 0
			init.player.main_weapon.ammo_in_pocket = 0
			self.show_message_on_display(init.languages[init.settings["language"]]["EXPLANATION_OF_MOVEMENT"], ["center", config.CELL_SIZE], config.FONT_SIZE, config.COLOR_BLACK, "MOVE EXPLANATION")
		elif index == 1:
			init.texts = []
		elif index == 2:
			init.player.main_weapon.ammo_in_weapon = 3
			init.player.main_weapon.ammo_in_pocket = 20
			self.show_message_on_display(init.languages[init.settings["language"]]["EXPLANATION_OF_SHOOTING"], ["center", config.CELL_SIZE], config.FONT_SIZE, config.COLOR_BLACK, "SHOOT EXPLANATION")
		elif index == 3:
			init.texts = []
			init.game_map["map"][9][19] = "R_90_2"
			init.board.map.map_translation()
		elif index == 4:
			init.player.grenade_type = FragmentationGrenade()
			init.player.grenade_count = 3
			self.show_message_on_display(init.languages[init.settings["language"]]["EXPLANATION_OF_GRENADE_THROWING"], ["center", config.CELL_SIZE], config.FONT_SIZE, config.COLOR_BLACK, "GRENADE EXPLANATION")
		elif index == 5:
			init.texts = []
			init.player.grenade_count = 0
			init.player.main_weapon.ammo_in_weapon = 0
			init.player.main_weapon.ammo_in_pocket = 0
			init.player.melee_weapon = Bayonet()
			init.game_map["map"][13][21] = "R_0_2"
			init.board.map.map_translation()
		elif index == 6:
			self.show_message_on_display(init.languages[init.settings["language"]]["EXPLANATION_OF_BAYONET"], ["center", config.CELL_SIZE], config.FONT_SIZE, config.COLOR_BLACK, "BAYONET EXPLANATION")
		elif index == 7:
			init.texts = []
			init.game_map["map"][13][28] = "R_0_2"
			init.board.map.map_translation()
		elif index == 8:
			self.show_message_on_display(init.languages[init.settings["language"]]["INTERACTION_WITH_CELLS"], ["center", config.CELL_SIZE], config.FONT_SIZE, config.COLOR_BLACK, "CELL ACTION EXPLANATION")
		elif index == 9:
			init.game_map["map"][11][32] = "R_90_2"
			init.board.map.map_translation()
			init.texts = []
		elif index == 10:
			init.game_map["map"][15][32] = "R_90_2"
			init.board.map.map_translation()
		elif index == 11:
			config.state_of_the_game["game"] = False
			config.state_of_the_game["level selection"] = True
			self.reload()
	
	def checkpoint(self, position: list):
		'''
		Функция вызывается при прохождении чекпоинта
		'''
		for checkpoint in init.game_map["checkpoints"]:
			if init.game_map["checkpoints"][checkpoint] == position:
				if init.game_map["map_name"] == "MAP_1":
					if checkpoint == "checkpoint_1":
						self.commissioners_speech()
					elif checkpoint in ["checkpoint_2", "checkpoint_3"]:
						self.descent_into_the_trenches()
					elif checkpoint == "checkpoint_4":
						self.meet_world_eater()
				if init.game_map["map_name"] == "Tutorial":
					if checkpoint == "checkpoint_1":
						self.tutorial(0)
					elif checkpoint == "checkpoint_2":
						self.tutorial(1)
					elif checkpoint == "checkpoint_3":
						self.tutorial(2)
					elif checkpoint == "checkpoint_4":
						self.tutorial(4)
					elif checkpoint == "checkpoint_5":
						self.tutorial(6)
					elif checkpoint == "checkpoint_6":
						self.tutorial(8)
					elif checkpoint == "checkpoint_7":
						self.tutorial(11)
	
	def commissioners_speech(self):
		if not self.scripts_chekpoints["was_commissioners_speech"]:
			Dialogue(init.languages[init.settings["language"]]["COMMISSARS_SPEECH"], [init.player, Commissar("Boltgun", "Boltpistol", "Bayonet", "FragmentationGrenade", "no_ai", [0, 0], None)])
			self.scripts_chekpoints["was_commissioners_speech"] = True
			init.game_map["map"][2][8] = "q_0_2"
			init.game_map["map"][2][9] = "q_0_2"
			init.board.map.map_translation()
	
	def descent_into_the_trenches(self):
		if not self.scripts_chekpoints["was_descent_into_the_trenches"]:
			self.scripts_chekpoints["was_descent_into_the_trenches"] = True
			init.game_map["map"][18][9] = "o"
			init.game_map["map"][18][10] = "o"
			init.game_map["map"][19][7] = "o"
			init.board.remove_character("all", "ally")
	
	def meet_world_eater(self):
		if not self.scripts_chekpoints["was_meet_world_eater"]:
			init.game_map["map"][25][23] = "b"
			self.boss = WorldEaater("Boltrifle", "Boltpistol", "Bayonet", "FragmentationGrenade", "charger", [29, 25], 90)
			Dialogue(init.languages[init.settings["language"]]["MEET_WORLD_EATER"], [init.player, self.boss])
			self.scripts_chekpoints["was_meet_world_eater"] = True
			init.gui.is_boss_fight = True
			init.gui.boss = self.boss
			init.enemies.add(self.boss)
			init.board.add_character(self.boss, "boss")
	
	def end_fight_with_world_eater(self):
		if not self.scripts_chekpoints["was_end_fight_with_world_eater"]:
			self.scripts_chekpoints["was_end_fight_with_world_eater"] = True
			salamander = Salamander()
			salamander.name = "salamander"
			Dialogue(init.languages[init.settings["language"]]["SPEECH_BETWEEN_WORLD_EATER_AND_SALAMANDERS"], [salamander, self.boss])
	
	def end_of_cut_scene(self):
		if self.scripts_chekpoints["was_end_fight_with_world_eater"]:
			print(self.boss)
			init.board.remove_character(self.boss, "boss")
			self.boss.kill()
			init.gui.is_boss_fight = False
			init.gui.boss = None
			if init.save["progress"] == 1:
				init.save["progress"] += 1
				self.save_save()
			config.state_of_the_game["game"] = False
			config.state_of_the_game["level selection"] = True
			self.reload()

	def game_over(self):
		'''
		Функция вызывается при проигрыше
		'''
		config.state_of_the_game["game"] = False
		init.items.empty()
		init.bullets.empty()
		init.enemies.empty()
		init.allies.empty()
		init.board.remove_character("all", "ally")
		init.board.remove_character("all", "enemy")
		init.board.remove_character("all", "boss")
		config.state_of_the_game["menu"] = True
	
	def save_settings(self):
		'''
		Сохраняет настройки в файл
		'''
		with open("settings.json", "w") as file:
			json.dump(init.settings, file)
	
	def save_save(self):
		'''
		Сохроняет сохранение
		'''
		with open("saves\save.json", "w") as file:
			json.dump(init.save, file)
	
	def load_settings(self):
		'''
		Загружает настройки из файла
		'''
		with open("settings.json", "r", encoding="utf-8") as file:
			init.settings = json.load(file)
		
	def load_languages(self):
		'''
		Загружает языки из файла
		'''
		with open("assets\languages.json", "r", encoding="utf-8") as file:
			init.languages = json.load(file)
	
	def load_save(self):
		'''
		Загружает сохранение
		'''
		with open("saves\save.json", "r", encoding="utf-8") as file:
			init.save = json.load(file)
	
	def load_tutorial(self):
		'''
		Загружает обучающий уровень
		'''
		with open("maps\Tutorial.json", "r", encoding="utf-8") as file:
			init.game_map = json.load(file)
		config.zero_coordinate = [config.CELL_SIZE*init.game_map["zero_point"][0], config.CELL_SIZE*init.game_map["zero_point"][1]]
		print(f"is loaded {init.game_map["map_name"]}")
		init.board.map.map_translation()
		init.board.map.blit_map()
		self.load_allies()
		self.load_enemies()
		init.player.restart()
	
	def load_map(self, map_index: int):
		'''
		Загружает карту по индексу
		'''
		init.game_map = copy.deepcopy(self.maps[map_index])
		config.zero_coordinate = [config.CELL_SIZE*init.game_map["zero_point"][0], config.CELL_SIZE*init.game_map["zero_point"][1]]
		print(f"is loaded {init.game_map["map_name"]}")
		init.board.map.blit_map()
		self.load_allies()
		self.load_enemies()
		init.player.restart()

	def load_allies(self):
		for ally in init.game_map["allies"]:
			ally_type = globals()[ally["self_type"]]
			self_ally = ally_type(ally["main_weapon"], ally["second_weapon"], ally["melee_weapon"], ally["grenade_type"], ally["ai_type"], ally["position"], ally["start_angle"], ally.get("waypoints", None))
			init.allies.add(self_ally)
			init.board.add_character(self_ally, "ally")

	def load_enemies(self):
		for enemy in init.game_map["enemies"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"], enemy.get("waypoints", None))
			init.enemies.add(self_enemy)
			init.board.add_character(self_enemy, "enemy")

		for enemy in init.game_map["enemies_tied_to_the_script"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"], enemy.get("waypoints", None))
			init.enemies_tied_to_the_script.add(self_enemy)
			init.board.add_character(self_enemy, "enemy")

	def buttons_init(self):
		'''
		Инициализирует кнопки
		'''
		init.buttons_on_main_menu = []
		init.buttons_game_mode_selection = []
		init.buttons_level_selection = []
		init.buttons_menu = []
		init.buttons_settings = []
		init.buttons_statistics = []

		#Создание кнопок для стартового меню
		StartGameButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE*2])
		SettingsButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE//2])
		ShowStatistics([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2+config.CELL_SIZE])
		ExitGameButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2+config.CELL_SIZE*2+config.CELL_SIZE//2])

		#Создание кнопок для статистики
		BackToMainMenuFromStatistics([config.CELL_SIZE//4, config.window_size[1]-config.CELL_SIZE-config.CELL_SIZE//4])

		#Создание кнопок для настроек
		SaveSettingsButton([config.window_size[0]-config.CELL_SIZE*2-config.CELL_SIZE//4, config.window_size[1]-config.CELL_SIZE-config.CELL_SIZE//4])
		BackToMainMenuFromSettingsButton([config.CELL_SIZE//4, config.window_size[1]-config.CELL_SIZE-config.CELL_SIZE//4])

		LanguageSelectionButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE*2])

		#Создание кнопок для выбора режима игры
		TutorialButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE*2])
		LevelSelectionButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE//2])
		MapEditorButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2+config.CELL_SIZE])
		BackToMainMenuFromModeMenuButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2+config.CELL_SIZE*2.5])

		#Создание кнопок для выбора уровня
		for i in range(len(self.maps)):
			LevelStartButton([config.window_size[0]//2-config.CELL_SIZE, (i+1)*config.CELL_SIZE//4+i*config.CELL_SIZE], i+1)
		BackToGameModeSelectionButton([config.CELL_SIZE//4, config.window_size[1]-config.CELL_SIZE-config.CELL_SIZE//4])

		#Создание кнопок для меню
		ContinueButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE*2])
		RestartButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE*2])
		MainMenuButton([config.window_size[0]//2-config.CELL_SIZE, config.window_size[1]//2-config.CELL_SIZE//2])

	def reload(self):
		'''
		Перезапускает скрипты
		'''
		for scripts_checkpoint in self.scripts_chekpoints:
			self.scripts_chekpoints[scripts_checkpoint] = False
		for moving in config.moving:
			config.moving[moving] = False
		if self.boss != None:
			init.board.remove_character(self.boss, "boss")
			self.boss.kill()
			init.gui.is_boss_fight = False
			init.gui.boss = None
		init.items.empty()
		init.bullets.empty()
		init.enemies.empty()
		init.allies.empty()
		init.board.remove_character("all", "ally")
		init.board.remove_character("all", "enemy")

	def show_message_on_display(self, message: str, position: list, font: int, color: tuple, content: str):
		'''
		Отображает сообщение на экране
		'''
		message = Message(message, position, font, color, content)
		
		init.texts.append(message)
	
	def move_group(self, group: py.sprite.Sprite, dx: int, dy: int):
		"""
		Перемещает все спрайты в группе на dx по оси X и dy по оси Y
		"""
		for sprite in group:
			sprite.position[0] += dx
			sprite.position[1] += dy

			sprite.center[0] += dx
			sprite.center[1] += dy

class Message(py.sprite.Sprite):
	def __init__(self, message: str, position: list, font: int, color: tuple, content: str):
		self.my_font = py.font.SysFont('Comic Sans MS', font)
		self.text_surface = self.my_font.render(message, False, color)
		self.content = content
		if isinstance(position[0], int) and isinstance(position[1], int):
			pass
		elif isinstance(position[0], int):
			if position[1] == "center":
				position[1] = config.window_size[1] // 2 - self.text_surface.get_width() // 2
		elif isinstance(position[1], int):
			if position[0] == "center":
				position[0] = config.window_size[0] // 2 - self.text_surface.get_width() // 2
		else:
			position[1] = config.window_size[1] // 2 - self.text_surface.get_width() // 2
			position[0] = config.window_size[0] // 2 - self.text_surface.get_width() // 2
		self.position = position

	def draw(self):
		init.screen.blit(self.text_surface, self.position)