from assets.classes.class_bullets import *

class Weapon():
	def __init__(self, name: str = "none", bullet_type: str = "none", auto: bool = False, cooldown: int = 1000, max_distance: int = 0, ammo_in_weapon_max: int = 0, ammo_in_pocket_max: int = 0):
		self.name = name 
		self.bullet_type = bullet_type
		self.automatic = auto
		self.cooldown = cooldown
		self.has_second_shoot_mod = False
		self.max_distance = max_distance
		self.ammo_in_weapon_max = ammo_in_weapon_max
		self.ammo_in_pocket_max = ammo_in_pocket_max
		self.ammo_in_pocket = ammo_in_pocket_max
		self.ammo_in_weapon = ammo_in_weapon_max
	
	def shoot(self, start_pos, target_pos, is_behind_cover, creator):
		if self.bullet_type == "laser":
			LaserBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		elif self.bullet_type == "bolter":
			BolterBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		elif self.bullet_type == "bigbolter":
			BigBolterBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		elif self.bullet_type == "plasma":
			PlasmaBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		elif self.bullet_type == "bayonet":
			BayonetBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		elif self.bullet_type == "fire":
			Fire(start_pos, target_pos, self.max_distance, creator)
		elif self.bullet_type == "fragmentation grenade":
			GrenadeBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
		else:
			invisibleLaserBullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)
	
	def alt_shoot(self, start_pos, target_pos, is_behind_cover, creator):
		if self.bullet_type == "plasma":
			Plasma_type2Bullet(start_pos, target_pos, self.max_distance, is_behind_cover, creator)

class Boltgun(Weapon):
	def __init__(self):
		super().__init__("Boltgun", "bolter", True, 200, config.CELL_SIZE*15, 30, 90)

class Boltrifle(Weapon):
	def __init__(self):
		super().__init__("Boltrifle", "bigbolter", True, 500, config.CELL_SIZE*20, 45, 255)

class Boltpistol(Weapon):
	def __init__(self):
		super().__init__("Boltpistol", "bolter", True, 600, config.CELL_SIZE*10, 5, 25)

class Lasgun(Weapon):
	def __init__(self):
		super().__init__("Lasgun", "laser", False, 500, config.CELL_SIZE*15, 20, 120)

class Plasmagun(Weapon):
	def __init__(self):
		super().__init__("Plasmagun", "plasma", False, 1000, config.CELL_SIZE*7, 5, 30)
		self.has_second_shoot_mod = True

class Bayonet(Weapon):
	def __init__(self):
		super().__init__("Bayonet", "bayonet", True, 200, config.CELL_SIZE//2)
	
class Flamethrower(Weapon):
	def __init__(self):
		super().__init__("Flamethrower", "fire", True, 100, config.CELL_SIZE*10, 100, 500)

class FragmentationGrenade(Weapon):
	def __init__(self):
		super().__init__("Grenade", "fragmentation grenade", True, 2000, config.CELL_SIZE*5)