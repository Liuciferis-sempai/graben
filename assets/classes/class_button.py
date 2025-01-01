import pygame as py
import assets.config as config
import assets.initialization as init

class Button(py.sprite.Sprite):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку в нужной позиции, текст и размеры зависит от типа кнопки
		@position задаёт позицию кнопки
		'''
		super().__init__()
		self.position = position
		self.text = "NoText" if not hasattr(self, "text") else self.text
		self.width = config.CELL_SIZE*2 if not hasattr(self, "width") else self.width
		self.heidht = config.CELL_SIZE if not hasattr(self, "heidht") else self.heidht
		
		self.my_font = py.font.SysFont('Comic Sans MS', config.FONT_SIZE)
		self.text_surface = self.my_font.render(self.text, False, config.COLOR_WHITE)
		self.rect = py.Rect(position[0], position[1], self.width, self.heidht)
		self.surface = py.surface.Surface([self.width, self.heidht])
		self.surface.fill(config.COLOR_BLACK)

		self.available = True

		self.center = [self.position[0]+self.width//2-self.text_surface.get_width()//2, self.position[1]+self.heidht//2-config.FONT_SIZE]
	
	def click(self):
		print("NoAction")
	
	def draw(self):
		init.screen.blit(self.surface, self.position)
		init.screen.blit(self.text_surface, self.center)

#кнопки для главного меню
class StartGameButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для старта игры
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["START"]
		self.contents = "START"
		super().__init__(position)

		init.buttons_on_main_menu.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])
		config.state_of_the_game["main menu"] = False
		init.enemies.empty()
		init.allies.empty()
		init.items.empty()
		config.state_of_the_game["game mode selection"] = True
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])

class SettingsButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для открытия настроек
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["SETTINGS"]
		self.contents = "SETTINGS"
		super().__init__(position)

		init.buttons_on_main_menu.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[settings]: ", config.state_of_the_game["settings"])
		config.state_of_the_game["main menu"] = False
		config.state_of_the_game["settings"] = True
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[settings]: ", config.state_of_the_game["settings"])

class ShowStatistics(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для показа статистики игрока
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["SHOW_STATISTICS"]
		self.contents = "SHOW_STATISTICS"
		super().__init__(position)

		init.buttons_on_main_menu.append(self)

	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[statistics]: ", config.state_of_the_game["statistics"])
		config.state_of_the_game["main menu"] = False
		config.state_of_the_game["statistics"] = True
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[statistics]: ", config.state_of_the_game["statistics"])
		init.save["statistics"]["time in game"] += py.time.get_ticks() - config.last_time_update
		config.last_time_update = py.time.get_ticks()
		init.scripts.save_save()
		init.scripts.show_message_on_display(f"{init.languages[init.settings["language"]]["NUMBER_OF_DEATHS"]}: {init.save["statistics"]["number of deaths"]}", ["center", config.window_size[1]//2-config.CELL_SIZE], config.FONT_SIZE, config.COLOR_WHITE)
		init.scripts.show_message_on_display(f"{init.languages[init.settings["language"]]["NUMBER_OF_KILLS"]}: {init.save["statistics"]["number of kills"]}", ["center", config.window_size[1]//2], config.FONT_SIZE, config.COLOR_WHITE)
		time = init.save["statistics"]["time in game"]
		second = time // 1000
		minute = 0
		hour = 0
		while second > 60:
			second -= 60
			minute += 1
		while minute > 60:
			minute -= 60
			hour += 1
		init.scripts.show_message_on_display(f"{init.languages[init.settings["language"]]["TIME_IN_GAME"]}: {hour} h {minute} m {second} s", ["center", config.window_size[1]//2+config.CELL_SIZE], config.FONT_SIZE, config.COLOR_WHITE)

class ExitGameButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для выхода из игры
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["EXIT"]
		self.contents = "EXIT"
		super().__init__(position)

		init.buttons_on_main_menu.append(self)
	
	def click(self):
		config.running = False

#кнопки для статистики
class BackToMainMenuFromStatistics(Button):
	def __init__(self, position):
		'''
		Создаёт кнопку для возвращения в меню из статистики
		@position задаёт позицию
		'''
		self.text = init.languages[init.settings["language"]]["BACK"]
		self.contents = "BACK"
		super().__init__(position)

		init.buttons_statistics.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[statistics]: ", config.state_of_the_game["statistics"])
		config.state_of_the_game["main menu"] = True
		init.texts = []
		config.state_of_the_game["statistics"] = False
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[statistics]: ", config.state_of_the_game["statistics"])

#кнопки для настроек
class SaveSettingsButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для сохранения настроек
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["SAVE"]
		self.contents = "SAVE"
		super().__init__(position)

		init.buttons_settings.append(self)
	
	def click(self):
		init.old_settings = init.settings.copy()
		init.scripts.save_settings()
		init.texts = []

class BackToMainMenuFromSettingsButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возвращения в главное меню
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["BACK"]
		self.contents = "BACK"
		super().__init__(position)

		init.buttons_settings.append(self)
	
	def click(self):
		exit = False
		for text in init.texts:
			if text.content == "SAVE CONFIRM":
				init.settings = init.old_settings.copy()
				init.texts = []
				init.scripts.buttons_init()
				exit = True

		if init.settings != init.old_settings and not exit:
			init.scripts.show_message_on_display(init.languages[init.settings["language"]]["SETTINGS SAVE CONFIRM"], ["center", "center"], config.FONT_SIZE, config.COLOR_WHITE, "SAVE CONFIRM")
		else:
			print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[settings]: ", config.state_of_the_game["settings"])
			config.state_of_the_game["main menu"] = True
			config.state_of_the_game["settings"] = False
			print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[settings]: ", config.state_of_the_game["settings"])

class LanguageSelectionButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для выбора языка
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["LANGUAGE"]
		self.contents = "LANGUAGE"
		super().__init__(position)

		init.buttons_settings.append(self)
	
	def click(self):
		index = 0
		for i, language in enumerate(init.languages):
			if language == init.settings["language"]:
				index = i
				print("index: ", index)
				break
		if index+1 > len(init.languages)-1:
			init.settings["language"] = list(init.languages.keys())[0]
		else:
			init.settings["language"] = list(init.languages.keys())[index+1]
		init.scripts.buttons_init()

#кнопки для выбора режима игры
class BackToMainMenuFromModeMenuButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возвращения в главное меню
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["BACK"]
		self.contents = "BACK"
		super().__init__(position)

		init.buttons_game_mode_selection.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])
		config.state_of_the_game["main menu"] = True
		config.state_of_the_game["game mode selection"] = False
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])

class LevelSelectionButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для перехода к выбору уровня
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["LEVEL SELECTION"]
		self.contents = "LEVEL SELECTION"
		super().__init__(position)

		init.buttons_game_mode_selection.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[level selection]: ", config.state_of_the_game["level selection"])
		config.state_of_the_game["game mode selection"] = False
		config.state_of_the_game["level selection"] = True
		print("after click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[level selection]: ", config.state_of_the_game["level selection"])

class TutorialButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для перехода к обучению
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["TUTORIAL"]
		self.contents = "TUTORIAL"
		super().__init__(position)

		init.buttons_game_mode_selection.append(self)
	
	def click(self):
		import assets.maps as maps
		print("befor click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		config.state_of_the_game["game mode selection"] = False
		init.scripts.load_tutorial()
		config.state_of_the_game["game"] = True
		print("after click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])

class MapEditorButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для открытия эдитора для карты
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["EDITOR"]
		self.contents = "EDITOR"
		super().__init__(position)

		init.buttons_game_mode_selection.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[editor]: ", config.state_of_the_game["editor"])
		config.state_of_the_game["game mode selection"] = False
		config.state_of_the_game["editor"] = True
		print("after click: state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"], "/n", "state_of_the_game[editor]: ", config.state_of_the_game["editor"])

#кнопки для редактора карт
class MapChoiseButton(Button):
	def __init__(self, position: tuple, map_num: int):
		'''
		Создаёт кнопку для открытия выбранной карты
		@position задаёт позицию кнопки
		'''
		self.text = f"{init.languages[init.settings['language']]['LEVEL']} {map_num}"
		self.contents = f"LEVEL {map_num}"
		super().__init__(position)

		self.map_num = map_num

		init.buttons_editor.append(self)
	
	def click(self):
		init.editor.choise_map(self.map_num)

class CreateNewMap(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для создания новой карты
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings['language']]['NEW_MAP']
		self.contents = "NEW_MAP"
		super().__init__(position)

		init.buttons_editor.append(self)
	
	def click(self):
		init.editor.create_new_map()

class MapEdit(Button):
	def __init__(self, position: tuple):
		'''
		Открывает редактор карты
		'''
		self.text = init.languages[init.settings["language"]]["MAP_EDITING"]
		self.contents = "MAP_EDITING"
		super().__init__(position)

		init.buttons_editor.append(self)

	def click(self):
		init.editor.editing_map()

class BackToMainLocation(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возврата на основной экран редактора
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["BACK"]
		self.contents = "BACK"
		super().__init__(position)

		init.buttons_editor.append(self)
	
	def click(self):
		init.editor.back_to_main_location()

#кнопки для выбора уровней
class LevelStartButton(Button):
	def __init__(self, position: tuple, level_num: int):
		'''
		Создаёт кнопку для старта выбранного уровня
		@position задаёт позицию кнопки
		@level_num определяет какой MAP будет загружен из папки MAPS
		'''
		self.text = f"{init.languages[init.settings['language']]['LEVEL']} {level_num}"
		self.contents = f"LEVEL {level_num}"
		super().__init__(position)

		self.level_num = level_num

		if level_num > init.save["progress"]:
			self.available = False
			self.surface.fill(config.COLOR_DARK_GREY)

		init.buttons_level_selection.append(self)
	
	def click(self):
		if not self.available:
			return
		print("befor click: state_of_the_game[level selection]: ", config.state_of_the_game["level selection"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		config.state_of_the_game["level selection"] = False
		init.loaded_map = self.level_num
		init.scripts.load_map(self.level_num)
		init.scripts.reload()
		init.player.restart()
		init.gui.load_ico()
		config.state_of_the_game["game"] = True
		print("after click: state_of_the_game[level selection]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])

class BackToGameModeSelectionButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возвращения к выбору режима игры
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["BACK"]
		self.contents = "BACK"
		super().__init__(position)

		init.buttons_level_selection.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[level selection]: ", config.state_of_the_game["level selection"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])
		config.state_of_the_game["level selection"] = False
		config.state_of_the_game["game mode selection"] = True
		print("after click: state_of_the_game[level selection]: ", config.state_of_the_game["level selection"], "/n", "state_of_the_game[game mode selection]: ", config.state_of_the_game["game mode selection"])

#кнопки для меню
class ContinueButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возвращения в игру
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["CONTINUE"]
		self.contents = "CONTINUE"
		super().__init__(position)

		init.buttons_menu.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[menu]: ", config.state_of_the_game["menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		config.state_of_the_game["menu"] = False
		config.state_of_the_game["game"] = True
		print("after click: state_of_the_game[menu]: ", config.state_of_the_game["menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])

class RestartButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для перезапуска уровня
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["RESTART"]
		self.contents = "RESTART"
		super().__init__(position)

		init.buttons_menu.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[menu]: ", config.state_of_the_game["menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		config.state_of_the_game["menu"] = False
		init.scripts.load_map(init.loaded_map)
		init.player.restart()
		init.scripts.reload()
		config.state_of_the_game["game"] = True
		print("after click: state_of_the_game[menu]: ", config.state_of_the_game["menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])

class MainMenuButton(Button):
	def __init__(self, position: tuple):
		'''
		Создаёт кнопку для возвращения в главное меню
		@position задаёт позицию кнопки
		'''
		self.text = init.languages[init.settings["language"]]["MAIN MENU"]
		self.contents = "MAIN MENU"
		super().__init__(position)

		init.buttons_menu.append(self)
	
	def click(self):
		print("befor click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		config.state_of_the_game["main menu"] = True
		config.state_of_the_game["menu"] = False
		print("after click: state_of_the_game[main menu]: ", config.state_of_the_game["main menu"], "/n", "state_of_the_game[game]: ", config.state_of_the_game["game"])
		init.texts = []