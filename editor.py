import assets.initialization as init
import assets.config as config
from assets.classes.class_character import *
from assets.classes.class_button import *
from assets.classes.class_weapon import *
from assets.classes.class_obstacle import *
import json
import pygame_textinput
import assets.sprits as sprits

class EditorScreen:
	def __init__(self):
		init.scripts.map_loader()
		for i in range(len(init.scripts.maps)):
			MapChoiseButton([config.window_size[0]//2-config.CELL_SIZE, (i+1)*config.CELL_SIZE//4+i*config.CELL_SIZE], i+1)
		CreateNewMap([config.window_size[0]//2-config.CELL_SIZE, (i+2)*config.CELL_SIZE//4+(i+1)*config.CELL_SIZE])
		self.map_num = 0
		self.max_map_index = (i+2)
		self.data = {
			"map_name": f"MAP_{self.max_map_index}",
			"map": [],
			"zero_point": [0, 0],
			"player_main_weapon": "Weapon",
			"player_secondary_weapon": "Weapon",
			"player_grenade_type": "Weapon",
			"player_melee_weapon": "Weapon",
			"checkpoints": {},
			"allies": [],
			"enemies": [],
			"enemies_tied_to_the_script": []
		}
		self.input_fields = []
		self.camera_moving = {
			"up": False,
			"down": False,
			"left": False,
			"right": False
		}
		self.selected_cell = None
		self.cell_list = []
		self.s_cell_list = []
		self.c_cell_list = []
		self.character_list = []
	
	def choise_map(self, map_num: int):
		'''
		Выбирает нужную карту
		'''
		self.map_num = map_num
		self.open_map()
	
	def open_map(self):
		'''
		Загружает карту по индексу
		'''
		with open(f"maps\map_{self.map_num}.json", "r", encoding="utf-8") as file:
			self.data = json.load(file)
		self.editing_start()

	def create_new_map(self):
		'''
		Создаёт новую карту
		'''
		self.map_num = self.max_map_index
		with open(f"maps\map_{self.max_map_index}.json", "w", encoding="utf-8") as file:
			json.dump(self.data, file, ensure_ascii=True, indent=4)
		self.editing_start()
	
	def save(self):
		'''
		Сохроняет результат
		'''
		with open(f"maps/map_{self.map_num}.json", "w") as file:
			json.dump(self.data, file, ensure_ascii=True, indent=4)
	
	def close(self):
		'''
		Коректное закрытие редактора
		'''
		self.save()
		self.data = {
			"map_name": f"MAP_{self.max_map_index}",
			"map": [],
			"zero_point": [0, 0],
			"player_main_weapon": "Weapon",
			"player_secondary_weapon": "Weapon",
			"player_grenade_type": "Weapon",
			"player_melee_weapon": "Weapon",
			"checkpoints": {},
			"allies": [],
			"enemies": [],
		}
		init.buttons_editor = []
		config.state_of_editor["main location"] = False
		self.map_num = 0
		for i in range(len(init.scripts.maps)):
			MapChoiseButton([config.window_size[0]//2-config.CELL_SIZE, (i+1)*config.CELL_SIZE//4+i*config.CELL_SIZE], i+1)
		CreateNewMap([config.window_size[0]//2-config.CELL_SIZE, (i+2)*config.CELL_SIZE//4+(i+1)*config.CELL_SIZE])
	
	def __create_buttons(self):
		'''
		Создаёт кнопки основной локации
		'''
		MapEdit([config.CELL_SIZE, config.CELL_SIZE//2])
	
	def editing_start(self):
		'''
		Инициализирует работу над выбранной картой
		'''
		init.buttons_editor = []
		config.state_of_editor["main location"] = True
		self.__create_buttons()
		self.__characters_list_update()
	
	def back_to_main_location(self):
		'''
		Возврат в основную локацию редактора
		'''
		config.state_of_editor = {
			"main location": True,
			"main weapon choise": False,
			"second weapon choise": False,
			"melee weapon choise": False,
			"grenade choise": False,
			"editing a map": False
		}
		self.input_fields = []
		init.buttons_editor = []
		self.__create_buttons()
	
	def editing_map(self):
		'''
		Инициализирует работу над картой
		'''
		init.buttons_editor = []
		BackToMainLocation([config.CELL_SIZE//2, config.CELL_SIZE//2])
		config.state_of_editor["main location"] = False
		config.state_of_editor["editing a map"] = True

		text_input = pygame_textinput.TextInputVisualizer(font_color=config.COLOR_RED)
		self.input_fields.append(text_input)
	
	def __processing_input(self, field):
		'''
		Обработка ввода
		'''
		request = field.value.split() #разделят цельную строку на составные части
		print(request)
		field.value = "" #обнуление строки

		try:
			if request[0] == "cb": #обрабатывает приказ на создание карты
				if "*" in request[1]:
					request_1 = request[1].split("*")
					self.data["map"] = []
					self.__create_board_field([request_1[0], request_1[1]])
			elif request[0] == "add": #обрабатывает приказ на добавление...
				if request[1] == "to" and request[2] == "map": #... для карты ...
					self.selected_cell = None
					if "*" in request[3]: #обрабатыывает умножение (количество добавляемых предметов)
						request_1 = request[3].split("*")
						request_1 = [request_1[0], int(request_1[1])]
					else:
						request_1 = [request[3], 1]
					
					add_invert = False
					try:
						if request[4] in ["up", "left"]:
							add_invert = True
					except IndexError:
						pass

					if request_1[0] == "row": #... строку
						for _ in range(request_1[1]):
							if add_invert:
								for enemy in self.data["enemies"]:
									enemy["position"][1] += 1
								for point in self.data["checkpoints"]:
									self.data["checkpoints"][point][1] += 1
								self.__characters_list_update()
							self.__add_row(add_invert)
					elif request_1[0] == "col": #... стоба
						for _ in range(request_1[1]):
							if add_invert:
								for enemy in self.data["enemies"]:
									enemy["position"][0] += 1
								for point in self.data["checkpoints"]:
									self.data["checkpoints"][point][0] += 1
								self.__characters_list_update()
							self.__add_column(add_invert)

				elif request[1] in ["check", "point", "checkpoint"]: #... чекпоинт
					checkpoint_count = len(self.data["checkpoints"])
					if self.selected_cell != None:
						self.data["checkpoints"][f"checkpoint_{checkpoint_count+1}"] = [self.selected_cell.y, self.selected_cell.x]

				elif request[1] == "chr": #...персонажа...
					character_self = self.__character_translation(request[2])
					if request[3] == "e":
						request[3] = "enemies"
					elif request[3] == "a":
						request[3] = "allies"
					elif request[3] == "t":
						request[3] = "enemies_tied_to_the_script"
					if request[3] in config.CHARACTERs_TYPES:
						character_type = request[3]
						character_position = None
						i = 0
						if request[4] == "cell":
							if self.selected_cell != None:
								character_position = [self.selected_cell.y, self.selected_cell.x]
							else:
								return
						elif request[4] == "coords":
							i = 2
							character_position = [int(request[6]), int(request[7])]
						if character_position != None:
							character_angle = int(request[5+i])

							character_main_weapon = request[6+i]
							character_main_weapon = self.__weapon_translation(character_main_weapon)

							character_second_weapon = request[7+i]
							character_second_weapon = self.__weapon_translation(character_second_weapon)

							character_melee_weapon = request[8+i]
							character_melee_weapon = self.__weapon_translation(character_melee_weapon)

							character_grenade_type = request[9+i]
							character_grenade_type = self.__weapon_translation(character_grenade_type)

							character_ai_type = request[10+i]

							self.data[character_type].append({
								"self_type": character_self,
								"main_weapon": character_main_weapon,
								"second_weapon": character_second_weapon,
								"melee_weapon": character_melee_weapon,
								"grenade_type": character_grenade_type,
								"ai_type": character_ai_type,
								"position": character_position,
								"start_angle": character_angle
							})
							self.__characters_list_update()
			elif request[0] == "remove": #обрабатывает приказ на убирание
				if request[1] == "chr": #... персонажа
					character_position = None
					if request[2] == "cell":
						if self.selected_cell != None:
							character_position = [self.selected_cell.y, self.selected_cell.x]
					elif request[2] == "coords":
						character_position = [request[3], request[4]]

					if character_position != None:
						for enemy in self.data["enemies"]:
							if enemy["position"] == character_position:
								self.data["enemies"].remove(enemy)
								self.__characters_list_update()
								break
						for allie in self.data["allies"]:
							if enemy["position"] == character_position:
								self.data["allie"].remove(allie)
								self.__characters_list_update()
								break
				elif request[1] in ["point", "check", "checkpoint"]: #... контрольной точки
					if request[2] == "cell":
						if self.selected_cell != None:
							for checkpoint in self.data["checkpoints"]:
								if self.data["checkpoints"][checkpoint] == [self.selected_cell.y, self.selected_cell.x]:
									self.data["checkpoints"].pop(checkpoint)
									break
					elif request[2] == "coords":
						for checkpoint in self.data["checkpoints"]:
							if self.data["checkpoints"][checkpoint] == [int(request[4]), int(request[3])]:
								self.data["checkpoints"].pop(checkpoint)
								break

			elif request[0] == "rp": #обрабатывает замену ячейки
				if self.selected_cell != None: #через выбору ячейки по клику
					self.data["map"][self.selected_cell.x][self.selected_cell.y] = self.__cell_letter_translation(" ".join(request[1:]))
				elif request[1] == "c": #через координаты
					self.data["map"][int(request[2])][int(request[3])] = request[4]
			elif request[0] == "reset": #обнуление ...
				if request[1] == "map": #... карты
					self.data["map"] = []
					self.data["zero_point"] = [0, 0]
				elif request[1] == "cell":#... выбранной клетки
					self.selected_cell = None
				elif request[1] == "chr":#... персонажей
					try:
						if request[2] in ["e", "enemies"]:
							self.data["enemies"] = []
						elif request[2] in ["a", "allies"]:
							self.data["allies"] = []
					except IndexError:
						self.data["enemies"] = []
						self.data["allies"] = []
			elif request[0] == "fix": #сохранение...
				if request[1] == "map":#... проекта
					self.save()
				elif request[1] == "zero":#... нулевой координаты
					self.data["zero_point"] = [config.zero_coordinate[0] // config.CELL_SIZE, config.zero_coordinate[1] // config.CELL_SIZE]
			elif request[0] == "set": #задать...
				if request[1] == "name": #... имя карты
					self.data["map_name"] = request[2]
		except IndexError:
			pass
	
	def __create_board_field(self, size: list):
		'''
		Создаёт поле размером size[0] на size[1]
		'''
		for x in range(int(size[0])):
			self.data["map"].append([])
			for _ in range(int(size[1])):
				self.data["map"][x].append("o")
	
	def __add_row(self, add_invert: bool):
		'''
		Добавляет строку
		'''
		if add_invert:
			self.data["map"].insert(0, [])
		else:
			self.data["map"].append([])
		
		for _ in range(len(self.data["map"][1])):
			if add_invert:
				self.data["map"][0].append("o")
			else:
				self.data["map"][-1].append("o")
	
	def __add_column(self, add_invert: bool):
		'''
		Добавляет столб
		'''
		for x in range(len(self.data["map"])):
			if add_invert:
				self.data["map"][x].insert(0, "o")
			else:
				self.data["map"][x].append("o")
	
	def __show_map(self):
		'''
		Отрисовывает карту
		'''
		init.obstacles.empty()
		init.markers.empty()

		self.cell_list = []
		coord = [0, 0]
		for x, line in enumerate(self.data["map"]):
			for y, cell in enumerate(line):
				if True:
					temp_coord = [config.zero_coordinate[0]+coord[0]*config.CELL_SIZE, config.zero_coordinate[1]+coord[1]*config.CELL_SIZE]
					if temp_coord[0] > 0 or temp_coord[0]+config.CELL_SIZE > 0:
						if temp_coord[0] > config.window_size[0] or temp_coord[1] > config.window_size[1]:
							break
						if temp_coord[1] > 0 or temp_coord[1]+config.CELL_SIZE > 0:
							cell = Obstacle(temp_coord, [x, y], cell)
							cell.x = x
							cell.y = y
							if self.selected_cell != None:
								if self.selected_cell.x == cell.x and self.selected_cell.y == cell.y:
									m_cell = M_Mark(temp_coord, [x, y])
									init.markers.add(m_cell)
							if cell.type == 19:
								s_cell = S_Mark(temp_coord, [x, y])
								self.s_cell_list.append(s_cell)
								init.markers.add(s_cell)
							for checkpoint in self.data["checkpoints"]:
								if self.data["checkpoints"][checkpoint] == [y, x]:
									c_cell = C_Mark(temp_coord, [x, y])
									self.c_cell_list.append(c_cell)
									init.markers.add(c_cell)
							self.cell_list.append(cell)
							init.obstacles.add(cell)
					coord[0] += 1
			coord[0] = 0
			coord[1] += 1

		p_cell = P_Mark([-self.data["zero_point"][0]*config.CELL_SIZE + config.zero_coordinate[0] + config.window_size[0]//2, -self.data["zero_point"][1]*config.CELL_SIZE + config.zero_coordinate[1] + config.window_size[1]//2], [0, 0])
		init.markers.add(p_cell)
	
	def __characters_list_update(self):
		'''
		Обновляет список персонажей в глобальной группе спрайтов
		'''
		init.enemies.empty()
		self.character_list = []

		for enemy in self.data["enemies"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"])
			init.enemies.add(self_enemy)
			self.character_list.append(self_enemy)

		for enemy in self.data["enemies_tied_to_the_script"]:
			enemy_type = globals()[enemy["self_type"]]
			self_enemy = enemy_type(enemy["main_weapon"], enemy["second_weapon"], enemy["melee_weapon"], enemy["grenade_type"], enemy["ai_type"], enemy["position"], enemy["start_angle"])
			init.enemies.add(self_enemy)
			self.character_list.append(self_enemy)

		init.allies.empty()
		for allie in self.data["allies"]:
			allie_type = globals()[allie["self_type"]]
			self_allie = allie_type(allie["main_weapon"], allie["second_weapon"], allie["melee_weapon"], allie["grenade_type"], allie["ai_type"], allie["position"], allie["start_angle"])
			init.allies.add(self_allie)
			self.character_list.append(self_allie)
		
	def __find_cell(self):
		'''
		Находит клетку на которую было сделанно нажатие
		'''
		mause_pos = py.mouse.get_pos()
		for cell in self.cell_list:
			if cell.rect.collidepoint(mause_pos):
				self.selected_cell = cell
				return
	
	def __cell_letter_translation(self, request: str):
		'''
		Переводит абстрактный запрос в используеммое для клетки обозначение
		'''
		for translation in sprits.TRANSLATION:
			if request in translation:
				return translation[0]
		return "o"

	def __weapon_translation(self, weapon: str):
		if weapon in ["Lasgun", "L", "1"]:
			return "Lasgun"
		elif weapon in ["Boltgun", "B", "B0", "2"]:
			return "Boltgun"
		elif weapon in ["Boltpistol", "B1", "3"]:
			return "Boltpistol"
		elif weapon in ["Boltrifel", "B2", "4"]:
			return "Boltrifel"
		elif weapon in ["Plasmagun", "P", "5"]:
			return "Plasmagun"
		elif weapon in ["Bayonet", "Ba", "6"]:
			return "Bayonet"
		elif weapon in ["Flamethrower", "F", "7"]:
			return "Flamethrower"
		elif weapon in ["FragmentationGrenade", "FG", "8"]:
			return "FragmentationGrenade"
		else:
			return "Weapon"
	
	def __character_translation(self, character: str):
		if character in ["BloodPackSoldier", "bloodpacksoldier", "bsoldier", "b_soldier", "bloodsoldier", "BloodSoldier"]:
			return "BloodPackSoldier"
	
	def update_editor(self, events):
		if config.state_of_editor["editing a map"]:
			self.__show_map()
			for character in self.character_list:
				character.position_update()
			for field in self.input_fields:
				field.update(events)
				init.screen.blit(field.surface, (config.CELL_SIZE*3, config.CELL_SIZE//2))
				for event in events:
					if event.type == py.KEYDOWN:
						if event.key == py.K_RETURN:
							self.__processing_input(field)
						if event.key == py.K_UP:
							self.camera_moving["up"] = True
						if event.key == py.K_DOWN:
							self.camera_moving["down"] = True
						if event.key == py.K_RIGHT:
							self.camera_moving["right"] = True
						if event.key == py.K_LEFT:
							self.camera_moving["left"] = True
					if event.type == py.KEYUP:
						if event.key == py.K_UP:
							self.camera_moving["up"] = False
						if event.key == py.K_DOWN:
							self.camera_moving["down"] = False
						if event.key == py.K_RIGHT:
							self.camera_moving["right"] = False
						if event.key == py.K_LEFT:
							self.camera_moving["left"] = False
					if event.type == py.MOUSEBUTTONDOWN:
						if event.button == 1:
							self.__find_cell()

				if any(self.camera_moving):
					if self.camera_moving["up"]:
						config.zero_coordinate[1] += 15
					if self.camera_moving["down"]:
						config.zero_coordinate[1] -= 15
					if self.camera_moving["right"]:
						config.zero_coordinate[0] -= 15
					if self.camera_moving["left"]:
						config.zero_coordinate[0] += 15