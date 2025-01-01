running = True

window_size = [1920, 1200]
scale_factor = 1
CELL_SIZE = 150
FPS = 30
FONT_SIZE = 30
ANIMATION_COOLDOWN = 200
BUNKER_COOLDOWN = [100, 200]

zero_coordinate = [0, 0]
SCATTER = CELL_SIZE//3
last_time_update = 0
is_console_open = False
has_tracked_enemys = True

CHARACTERs_TYPES = [
    "enemies",
    "allies",
    "boss",
    "enemies_tied_to_the_script"
]

state_of_the_game = {
	"main menu": True,
    "statistics": False,
	"settings": False,
	"game mode selection": False,
    "editor": False,
	"level selection": False,
	"menu": False,
	"game": False
}

state_of_editor = {
    "main location": False,
    "main weapon choise": False,
    "second weapon choise": False,
    "melee weapon choise": False,
    "grenade choise": False,
    "editing a map": False
}

moving = {
	"forward": False,
	"left": False, 
	"right": False,
	"back": False,
	"taking aim": False,
	"run": False,
	"auto fire": False,
	"fire": False,
	"cut scene": False
}

#Характеристики
PlAYER_MAX_HP = 3
PLAYER_SPEED = 10
FIRE_EXIST = 5

#Характеристики врагов
BLOOD_PACK_SOLDIER_HP = 1
BLOOD_PACK_SOLDIER_SPEED = 5
WORLD_EATER_HP_MAX = 1000
WORLD_EATER_SPEED = 12

#Характеристики Союзников
COMMISSAR_SPEED = 10

#ЦВЕТА
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (36, 36, 36)
COLOR_BROWN = (153, 76, 0)
COLOR_DARK_BROWN = (102, 51, 0)
COLOR_DIRT = (106, 86, 0)

#o - dirt (not passable)
#s - dirt (passable)

#T - trench V
#t - trench G

#c - Chechpoint on T
#C - Chechpoint on t
#H - Chechpoint on empty trench cell
#h - Chechpoint on dirt

#e - empty trench cell
#q - trench cell (type 1)
#w - trench cell (type 2)

#A - trench F

#Q - trench T1
#W - trench T2
#E - trench T3
#R - trench T4

#Z - trench G1
#U - trench G2 / u - with Chechpoint
#I - trench G3 / i - with Chechpoint
#P - trench G4

#B - trench (V) with obstacle (type 1)
#b - trench (G) with obstacle (type 2)

#l - dirt with barbwire (V)
#

#M - MG

#Карта
#при создании персонажа, сначала указывать столбец, а потом линию. к обеим координатам прибавить 1/4 от CELL_SIZE