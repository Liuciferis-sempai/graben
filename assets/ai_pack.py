import pygame as py
import assets.initialization as init
import assets.config as config
import math
import random

class AI:
	'''
	Базовый ИИ, пассивный, не обладает ответной реакцией
	'''
	def __init__(self, bot: py.sprite.Sprite):
		self.bot = bot
		self.is_triggered = False
	
	def saw_target(self):
		'''
		нацеливание бота на игрока
		'''
		self.is_triggered = True
		self.bot.turn(init.player.start_position)
		self.bot.state = "aiming"
	
	def triggered(self, trigger: object):
		pass

	def update(self):
		pass

class Turret(AI):
	'''
	Персонаж как турель, стоит на месте и стреляет по цели, когда видит её
	'''
	def __init__(self, bot: py.sprite.Sprite):
		super().__init__(bot)
	
	def _can_see(self):
		'''
		Проверка на то, видит ли ии цель
		'''
		dx, dy = init.player.rect.centerx - self.bot.rect.centerx, init.player.rect.centery - self.bot.rect.centery

		angle_to_player = math.degrees(math.atan2(dy, dx)) + 90
		angle_diff = abs((angle_to_player + self.bot.angle + 180) % 360 - 180)
		
		if angle_diff <= self.bot.fov:
			for obstacle in init.obstacles:
				if obstacle.type in [0, 20, 14, 12]:
					if obstacle.rect.clipline(self.bot.rect.center, init.player.rect.center):
						return False
			return True
		else:
			return False
	
	def triggered(self, trigger: object):
		'''
		Бот резко смотрит в сторону тригера
		'''
		if not self.is_triggered:
			dx_angle = trigger.rect.centerx - self.bot.rect.centerx
			dy_angle = trigger.rect.centery - self.bot.rect.centery
			self.bot.angle = math.degrees(math.atan2(-dy_angle, dx_angle)) - 90
			
			rotated_image = py.transform.rotate(self.bot.picture, self.bot.angle)
			self.bot.image = rotated_image
			self.bot.state = "aiming"
	
	def update(self):
		'''
		Обновление ИИ. делается каждый шаг
		'''
		if self._can_see():
			self.saw_target()
			self.bot.shoot(init.player)

class FigurantAI(AI):
	'''
	Статист, ии которого сильно ограничен
	'''
	def __init__(self, bot: py.sprite.Sprite, modifikator: dict):
		super().__init__(bot)

		modifikator_type = modifikator.get("type", False)
		if not modifikator_type:
			return
		elif modifikator_type == "player_tracking":
			self.traking_target = init.player
			if not self.traking_target:
				return
			self.traking = True
	
	def update(self):
		if self.traking:
			self.bot.turn(self.traking_target.rect.center)

class TurretGrenadier(Turret):
	'''
	Статист гренадёр
	'''
	def _can_atack(self):
		dx, dy = init.player.rect.centerx - self.bot.rect.centerx, init.player.rect.centery - self.bot.rect.centery
		distance = math.sqrt(dx**2 + dy**2)

		if self.bot.active_weapon.has_second_shoot_mod:
			if distance < self.bot.active_weapon.max_distance:
				return True
		else:
			if distance < self.bot.grenade_type.max_distance:
				return True
		return False

	def update(self):
		super().update()
		if self._can_atack():
			if self.bot.active_weapon.has_second_shoot_mod:
				self.saw_target()
				self.bot.weapon_mode = 1
				self.bot.shoot(init.player)
				self.bot.weapon_mode = 0
			else:
				self.bot.grenade(init.player.rect.center)

