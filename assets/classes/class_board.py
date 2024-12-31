import pygame as py
import assets.config as config
import assets.initialization as init
from assets.image_loader import *
from assets.map_generator import *

class Board:
	def __init__(self):
		self.map = Map()
		self.__enemies_list = []
		self.__allies_list = []
		self.__item_list = []
		self.__boss_group = []
	
	def zero_coordinate_update(self):
		'''
		Обновление "нулевой координаты", что определяет положение левого верхрено угла карты
		'''
		dx = 0
		dy = 0

		speed = init.player.speed

		if config.moving["taking aim"]:
			speed /= 2
		if config.moving["run"]:
			speed *= 2
		
		if config.moving["forward"]:
			dy += speed
		if config.moving["left"]:
			dx += speed
		if config.moving["right"]:
			dx -= speed
		if config.moving["back"]:
			dy -= speed
		
		dx, dy = init.player.check_collision(dx, dy)
		
		if dx == 0 and dy == 0:
			return
		
		config.zero_coordinate[0] += dx
		config.zero_coordinate[1] += dy
		self.map.map_translation()
	
	def add_character(self, character: py.sprite.Sprite, list_type: str):
		'''
		Добавить персонажа в список у board для обновления
		'''

		if list_type == "enemy":
			self.__enemies_list.append(character)
		elif list_type == "allie":
			self.__allies_list.append(character)
		elif list_type == "boss":
			self.__boss_group.append(character)
	
	def add_item(self, item: py.sprite.Sprite):
		'''
		Добавляет брошений предмет в список
		'''
		self.__item_list.append(item)
	
	def remove_character(self, character: py.sprite.Sprite, list_type: str):
		'''
		Уберает персонажа из списка
		'''

		if character == "all":
			if list_type == "enemy":
				self.__enemies_list = []
			elif list_type == "allie":
				self.__allies_list = []
			elif list_type == "boss":
				self.__boss_group = []
		else:
			if list_type == "enemy":
				self.__enemies_list.remove(character)
			elif list_type == "allie":
				self.__allies_list.remove(character)
			elif list_type == "boss":
				self.__boss_group.remove(character)

	def update_board(self):
		for boss in self.__boss_group:
			boss.position_update()
			boss.ai.update()
			boss.animation_update()
		for enemy in self.__enemies_list:
			enemy.position_update()
			if enemy.rect.centerx < config.window_size[0] and enemy.rect.centerx > 0:
				if enemy.rect.centery < config.window_size[1] and enemy.rect.centery > 0:
					if not enemy.dead:
						enemy.ai.update()
					enemy.animation_update()
		
		for allie in self.__allies_list:
			allie.position_update()
			allie.ai.update()
			#allie.animation_update()
		for item in self.__item_list:
			item.update()
		for anim_obstacle in init.animated_obstacle:
			anim_obstacle.animation_update()
		
		init.player.animation_update()
		init.player.turn()
		init.player.update()

		if config.moving["fire"] and init.player.active_weapon.automatic:
			init.player.shoot()

		if any(config.moving[key] for key in ["forward", "left", "right", "back"]):
			self.zero_coordinate_update()