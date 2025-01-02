import pygame as py
import assets.config as config

screen = py.display.set_mode((config.window_size), py.RESIZABLE)

from assets.maps import MAPS
game_map = MAPS["MAP_0"]
loaded_map = 0

from assets.classes.class_board import Board
from assets.classes.class_weapon import *

player_group = py.sprite.Group()
enemies = py.sprite.Group()
allies = py.sprite.Group()
chr_collision = py.sprite.Group() #группа для проверки на колюзию у персонажей
bullet_collision = py.sprite.Group() #группа для проверки на колюзию у пуль
chr_collision_and_bullet_collision = py.sprite.Group() #группа для проверки на колюзию у персонажей и пуль
no_collision =  py.sprite.Group() #все остальные
bullets = py.sprite.Group()
items = py.sprite.Group()
markers = py.sprite.Group()
enemies_tied_to_the_script = py.sprite.Group()

dialogue = None
texts = []
animated_obstacle = []

#разные списки кнопок
buttons_on_main_menu = []
buttons_game_mode_selection = []
buttons_level_selection = []
buttons_menu = []
buttons_settings = []
buttons_statistics = []
buttons_editor = []

board = Board()

from assets.classes.class_character import Walram
player = Walram()
player_group.add(player)

from assets.classes.class_gui import GUI
gui = GUI()

languages = None
settings = None
save = None
old_settings = None
from assets.classes.class_scripts import Scripts
scripts = Scripts()
scripts.map_loader()
scripts.load_settings()
scripts.load_languages()
scripts.load_save()
old_settings = settings.copy()

from editor import EditorScreen
editor = EditorScreen()

from console import Console
console = Console()