class Charger(AI):
	'''
	Агрессивный ИИ, что стремится сократить дистанцию с игроком
	'''
	def __init__(self, bot: py.sprite.Sprite):
		super().__init__(bot)
		self.wish = "none"
		self.wish_list = [
			"charge", "wait", "fire"
		]
		self.wish_list_weight = (
			0.40, 0.10, 0.50
		)
		self.wait_began_at = 0
		self.wait_frame = {
			"min": 600,
			"max": 2000
		}
		self.fire_began_at = 0
		self.fire_frame = {
			"min": 5000,
			"max": 11000
		}
		self.charge_began_at = 0
		self.charge_frame = {
			"min": 9000,
			"max": 19000
		}
	
	def update(self):
		'''
		Обновление ИИ. делается каждый шаг
		'''
		self.bot.turn(init.player.start_position)
		if self.wish == "none":
			self.wish = random.choices(self.wish_list, self.wish_list_weight)
			self.wish = self.wish[0]
			print(self.wish)
		
		if self.wish == "charge":
			self.charge()
		elif self.wish == "wait":
			self.wait()
		elif self.wish == "fire":
			self.fire()
	
	def charge(self):
		'''
		Режим чарджа
		'''
		dx, dy = init.player.start_position[0] - config.zero_coordinate[0] - self.bot.start_position[0], init.player.start_position[1] - config.zero_coordinate[1] - self.bot.start_position[1]

		if dx > self.bot.speed:
			dx = self.bot.speed
		elif dx < 0:
			if abs(dx) > self.bot.speed:
				dx = -self.bot.speed
		if dy > self.bot.speed:
			dy = self.bot.speed
		elif dy < 0:
			if abs(dy) > self.bot.speed:
				dy = -self.bot.speed
		
		self.bot.start_position[0] += dx
		self.bot.start_position[1] += dy

		if self.charge_began_at == 0:
			self.charge_began_at = py.time.get_ticks()
		if py.time.get_ticks() - self.charge_began_at > self.charge_frame["min"]:
			if self.charge_began_at < self.charge_frame["max"]:
				factor = random.random()
				if factor < 0.0005:
					self.charge_began_at = 0
					self.wish = "wait"
			else:
				self.charge_began_at = 0
				self.wish = "wait"
		
		if self.bot.rect.colliderect(init.player.rect):
			self.bot.melee_atack(init.player)
			self.wish = "wait"

	def wait(self):
		'''
		Режим ожидания и бездействия
		'''
		self.bot.state = "waiting"
		if self.wait_began_at == 0:
			self.wait_began_at = py.time.get_ticks()
		if py.time.get_ticks() - self.wait_began_at > self.wait_frame["min"]:
			if self.wait_began_at < self.wait_frame["max"]:
				factor = random.random()
				if factor < 0.0005:
					self.wait_began_at = 0
					self.wish = "none"
			else:
				self.wait_began_at = 0
				self.wish = "none"

	def fire(self):
		'''
		Режим стрельбы
		'''
		self.bot.state = "aiming"
		self.bot.shoot(init.player)
		if self.fire_began_at == 0:
			self.fire_began_at = py.time.get_ticks()
		if py.time.get_ticks() - self.fire_began_at > self.fire_frame["min"]:
			if self.fire_began_at < self.fire_frame["max"]:
				factor = random.random()
				if factor < 0.0005:
					self.fire_began_at = 0
					self.wish = "wait"
			else:
				self.fire_began_at = 0
				self.wish = "wait"

class Traveler(AI):
	def __init__(self, bot: object):
		super().__init__(bot)

		waypoints = bot.get(bot.waypoints, None)
		self.waypoints = waypoints
		self.index = 0
	
	def update(self):
		if self.waypoints != None:
			pass

def choice_ai(bot: py.sprite.Sprite, ai_type: str, modifikator: dict = {}):
	'''
	выберает нужный ии для бота
	@bot бот которому присваивается ИИ
	@ai_type -> "no_ai", "figurant"
	@modifikator -> {"type": str ...}
	'''

	if ai_type == "figurant":
		return FigurantAI(bot, modifikator)
	elif ai_type == "turret":
		return Turret(bot)
	elif ai_type == "turret_grenadier":
		return TurretGrenadier(bot)
	elif ai_type == "charger":
		return Charger(bot)
	else:
		return AI(bot)