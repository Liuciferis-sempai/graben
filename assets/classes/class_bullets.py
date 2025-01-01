import pygame as py
import assets.config as config
import math
import assets.initialization as init
from assets.sprits import BULLETS, EXPLOSION

class Fire(py.sprite.Sprite):
	def	__init__(self, start_pos, target_pos, creator):
		super().__init__()
		self.image = BULLETS["FIRE"]
		self.original_image = self.image
		self.creator = creator
		self.start_pos = start_pos
		self.target_pos = target_pos

		self.die_update_time = py.time.get_ticks()
		self.die_wait_time = 20
		self.must_die_or_not = False

		self.already_exists = 0
		self.speed = 50

		dx = target_pos[0] - config.zero_coordinate[0] - start_pos[0]
		dy = target_pos[1] - config.zero_coordinate[1] - start_pos[1]

		self.angle = math.degrees(math.atan2(-dy, dx)) - 90
		self.image = py.transform.rotate(self.original_image, self.angle)

		self.rect = self.image.get_rect(center=start_pos)
		self.pos = py.math.Vector2(start_pos)
		try:
			self.direction = py.math.Vector2(dx, dy).normalize()
		except:
			self.direction = (0, 0)
		init.bullets.add(self)
	
	def update(self):
		move_vector = self.direction * self.speed
		self.rect.center = (self.pos.x + config.zero_coordinate[0], self.pos.y + config.zero_coordinate[1])
		self.pos += move_vector
		
		self.already_exists += 1
		if self.already_exists > config.FIRE_EXIST:
			self.must_die()
		else:
			collided_obstacles = py.sprite.spritecollide(self, init.obstacles_group, False)
			collided_enemy = py.sprite.spritecollide(self, init.enemies, False)
			collided_player = py.sprite.spritecollide(self, init.player_list, False)

			for obstacle in collided_obstacles:
				if obstacle.type in [0]:
					#self.kill()
					break
			if self.creator in collided_enemy:
				for hitted in collided_player:
					self.hit(hitted)
			else:
				for hitted, in collided_enemy:
					self.hit(hitted)
	
	def hit(self, hitted):
		if hitted != self.creator:
			self.must_die()
			if hasattr(hitted, "hit"):
				hitted.hit(self)
	
	def must_die(self):
		if not self.must_die_or_not:
			self.die_update_time = py.time.get_ticks()
			self.must_die_or_not = True
		if py.time.get_ticks() - self.die_update_time > self.die_wait_time:
			self.kill()

