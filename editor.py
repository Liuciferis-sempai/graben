import assets.initialization as init
import assets.config as config
from assets.classes.class_character import *
from assets.classes.class_button import *
from assets.classes.class_weapon import *
from assets.classes.class_obstacle import *
import json
import pygame_textinput
import assets.sprits as sprits
from assets.commands import *

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
			"tracked_checkpoints": {},
			"allies": [],
			"enemies": [],
			"enemies_tied_to_the_script": []
		}
		self.data_default = {
			"map_name": f"MAP_{self.max_map_index}",
			"map": [],
			"zero_point": [0, 0],
			"player_main_weapon": "Weapon",
			"player_secondary_weapon": "Weapon",
			"player_grenade_type": "Weapon",
			"player_melee_weapon": "Weapon",
			"checkpoints": {},
			"tracked_checkpoints": {},
			"allies": [],
			"enemies": [],
			"enemies_tied_to_the_script": []
		}
		self.text_input = pygame_textinput.TextInputVisualizer(font_color=config.COLOR_RED)
		self.answer = ""
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
		init.scripts.show_message_on_display("", [config.CELL_SIZE*3, config.CELL_SIZE*1.5], config.FONT_SIZE, config.COLOR_RED, "")
	
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
		with open(f"maps\{self.map_num}_map.json", "r", encoding="utf-8") as file:
			self.data = json.load(file)
		self.editing_start()

	def create_new_map(self):
		'''
		Создаёт новую карту
		'''
		self.map_num = self.max_map_index
		with open(f"maps\{self.max_map_index}_map.json", "w", encoding="utf-8") as file:
			json.dump(self.data, file, ensure_ascii=True, indent=4)
		self.editing_start()
	
	def save(self):
		'''
		Сохроняет результат
		'''
		with open(f"maps/{self.map_num}_map.json", "w") as file:
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
	
	def _create_buttons(self):
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
		self._create_buttons()
		self._characters_list_update()
	
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
		self._create_buttons()
	
	def editing_map(self):
		'''
		Инициализирует работу над картой
		'''
		init.buttons_editor = []
		BackToMainLocation([config.CELL_SIZE//2, config.CELL_SIZE//2])
		config.state_of_editor["main location"] = False
		config.state_of_editor["editing a map"] = True
	
	def _show_answer(self):
		'''
		Отображает ответ программы (например: консоли)
		'''
		try:
			if self.answer != init.texts[0].content:
				init.texts = []
				init.scripts.show_message_on_display(self.answer, [config.CELL_SIZE*3, config.CELL_SIZE*0.5], config.FONT_SIZE, config.COLOR_RED, self.answer)
		except:
			pass
	
	def _processing_input(self, field):
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
					self._create_board_field([request_1[0], request_1[1]])
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
								self._characters_list_update()
							self._add_row(add_invert)
					elif request_1[0] == "col": #... стоба
						for _ in range(request_1[1]):
							if add_invert:
								for enemy in self.data["enemies"]:
									enemy["position"][0] += 1
								for point in self.data["checkpoints"]:
									self.data["checkpoints"][point][0] += 1
								self._characters_list_update()
							self._add_column(add_invert)

				elif request[1] in ["check", "point", "checkpoint"]: #... чекпоинт
					checkpoint_count = len(self.data["checkpoints"])
					if self.selected_cell != None:
						self.data["checkpoints"][f"checkpoint_{checkpoint_count+1}"] = [self.selected_cell.y, self.selected_cell.x]

				elif request[1] == "chr": #...персонажа...
					character_self = self._character_translation(request[2])
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
							character_position = [tr_int(request[6]), tr_int(request[7])]
							if not (character_position[0] and character_position[1]):
								return
						if character_position != None:
							character_angle = tr_int(self._get_request(request, 5+i, "0"))

							character_main_weapon = self._weapon_translation(self._get_request(request, 6+1, "Lasgun"))

							character_second_weapon = self._weapon_translation(self._get_request(request, 7+i, "Weapon"))

							character_melee_weapon = self._weapon_translation(self._get_request(request, 8+i, "Weapon"))

							character_grenade_type = self._weapon_translation(self._get_request(request, 9+i, "Weapon"))

							character_ai_type = self._get_request(request, 10+i, "no_ai")

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
							self._characters_list_update()
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
								self._characters_list_update()
								break
						for ally in self.data["allies"]:
							if enemy["position"] == character_position:
								self.data["ally"].remove(ally)
								self._characters_list_update()
								break
						for enemy in self.data["enemies_tied_to_the_script"]:
							if enemy["position"] == character_position:
								self.data["enemies_tied_to_the_script"].remove(enemy)
								self._characters_list_update()
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
					self.data["map"][self.selected_cell.x][self.selected_cell.y] = self._cell_letter_translation(" ".join(request[1:]))
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
						elif request[2] in ["t"]:
							self.data["enemies_tied_to_the_script"] = []
					except IndexError:
						self.data["enemies"] = []
						self.data["allies"] = []
						self.data["enemies_tied_to_the_script"] = []
				elif request[1] == "all":
					self.data = self.data_default.copy()
			elif request[0] == "fix": #сохранение...
				if request[1] == "map":#... проекта
					self.save()
				elif request[1] == "zero":#... нулевой координаты
					self.data["zero_point"] = [config.zero_coordinate[0] // config.CELL_SIZE, config.zero_coordinate[1] // config.CELL_SIZE]
			elif request[0] == "set": #задать...
				if request[1] == "name": #... имя карты
					self.data["map_name"] = request[2]
			elif request[0] == "info": #показать информацию о...
				request_1 = self._get_request(request, 1, "map")
				if request_1 == "map": #... карты
					self.answer = f"Map name: {self.data["map_name"]}; CHR count: {len(self.data["enemies"])+len(self.data["allies"])+len(self.data["enemies_tied_to_the_script"])}; Checkpoints count: {len(self.data["checkpoints"])}"
				elif request_1 == "cell": #... выбранной клетки
					if self.selected_cell != None:
						self.answer = f"Cell: x {self.selected_cell.x} y {self.selected_cell.y}; Type: {self.selected_cell.type} / {next((key for key, value in sprits.OBSTACLE_MAP.items() if value == self.selected_cell.type), None)}"
					else:
						self.answer = "No selected cell"
				elif request_1 == "chr": #... персонажа
					if self.selected_cell != None:
						for character in self.character_list:
							if character.x == self.selected_cell.x and character.y == self.selected_cell.y:
								self.answer = f"Position: x {character.x} y {character.y}; Type: {character.__class__.__name__}"
								break
						else:
							self.answer = "No character in selected cell"
					else:
						self.answer = "No selected cell"
		except Exception as e:
			self.answer = str(e)
			print(e)
	
	def _create_board_field(self, size: list):
		'''
		Создаёт поле размером size[0] на size[1]
		'''
		for x in range(int(size[0])):
			self.data["map"].append([])
			for _ in range(int(size[1])):
				self.data["map"][x].append("o")
	
	def _add_row(self, add_invert: bool):
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
	
	def _add_column(self, add_invert: bool):
		'''
		Добавляет столб
		'''
		for x in range(len(self.data["map"])):
			if add_invert:
				self.data["map"][x].insert(0, "o")
			else:
				self.data["map"][x].append("o")
	
	def _show_map(self):
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
							elif cell.type == 40:
								f_cell = F_Mark(temp_coord, [x, y])
								init.markers.add(f_cell)
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
	
	def _characters_list_update(self):
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
		for ally in self.data["allies"]:
			ally_type = globals()[ally["self_type"]]
			self_ally = ally_type(ally["main_weapon"], ally["second_weapon"], ally["melee_weapon"], ally["grenade_type"], ally["ai_type"], ally["position"], ally["start_angle"])
			init.allies.add(self_ally)
			self.character_list.append(self_ally)
		
	def _find_cell(self):
		'''
		Находит клетку на которую было сделанно нажатие
		'''
		mouse_pos = py.mouse.get_pos()
		for cell in self.cell_list:
			if cell.rect.collidepoint(mouse_pos):
				self.selected_cell = cell
				return
	
	def _cell_letter_translation(self, request: str):
		'''
		Переводит абстрактный запрос в используеммое для клетки обозначение
		'''
		for translation in sprits.TRANSLATION:
			if request in translation:
				return translation[0]
		return "o"

	def _weapon_translation(self, weapon: str):
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
	
	def _character_translation(self, character: str):
		if character in ["BloodPackSoldier", "bloodpacksoldier", "bsoldier", "b_soldier", "bloodsoldier", "BloodSoldier", "bs"]:
			return "BloodPackSoldier"
	
	def _get_request(self, request: list, index: int, default):
		'''
		Получает определённый элемент из запроса
		'''
		answer = None
		try:
			answer = request[index]
		except IndexError:
			answer = default
		
		return answer
			
	def update_editor(self, events):
		if config.state_of_editor["editing a map"]:
			self._show_map()
			for character in self.character_list:
				character.position_update()
			
			self.text_input.update(events)
			init.screen.blit(self.text_input.surface, (config.CELL_SIZE*3, config.CELL_SIZE))
			for event in events:
				if event.type == py.KEYDOWN:
					if event.key == py.K_RETURN:
						self._processing_input(self.text_input)
					self._show_answer()
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
						self._find_cell()

			if any(self.camera_moving):
				if self.camera_moving["up"]:
					config.zero_coordinate[1] += 15
				if self.camera_moving["down"]:
					config.zero_coordinate[1] -= 15
				if self.camera_moving["right"]:
					config.zero_coordinate[0] -= 15
				if self.camera_moving["left"]:
					config.zero_coordinate[0] += 15