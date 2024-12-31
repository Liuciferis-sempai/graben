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

	def map_loader(self):
		'''
		Загружает карты из нужной папки
		'''
		self.maps = {}
		files = [f for f in os.listdir("maps") if f.endswith(".json")]
		for i, file_name in enumerate(files, start=1):
			path = resource_path(os.path.join("maps", file_name))
			with open(path, "r", encoding="utf-8") as file:
				self.maps[i] = json.load(file)
	
	def tutorial(self):
		pass
	
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
	
	def commissioners_speech(self):
		if not self.scripts_chekpoints["was_commissioners_speech"]:
			Dialogue(init.languages[init.settings["language"]]["COMMISSARS_SPEECH"], [init.player, Commissar("Boltgun", "Boltpistol", "Bayonet", "FragmentationGrenade", "no_ai", [0, 0], None)])
			self.scripts_chekpoints["was_commissioners_speech"] = True
			init.game_map["map"][2][8] = "s"
			init.game_map["map"][2][9] = "s"
	
	def descent_into_the_trenches(self):
		if not self.scripts_chekpoints["was_descent_into_the_trenches"]:
			self.scripts_chekpoints["was_descent_into_the_trenches"] = True
			init.game_map["map"][18][9] = "o"
			init.game_map["map"][18][10] = "o"
			init.game_map["map"][19][7] = "o"
			init.board.remove_character("all", "allie")
	
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
	
	def load_map(self, map_index: int):
		'''
		Загружает карту по индексу
		'''
		init.game_map = copy.deepcopy(self.maps[map_index])
		config.zero_coordinate = [config.CELL_SIZE*init.game_map["zero_point"][0], config.CELL_SIZE*init.game_map["zero_point"][1]]
		print(f"is loaded {init.game_map["map_name"]}")
		init.board.map.map_translation()
		self.load_allies()
		self.load_enemies()
	
	def load_allies(self):
		for allie in init.game_map["allies"]:
			allie_type = globals()[allie["self_type"]]
			self_allie = allie_type(allie["main_weapon"], allie["second_weapon"], allie["melee_weapon"], allie["grenade_type"], allie["ai_type"], allie["position"], allie["start_angle"], allie.get("waypoints", None))
			init.allies.add(self_allie)
			init.board.add_character(self_allie, "allie")

	def load_enemies(self):
		for enemy in init.game_map["enemies"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"], enemy.get("waypoints", None))
			init.enemies.add(self_enemy)
			init.board.add_character(self_enemy, "enemy")

		for enemy in init.game_map["enemies_tied_to_the_script"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"], enemy.get("waypoints", None))
			init.enemies.add(self_enemy)
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

	def show_messeg_on_display(self, messeg: str, position: list, font: int, color: tuple):
		'''
		Отображает сообщение на экране
		'''
		messeg = Messege(messeg, position, font, color, "SAVE CONFIRM")
		
		init.texts.append(messeg)
	
	def move_group(self, group: py.sprite.Sprite, dx: int, dy: int):
		"""
		Перемещает все спрайты в группе на dx по оси X и dy по оси Y
		"""
		for sprite in group:
			sprite.position[0] += dx
			sprite.position[1] += dy

			sprite.center[0] += dx
			sprite.center[1] += dy

class Messege(py.sprite.Sprite):
	def __init__(self, messeg: str, position: list, font: int, color: tuple, content: str):
		self.my_font = py.font.SysFont('Comic Sans MS', font)
		self.text_surface = self.my_font.render(messeg, False, color)
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