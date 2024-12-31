import pygame as py
import assets.config as config
import assets.initialization as init
from assets.sprits import ICONS

class GUI(py.sprite.Sprite):
	'''
	graphical user interface
	'''
	def __init__(self):
		super().__init__()

		self.load_ico()

		self.is_boss_fight = False
		self.boss = None
	
	def load_ico(self):
		'''
		Загружает иконки в ГПИ
		'''
		self.hp_ico = ICONS["HP"]

		self.plasma_mode = [ICONS["PLASMA_MODE_0"], ICONS["PLASMA_MODE_1"]]

		self.grenade_ico = ICONS["GRENADE"]

		self.main_weapon_ico = ICONS[init.player.main_weapon.name.upper()]

		self.secondary_weapon_ico = ICONS[init.player.second_weapon.name.upper()]

		self.my_font = py.font.SysFont('Comic Sans MS', config.CELL_SIZE//4)
	
	def draw(self):
		'''
		Рисует все элементы интерфейса
		'''
		self.draw_hp()
		if init.player.main_weapon.name == "Plasmagun":
			self.draw_plasma_mode()
		self.draw_grenade()
		self.draw_main_weapon()
		self.draw_secondary_weapon()
		self.draw_ammunition()
		if self.is_boss_fight:
			self.draw_boss_hp()
	
	def draw_hp(self):
		'''
		Рисует полоску здоровья
		'''
		hp = init.player.hp
		for i in range(hp):
			init.screen.blit(self.hp_ico, [config.CELL_SIZE*i, 0])
	
	def draw_plasma_mode(self):
		'''
		Рисует режим стрельбы плазмой
		'''
		mode = init.player.weapon_mode
		init.screen.blit(self.plasma_mode[mode], [0, config.CELL_SIZE*1.5])
	
	def draw_grenade(self):
		'''
		Рисует количество гранат
		'''
		grenades = init.player.grenade_count
		for i in range(grenades):
			init.screen.blit(self.grenade_ico, [config.CELL_SIZE*i, config.CELL_SIZE*1.1])
	
	def draw_main_weapon(self):
		'''
		Рисует активное оружие
		'''
		init.screen.blit(self.main_weapon_ico, [config.CELL_SIZE*3+config.CELL_SIZE//4, 0])
	
	def draw_secondary_weapon(self):
		'''
		рисует запасное оружие игрока
		'''
		init.screen.blit(self.secondary_weapon_ico, [config.CELL_SIZE*5.5, 0])
	
	def draw_ammunition(self):
		'''
		Рисует количество патрон
		'''
		text_surface = self.my_font.render(f"{init.player.active_weapon.ammo_in_weapon} / {init.player.active_weapon.ammo_in_pocket}", False, config.COLOR_BLACK)
		init.screen.blit(text_surface, [config.CELL_SIZE*3+config.CELL_SIZE//4, config.CELL_SIZE*1.1])
	
	def draw_boss_hp(self):
		'''
		Рисует дизни босса
		'''
		text_surface = self.my_font.render(f"{init.languages[init.settings["language"]][self.boss.name]} / {self.boss.hp}", False, config.COLOR_BLACK)
		hp_surface = py.surface.Surface([config.CELL_SIZE//20, config.CELL_SIZE//8])
		hp_surface.fill(config.COLOR_RED)
		for i in range(self.boss.hp//20):
			init.screen.blit(hp_surface, [config.window_size[0]-config.CELL_SIZE//10*i-config.CELL_SIZE//10, 0])
		init.screen.blit(text_surface, [config.window_size[0]-text_surface.get_width()-config.CELL_SIZE, config.CELL_SIZE//8])