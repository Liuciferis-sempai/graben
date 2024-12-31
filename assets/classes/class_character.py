import pygame as py
import assets.config as config
import assets.initialization as init
import random
import assets.ai_pack as ai_pack
from assets.classes.class_weapon import *
from assets.sprits import CHARACTERS, ICONS

class Entity(py.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.dead = False
		self.name = "no_name"
		self.hp = 0
		self.speed = 0
		self.angle = 0
		self.state = "waiting"
		self.start_position = [0, 0]
		self.position = [0, 0]

		self.active_weapon = Weapon()

		self.main_weapon = Weapon()
		self.melee_weapon = Weapon()
		self.second_weapon = Weapon()
		self.grenade_type = Weapon()

		self.grenade_count = 0

		self.weapon_mode = 0

		self.ammo_count_in_pocket = 0
		self.ammo_count_in_pocket_max = 0
		self.ammo_count_in_weapon = 0
		self.ammo_count_in_weapon_max = 0

		self.last_animation_update_time = py.time.get_ticks()
		self.last_shoot_time = py.time.get_ticks()
		self.last_grenade_time = py.time.get_ticks()
		self.last_melee_atack_time = py.time.get_ticks()
		self.frame_index = 0
		self.animation = {
			"waiting": [],
			"walking": [],
			"running": [],
			"shooting": [],
			"aiming": [],
			"dead": []
		}
		self.image_width = config.CELL_SIZE//2
		self.image_height = config.CELL_SIZE//2
	
	def load_animations(self):
		pass
	
	def __has_no_obstacles(self, enemy: object):
		'''
		Проверяет, нет ли препятствий на пути к объекту
		'''
		for obstacle in init.obstacles:
			if obstacle.type in [0, 20, 14, 12]:
				if obstacle.rect.clipline(self.rect.center, enemy.rect.center):
					return False
		return True
	
	def change_weapon_mode(self):
		'''
		Смена режима стрельбы
		'''

		if self.active_weapon.name == "Plasmagun":
			if self.weapon_mode == 0:
				self.weapon_mode = 1
			else:
				self.weapon_mode = 0
	
	def point_of_shoot(self):
		'''
        Определяет где находится оружие на момент выстрела
        '''

		local_top_right = py.math.Vector2(self.rect.width // 2, -self.rect.height // 2)

		center = py.math.Vector2(self.rect.center)

		rotated_point = center + local_top_right.rotate(-self.angle)
		return rotated_point.x - config.zero_coordinate[0], rotated_point.y - config.zero_coordinate[1]
	
	def check_state(self):
		'''
		Проверяет состояние персонажа и устанавливает его состояние
		'''
		if self.name == "walram":
			if self.dead:
				self.state = "dead"
			elif config.moving["fire"]:
				self.state = "shooting"
			elif config.moving["taking aim"]:
				self.state = "aiming"
			elif config.moving["run"]:
				self.state = "running"
			elif any(config.moving[key] for key in ["forward", "left", "right", "back"]):
					self.state = "walking"
			else:
				self.state = "waiting"
	
	def animation_update(self):
		'''
		Обновляет анимации
		'''
		self.check_state() #проверка состояния персонажа

		if self.state == "shooting":
			cooldown = self.active_weapon.cooldown // 2
		elif self.state in ["dead", "running"]:
			cooldown = config.ANIMATION_COOLDOWN // 2
		elif self.state == "waiting":
			cooldown = config.ANIMATION_COOLDOWN * 2
		else:
			cooldown = config.ANIMATION_COOLDOWN

		if py.time.get_ticks() - self.last_animation_update_time > cooldown: #кулдаун (задержка) между кадрами
			self.last_animation_update_time = py.time.get_ticks()
			if self.frame_index > len(self.animation[self.state])-1:
				if self.state == "dead":
					print("!!!")
					if self.name == "walram":
						init.scripts.game_over()
					else:
						print("!!!!")
						init.board.remove_character(self, "enemy")
						self.kill()
						for enemy in init.enemies:
							print("!!! !!")
							if self.__has_no_obstacles(enemy):
								enemy.ai.triggered(self)
					return
				self.frame_index = 0
			self.picture = self.animation[self.state][self.frame_index]
			self.picture = py.transform.scale(self.picture, (self.image_width, self.image_height))

			self.frame_index += 1
	
	def check_collision(self, dx, dy):
		'''
		Проверка на колизию при перемещении
		'''
		if self.name == "walram":
			if init.settings["chits"]["noclip"]:
				return dx, dy
		new_rect = py.Rect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height)
		temp_sprite = py.sprite.Sprite()
		temp_sprite.rect = new_rect

		for obj in init.obstacles: #проверка на взаимодействие с картой
			if temp_sprite.rect.colliderect(obj.rect):
				if obj.type in [0, 20, 14, 12, 22, 23, 25]: #проверка на столкновение с препятствиями
					if self.rect.right > obj.rect.left and self.rect.left < obj.rect.left:
						if dx < 0:
							dx = -dx
							if self.name == "walram":
								config.moving["right"] = False
					elif self.rect.left < obj.rect.right and self.rect.right > obj.rect.right:
						if dx > 0:
							dx = -dx
							if self.name == "walram":
								config.moving["left"] = False
				elif obj.position in init.game_map["checkpoints"].values(): #проверка на контакт с тригерами скрипта
					init.scripts.checkpoint(obj.position)
				elif obj.type in [16, 17]: #проверка на контакт с боеприпасами
					pass

		#for obj in init.items: #проверка на взаимодействие с упавшим оружием
		#	if temp_sprite.rect.colliderect(obj.rect):
		#		if obj != self:
		#			if hasattr(obj, "weapon"):
		#				if obj.weapon.name != self.active_weapon.name and obj.weapon.name != self.second_weapon.name:
		#					self.active_weapon = obj.weapon
		#					self.grenade_count = obj.grenade_count
		#					self.ammo_count_in_weapon = obj.ammo_count_in_weapon
		#					self.ammo_count_in_pocket = obj.ammo_count_in_pocket
		#					self.ammo_count_in_weapon_max = obj.ammo_count_in_weapon_max
		#					self.ammo_count_in_pocket_max = obj.ammo_count_in_pocket_max
		#					obj.kill()

		new_rect = py.Rect(self.rect.left, self.rect.top + dy, self.rect.width, self.rect.height)
		temp_sprite = py.sprite.Sprite()
		temp_sprite.rect = new_rect

		for obj in init.obstacles: #проверка на взаимодействие с картой
			if temp_sprite.rect.colliderect(obj.rect):
				if obj.type in [0, 20, 14, 12, 22, 23, 25]: #проверка на столкновение с препятствиями
					dy = -dy
					if self.rect.bottom > obj.rect.top and self.rect.top < obj.rect.top:
						if dy < 0:
							dy = -dy
							if self.name == "walram":
								config.moving["back"] = False
					elif self.rect.top < obj.rect.bottom and self.rect.bottom > obj.rect.bottom:
						if dy > 0:
							dy = -dy
							if self.name == "walram":
								config.moving["forward"] = False
				elif obj.type in [16, 17]: #проверка на контакт с боеприпасами
					pass

		#for obj in init.items: #проверка на взаимодействие с упавшим оружием
		#	if temp_sprite.rect.colliderect(obj.rect):
		#		if obj != self:
		#			if hasattr(obj, "weapon"):
		#				if obj.weapon.name != self.active_weapon.name and obj.weapon.name != self.second_weapon.name:
		#					self.active_weapon = obj.weapon
		#					self.grenade_count = obj.grenade_count
		#					self.ammo_count_in_weapon = obj.ammo_count_in_weapon
		#					self.ammo_count_in_pocket = obj.ammo_count_in_pocket
		#					self.ammo_count_in_weapon_max = obj.ammo_count_in_weapon_max
		#					self.ammo_count_in_pocket_max = obj.ammo_count_in_pocket_max
		#					obj.kill()

		return dx, dy
	
	def turn(self, target):
		'''
		Поворот персонажа в сторону цели
		'''
		dx_angle = target[0] - self.rect.centerx
		dy_angle = target[1] - self.rect.centery
		self.angle = math.degrees(math.atan2(-dy_angle, dx_angle)) - 90
		
		rotated_image = py.transform.rotate(self.picture, self.angle)
		self.image = rotated_image
		self.rect = self.image.get_rect(center=self.rect.center)
	
	def shoot(self, target: object = None):
		'''
		Производит выстрел
		'''
		if self.active_weapon.ammo_in_weapon != 0:
			if py.time.get_ticks() - self.last_shoot_time > self.active_weapon.cooldown:
				self.active_weapon.ammo_in_weapon -= 1
				self.last_shoot_time = py.time.get_ticks()

				if target == None:
					target = py.mouse.get_pos()
				else:
					target = [target.rect.centerx+random.randint(-config.SCATTER, config.SCATTER), target.rect.centery+random.randint(-config.SCATTER, config.SCATTER)]

				if self.weapon_mode == 0:
					self.active_weapon.shoot(self.point_of_shoot(), target, False, self)
				else:
					self.active_weapon.alt_shoot(self.point_of_shoot(), target, True, self)
	
	def melee_atack(self, target: object = None):
		'''
		Производит атаку оружием ближнего боя
		'''
		if py.time.get_ticks() - self.last_melee_atack_time > self.melee_weapon.cooldown:
			self.last_melee_atack_time = py.time.get_ticks()

			if target == None:
				target = py.mouse.get_pos()
			else:
				target = target.rect.center

			self.melee_weapon.shoot(self.point_of_shoot(), target, True, self)

	def reload(self):
		'''
		Перезарядка
		'''
		self.ammo_count_in_weapon += 255

	def grenade(self, target_pos: list = None):
		'''
		Бросок гранаты
		'''
		if self.grenade_count != 0:
			if py.time.get_ticks() - self.last_grenade_time > self.grenade_type.cooldown:
				self.last_grenade_time = py.time.get_ticks()
				self.grenade_count -= 1
				if target_pos == None:
					target_pos = py.mouse.get_pos()
				self.grenade_type.shoot(self.point_of_shoot(), [target_pos[0]+random.randint(-config.SCATTER, config.SCATTER), target_pos[1]+random.randint(-config.SCATTER, config.SCATTER)], False, self)
	
	def position_update(self):
		'''
		обновляем позицию персанажа относительно нулевой координаты
		'''
		position = [config.zero_coordinate[0] + self.start_position[0], config.zero_coordinate[1] + self.start_position[1]]
		self.rect.x = position[0]
		self.rect.y = position[1]
	
	def hit(self, bullet):
		'''
		Обрабатываем попадание
		'''
		self.hp -= 1
		if self.hp <= 0:
			if self.name == "walram":
				if init.settings["chits"]["undead"]:
					self.hp = 3
					return
			self.dying()
			if self.name == "walram":
				init.save["statistics"]["number of deaths"] += 1
			elif bullet.creator.name == "walram":
				init.save["statistics"]["number of kills"] += 1
			init.scripts.save_save()
	
	def dying(self):
		'''
		Смерть персанажа
		'''
		self.dead = True
		self.state = "dead"
		FallenWeapon(self.active_weapon, self.rect.center)

class Walram(Entity):
	def __init__(self):
		super().__init__()

		self.name = "walram"
		self.hp = config.PlAYER_MAX_HP
		self.speed = config.PLAYER_SPEED

		self.main_weapon = globals()[init.game_map["player_main_weapon"]]()
		self.second_weapon = globals()[init.game_map["player_secondary_weapon"]]()
		self.melee_weapon = globals()[init.game_map["player_melee_weapon"]]()
		self.grenade_type = globals()[init.game_map["player_grenade_type"]]()
		self.active_weapon = self.main_weapon

		self.grenade_count = 3

		self.load_animations()

		original_picture = self.animation["waiting"][0]
		self.picture = py.transform.scale(original_picture, (self.image_width, self.image_height))
		self.image = self.picture
		self.start_position = [config.window_size[0]//2, config.window_size[1]//2]
		self.rect = self.image.get_rect(center=self.start_position)
	
	def load_animations(self):
		self.animation["waiting"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["WAITING"]
		self.animation["walking"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["WALKING"]
		self.animation["running"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["RUNNING"]
		self.animation["shooting"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["SHOOTING"]
		self.animation["aiming"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["AIMING"]
		self.animation["dead"] = CHARACTERS["WALRAM"][self.active_weapon.name.upper()]["DEAD"]
	
	def reload(self):
		if self.active_weapon.ammo_in_pocket >= self.active_weapon.ammo_in_weapon_max:
			self.active_weapon.ammo_in_weapon = self.active_weapon.ammo_in_weapon_max
			self.active_weapon.ammo_in_pocket -= self.active_weapon.ammo_in_weapon_max
		elif self.active_weapon.ammo_in_pocket != 0:
			self.active_weapon.ammo_in_weapon = self.active_weapon.ammo_in_pocket
			self.active_weapon.ammo_in_pocket = 0
	
	def turn(self):
		'''
		Поворот персонажа в сторону мыши
		'''

		mouse_x, mouse_y = py.mouse.get_pos()
		super().turn([mouse_x, mouse_y])

	def restart(self):
		'''
		Перезапуск персонажа
		'''
		self.dead = False
		self.hp = config.PlAYER_MAX_HP

		self.main_weapon = globals()[init.game_map["player_main_weapon"]]()
		self.second_weapon = globals()[init.game_map["player_secondary_weapon"]]()
		self.melee_weapon = globals()[init.game_map["player_melee_weapon"]]()
		self.grenade_type = globals()[init.game_map["player_grenade_type"]]()
		self.active_weapon = self.main_weapon

		self.main_weapon.ammo_in_pocket = self.main_weapon.ammo_in_pocket_max
		self.main_weapon.ammo_in_weapon = self.main_weapon.ammo_in_weapon_max

		self.active_weapon = self.main_weapon

		self.grenade_count = 3
		self.active_weapon = self.main_weapon

		self.main_weapon.ammo_in_weapon = self.main_weapon.ammo_in_weapon_max
		self.second_weapon.ammo_in_weapon = self.second_weapon.ammo_in_weapon_max

class Commissar(Entity):
	def __init__(self, main_weapon: str = "Weapon", second_weapon: str = "Weapon", melee_weapon: str = "Weapon", grenade_type: str = "Weapon", ai_type: str = "no_ai", start_position: list = [0, 0], start_angle: int = 0, waypoints: list = None):
		super().__init__()

		self.name = "commissar"
		self.hp = 4
		self.speed = config.COMMISSAR_SPEED
		self.angle = start_angle

		self.main_weapon = globals()[main_weapon]()
		self.second_weapon = globals()[second_weapon]()
		self.melee_weapon = globals()[melee_weapon]()
		self.grenade_type = globals()[grenade_type]()
		self.active_weapon = self.main_weapon

		self.ai = ai_pack.choice_ai(self, ai_type, {"type": "player_tracking"})

		original_picture = CHARACTERS["COMMISSAR"]["_"]

		self.picture = py.transform.scale(original_picture, (self.image_width, self.image_height))
		self.image = self.picture
		self.start_position = [start_position[0]*config.CELL_SIZE+config.CELL_SIZE//4, start_position[1]*config.CELL_SIZE+config.CELL_SIZE//4]
		self.rect = self.image.get_rect(center=self.start_position)

		if waypoints != None:
			self.waypoints = waypoints

class BloodPackSoldier(Entity):
	def __init__(self, main_weapon: str = "Weapon", second_weapon: str = "Weapon", melee_weapon: str = "Weapon", grenade_type: str = "Weapon", ai_type: str = "no_ai", start_position: list = [0, 0], start_angle: int = 0, waypoints: list = None):
		super().__init__()

		self.name = "blood_pack_soldier"
		self.hp = config.BLOOD_PACK_SOLDIER_HP
		self.speed = config.BLOOD_PACK_SOLDIER_SPEED
		self.fov = 110
		self.angle = start_angle

		self.main_weapon = globals()[main_weapon]()
		self.second_weapon = globals()[second_weapon]()
		self.melee_weapon = globals()[melee_weapon]()
		self.grenade_type = globals()[grenade_type]()
		self.active_weapon = self.main_weapon

		self.grenade_count = 5

		self.load_animations()

		self.ai = ai_pack.choice_ai(self, ai_type)

		self.position = start_position
		self.start_position = [start_position[0]*config.CELL_SIZE+config.CELL_SIZE//4, start_position[1]*config.CELL_SIZE+config.CELL_SIZE//4]

		original_picture = self.animation["waiting"][0]
		self.picture = py.transform.scale(original_picture, (self.image_width, self.image_height))
		self.image = self.picture
		self.start_position = [start_position[0]*config.CELL_SIZE+config.CELL_SIZE//4, start_position[1]*config.CELL_SIZE+config.CELL_SIZE//4]
		self.rect = self.image.get_rect(center=self.start_position)

		rotated_image = py.transform.rotate(self.picture, self.angle)
		self.image = rotated_image

		self.ammo_count_in_weapon = 255

		if waypoints != None:
			self.waypoints = waypoints
		
	def load_animations(self):
		self.animation["waiting"] = CHARACTERS["BLOODPACKSOLDIER"][self.active_weapon.name.upper()]["WAITING"]
		self.animation["shooting"] = CHARACTERS["BLOODPACKSOLDIER"][self.active_weapon.name.upper()]["SHOOTING"]
		self.animation["aiming"] = CHARACTERS["BLOODPACKSOLDIER"][self.active_weapon.name.upper()]["AIMING"]
		self.animation["dead"] = CHARACTERS["BLOODPACKSOLDIER"][self.active_weapon.name.upper()]["DEAD"]

class WorldEaater(Entity):
	def __init__(self, main_weapon: str = "Weapon", second_weapon: str = "Weapon", melee_weapon: str = "Weapon", grenade_type: str = "Weapon", ai_type: str = "no_ai", start_position: list = [0, 0], start_angle: int = 0, waypoints: list = None):
		super().__init__()
		self.image_width = config.CELL_SIZE
		self.image_height = config.CELL_SIZE

		self.name = "world_eater"
		self.hp = config.WORLD_EATER_HP_MAX
		self.speed = config.WORLD_EATER_SPEED
		self.fov = 360
		self.angle = start_angle

		self.main_weapon = globals()[main_weapon]()
		self.second_weapon = globals()[second_weapon]()
		self.melee_weapon = globals()[melee_weapon]()
		self.grenade_type = globals()[grenade_type]()
		self.active_weapon = self.main_weapon

		self.load_animations()

		self.ai = ai_pack.choice_ai(self, ai_type)

		self.position = start_position
		self.start_position = [start_position[0]*config.CELL_SIZE+config.CELL_SIZE//4, start_position[1]*config.CELL_SIZE+config.CELL_SIZE//4]

		original_picture = self.animation["waiting"][0]
		self.picture = py.transform.scale(original_picture, (self.image_width, self.image_height))
		self.image = self.picture
		self.start_position = [start_position[0]*config.CELL_SIZE, start_position[1]*config.CELL_SIZE]
		self.rect = self.image.get_rect(center=self.start_position)

		rotated_image = py.transform.rotate(self.picture, self.angle)
		self.image = rotated_image

		self.ammo_count_in_weapon = 9999

		if waypoints != None:
			self.waypoints = waypoints
	
	def load_animations(self):
		self.animation["waiting"] = CHARACTERS["WORLD_EATER"][self.active_weapon.name.upper()]["WAITING"]
		self.animation["shooting"] = CHARACTERS["WORLD_EATER"][self.active_weapon.name.upper()]["SHOOTING"]
		self.animation["aiming"] = CHARACTERS["WORLD_EATER"][self.active_weapon.name.upper()]["AIMING"]
		self.animation["dead"] = CHARACTERS["WORLD_EATER"][self.active_weapon.name.upper()]["DEAD"]
	
	def hit(self, bullet):
		if bullet.name == "laser":
			self.hp -= 1000
		elif bullet.name == "bolter":
			self.hp -= 30
		elif bullet.name == "bigbolter":
			self.hp -= 200
		elif bullet.name == "plasma":
			self.hp -= 150
		elif bullet.name == "grenade":
			self.hp -= 50
		elif bullet.name == "bayonet":
			self.hp -= 5
		
		if self.hp <= 0:
			init.scripts.end_fight_with_world_eater()

class Salamander(Entity):
	def __init__(self, main_weapon: str = "Weapon", second_weapon: str = "Weapon", melee_weapon: str = "Weapon", grenade_type: str = "Weapon", ai_type: str = "no_ai", start_position: list = [0, 0], start_angle: int = 0, waypoints: list = None):
		super().__init__()

		self.main_weapon = globals()[main_weapon]()
		self.second_weapon = globals()[second_weapon]()
		self.melee_weapon = globals()[melee_weapon]()
		self.grenade_type = globals()[grenade_type]()
		self.active_weapon = self.main_weapon

		if waypoints != None:
			self.waypoints = waypoints

class FallenWeapon(py.sprite.Sprite):
	def __init__(self, weapon: object, position: tuple):
		super().__init__()

		self.image = py.transform.scale(ICONS[weapon.name.upper()], (config.CELL_SIZE//2, config.CELL_SIZE//2))

		self.weapon = weapon

		position = [position[0]-config.zero_coordinate[0], position[1]-config.zero_coordinate[1]]
		self.rect = self.image.get_rect(center=position)
		self.start_position = position

		init.items.add(self)
		init.board.add_item(self)

	def update_animation(self):
		pass

	def update(self):
		self.rect.center = [config.zero_coordinate[0] + self.start_position[0], config.zero_coordinate[1] + self.start_position[1]]