class Bullet(py.sprite.Sprite):
	def __init__(self, start_pos, target_pos, speed, max_length, characteristics, creator, name):
		super().__init__()
		self.name = name
		self.image = BULLETS[name.upper()]
		self.original_image = self.image
		self.speed = speed
		self.max_length = max_length
		self.distance_traveled = 0
		self.creator = creator
		self.start_pos = start_pos

		self.is_behind_cover = characteristics.get("is_behind_cover", False)
		self.explosion = characteristics.get("explosion", False)
		self.explosion_on_target = characteristics.get("explosion_on_target", False)

		if self.explosion_on_target:
			#print(self.max_length, target_pos)
			dx = target_pos[0] - start_pos[0] - config.zero_coordinate[0]
			dy = target_pos[1] - start_pos[1] - config.zero_coordinate[1]

			new_max_length = math.sqrt(dx**2 + dy**2)
			if new_max_length < self.max_length:
				self.max_length = new_max_length
			#print(self.max_length, new_max_length)

		dx = target_pos[0] - config.zero_coordinate[0] - start_pos[0]
		dy = target_pos[1] - config.zero_coordinate[1] - start_pos[1]

		#print(dx, dy)

		self.angle = math.degrees(math.atan2(-dy, dx)) - 90
		self.image = py.transform.rotate(self.original_image, self.angle)

		self.rect = self.image.get_rect(center=start_pos)
		self.pos = py.math.Vector2(start_pos)
		try:
			self.direction = py.math.Vector2(dx, dy).normalize()
		except:
			self.direction = (0, 0)
		init.bullets.add(self)

	def update(self):
		if self.direction != (0, 0):
			move_vector = self.direction * self.speed
			self.rect.center = (self.pos.x + config.zero_coordinate[0], self.pos.y + config.zero_coordinate[1])
			self.pos += move_vector
			self.distance_traveled += self.speed
		
		if not self.explosion_on_target:
			collided_obstacles = py.sprite.spritecollide(self, init.obstacles, False)
			collided_enemy = py.sprite.spritecollide(self, init.enemies, False) + py.sprite.spritecollide(self, init.enemies_tied_to_the_script, False)
			collided_player = py.sprite.spritecollide(self, init.player_group, False)
			collided_allies = py.sprite.spritecollide(self, init.allies, False)

			for obstacle in collided_obstacles:
				if obstacle.type in [0, 20]:
					if self.is_behind_cover and obstacle.type == 0:
						continue
					else:
						if self.explosion:
							self.do_explosion()
						self.kill()
						break
			if self.creator in init.enemies:
				for hitted in collided_player:
					if self.creator != None:
						self.hit(hitted)
				for hitted in collided_allies:
					self.hit(hitted)
			else:
				for hitted in collided_enemy:
					self.hit(hitted)

		if self.distance_traveled > self.max_length:
			if self.explosion:
				self.do_explosion()
			self.kill()
	
	def do_explosion(self):
		explosion_name = None
		if self.__class__.__name__ in ["Plasma_type2Bullet", "PlasmaBullet"]:
			explosion_name = "plasma"
		elif self.__class__.__name__ == "GrenadeBullet":
			explosion_name = "Grenade"
		if explosion_name == None:
			return

		explosion = Explosion(explosion_name, self.pos)

		self.explosion = False

		collided_enemy = py.sprite.spritecollide(explosion, init.enemies, False) + py.sprite.spritecollide(self, init.enemies_tied_to_the_script, False)
		collided_player = py.sprite.spritecollide(explosion, init.player_group, False)

		for hitted in collided_enemy:
			hitted.hit(self)
		for hitted in collided_player:
			hitted.hit(self)

		init.bullets.add(explosion)
	
	def hit(self, hitted):
		if hitted != self.creator:
			if self.explosion:
				self.do_explosion()
			hitted.hit(self)
			self.kill()

class Explosion(py.sprite.Sprite):
	def __init__(self, explosion_name, pos):
		super().__init__()
		self.image = EXPLOSION[explosion_name.upper()]
		self.rect = self.image.get_rect()
		self.pos = pos
		self.rect.center = (config.zero_coordinate[0] + pos[0], config.zero_coordinate[1] + pos[1])
		self.cooldown = 800
		self.update_time = py.time.get_ticks()
	
	def update(self):
		super().update()
		self.rect.center = (self.pos.x + config.zero_coordinate[0], self.pos.y + config.zero_coordinate[1])

		if py.time.get_ticks() - self.cooldown > self.update_time:
			self.kill()

class LaserBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 50, max_distace, {"is_behind_cover": is_behind_cover, "explosion": False}, creator, "laser")

class LaserBulletForStatic(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 50, max_distace, {"is_behind_cover": is_behind_cover, "explosion": False}, creator, "laser")

class BolterBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 30, max_distace, {"is_behind_cover": is_behind_cover, "explosion": False}, creator, "bolter")

class BigBolterBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 45, max_distace, {"is_behind_cover": is_behind_cover, "explosion": False}, creator, "bigbolter") #explosion изменить на True и добавить взрыв болтера

class PlasmaBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 20, max_distace, {"is_behind_cover": is_behind_cover, "explosion": True}, creator, "plasma")

class Plasma_type2Bullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 15, max_distace, {"is_behind_cover": True, "explosion": True, "explosion_on_target": True}, creator, "plasma")

class GrenadeBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 18, max_distace, {"is_behind_cover": True, "explosion": True, "explosion_on_target": True}, creator, "grenade")

class invisibleLaserBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 25, max_distace, {"is_behind_cover": is_behind_cover, "explosion": False}, creator, "notlaser")

class invisibleLaser_type0_ignorBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 25, max_distace, {"is_behind_cover": True, "explosion": False}, creator, "notlaser")

class BayonetBullet(Bullet):
	def __init__(self, start_pos, target_pos, max_distace, is_behind_cover, creator):
		super().__init__(start_pos, target_pos, 30, max_distace, {"is_behind_cover": True, "explosion": False}, creator, "bayonet")