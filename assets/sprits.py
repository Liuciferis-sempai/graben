import pygame as py
from assets.image_loader import resource_path
import assets.config as config

#Terrein
DIRT = py.image.load(resource_path("assets\image\Terrein\dirt.png"))
T_V = py.image.load(resource_path("assets\image\Terrein\_trench_V.png"))
T_G = py.image.load(resource_path("assets\image\Terrein\_trench_G.png"))
T_F_X = py.image.load(resource_path("assets\image\Terrein\_trench_F_X.png"))
T_1X = py.image.load(resource_path("assets\image\Terrein\_trench_T1_X.png"))
T_2X = py.image.load(resource_path("assets\image\Terrein\_trench_T2_X.png"))
T_3X = py.image.load(resource_path("assets\image\Terrein\_trench_T3_X.png"))
T_4X = py.image.load(resource_path("assets\image\Terrein\_trench_T4_X.png"))
G_1X = py.image.load(resource_path("assets\image\Terrein\_trench_G1_X.png"))
G_2X = py.image.load(resource_path("assets\image\Terrein\_trench_G2_X.png"))
G_3X = py.image.load(resource_path("assets\image\Terrein\_trench_G3_X.png"))
G_4X = py.image.load(resource_path("assets\image\Terrein\_trench_G4_X.png"))
D_B = py.image.load(resource_path("assets\image\Terrein\dirt_with_barbwire.png"))
T_M = py.image.load(resource_path("assets\image\Terrein\_trench_M.png"))
T_1B = py.image.load(resource_path("assets\image\Terrein\_trench_with_obstacle_1.png"))
T_2B = py.image.load(resource_path("assets\image\Terrein\_trench_with_obstacle_2.png"))
T_EC = py.image.load(resource_path("assets\image\Terrein\empty_trench.png"))
T_1C = py.image.load(resource_path("assets\image\Terrein\_trench_cell_1.png"))
T_2C = py.image.load(resource_path("assets\image\Terrein\_trench_cell_2.png"))
T_3C = py.image.load(resource_path("assets\image\Terrein\_trench_cell_3.png"))
T_4C = py.image.load(resource_path("assets\image\Terrein\_trench_cell_4.png"))
WALL = py.image.load(resource_path("assets\image\Terrein\wall.png"))
S_FLOOR = py.image.load(resource_path("assets\image\Terrein\stone_floor.png"))
ART_B = py.image.load(resource_path("assets\image\Terrein\Art_barrel.png"))
ART_S = py.image.load(resource_path("assets\image\Terrein\Art_layer_station.png"))
ART_A = py.image.load(resource_path("assets\image\Terrein\Art_ammo.png"))
B_0 = py.image.load(resource_path("assets\image\Terrein\Bunker_0.png"))
B_1 = py.image.load(resource_path("assets\image\Terrein\Bunker_1.png"))
T_MORTAL_DOWN = py.image.load(resource_path("assets\image\Terrein\mortal_down.png"))
T_MORTAL_UP = py.image.load(resource_path("assets\image\Terrein\mortal_up.png"))
T_MORTAL_LEFT = py.image.load(resource_path("assets\image\Terrein\mortal_left.png"))
T_MORTAL_RIGHT = py.image.load(resource_path("assets\image\Terrein\mortal_right.png"))
BED_DOWN = py.image.load(resource_path("assets\image\Terrein\Bed_down.png"))
BED_UP = py.image.load(resource_path("assets\image\Terrein\Bed_up.png"))
BED_LEFT = py.image.load(resource_path("assets\image\Terrein\Bed_left.png"))
BED_RIGHT = py.image.load(resource_path("assets\image\Terrein\Bed_right.png"))

S = py.image.load(resource_path("assets\image\Terrein\s.png"))
C = py.image.load(resource_path("assets\image\Terrein\c.png"))
P = py.image.load(resource_path("assets\image\Terrein\p.png"))
FRAME = py.image.load(resource_path("assets\image\Terrein\Frame.png"))

TRANSLATION = [
	["o", "dirt 0"],
	["s", "dirt 1"],
	["T", "v trench", "v t", "t 0 0 1 1"],
	["t", "h trench", "h t", "g trench", "g t", "t 1 1 0 0"],
	["A", "a cross", "x 1 1 1 1", "t 1 1 1 1"],
	["Q", "q cross", "x 0 1 1 1", "t 0 1 1 1"],
	["W", "w cross", "x 1 0 1 1", "t 1 0 1 1"],
	["E", "e cross", "x 1 1 1 0", "t 1 1 1 0"],
	["R", "r cross", "x 1 1 0 1", "t 1 1 0 1"],
	["Z", "z cross", "x 1 0 1 0", "t 1 0 1 0"],
	["U", "u cross", "x 1 0 0 1", "t 1 0 0 1"],
	["I", "i cross", "x 0 1 0 1", "t 0 1 0 1"],
	["P", "p cross", "x 0 1 1 0", "t 0 1 1 0"],
	["l", "v prickle"],
    ["M", "mg up"],
    ["B", "v trench blocked", "v trench b", "v trench o", "v t b"],
    ["e", "e trench", "empty"],
    ["q", "cell 1", "trench cell 1"],
    ["w", "cell 2", "trench cell 2", "ammo cell"],
    ["O", "cell 3", "trench cell 3", "medic cell"],
    ["p", "cell 4", "trench cell 4"],
    ["b", "h trench blocked", "h trench b", "h trench o", "g trench blocked", "g trench b", "g trench o", "h t b", "h t o", "g t o", "g t b"],
    ["K", "stone wall"],
    ["k", "stone floor"],
    ["h", "art barrel", "art 1", "art1"],
    ["H", "art station", "art 2", "art2", "art s"],
    ["a", "art ammo"],
    ["n", "bunker"],
    ["d", "mortal down", "mortal d"],
    ["S", "mortal up", "mortal u"],
    ["D", "mortal left", "mortal l"],
    ["f", "mortal right", "mortal r"],
    ["r", "bed down", "bed d"],
    ["z", "bed up", "bed u"],
    ["u", "bed left", "bed l"],
    ["i", "bed right", "bed r"]
]

OBSTACLE_MAP = {
	"o": 0,
	"T": 1,
	"t": 2,
	"A": 3,
	"Q": 4,
	"W": 5,
	"E": 6,
	"R": 7,
	"Z": 8,
	"U": 9,
	"I": 10,
	"P": 11,
	"l": 12,
	"M": 13,
	"B": 14,
	"e": 15,
	"q": 16,
	"w": 17,
	"b": 18,
	"s": 19,
	"K": 20,
	"k": 21,
	"h": 22,
	"H": 23,
	"a": 24,
	"n": 25,
    "d": 26,
    27: 27,
    28: 28,
    "r": 29,
    "z": 30,
    "u": 31,
    "i": 32,
    "O": 33,
    "p": 34,
    "S": 35,
    "D": 36,
    "f": 37,
    38: 38,
    39: 39
}
IMAGE_MAP = {
	0: py.transform.scale(DIRT, (config.CELL_SIZE, config.CELL_SIZE)),
	1: py.transform.scale(T_V, (config.CELL_SIZE, config.CELL_SIZE)),
	2: py.transform.scale(T_G, (config.CELL_SIZE, config.CELL_SIZE)),
	3: py.transform.scale(T_F_X, (config.CELL_SIZE, config.CELL_SIZE)),
	4: py.transform.scale(T_1X, (config.CELL_SIZE, config.CELL_SIZE)),
	5: py.transform.scale(T_2X, (config.CELL_SIZE, config.CELL_SIZE)),
	6: py.transform.scale(T_3X, (config.CELL_SIZE, config.CELL_SIZE)),
	7: py.transform.scale(T_4X, (config.CELL_SIZE, config.CELL_SIZE)),
	8: py.transform.scale(G_1X, (config.CELL_SIZE, config.CELL_SIZE)),
	9: py.transform.scale(G_2X, (config.CELL_SIZE, config.CELL_SIZE)),
	10: py.transform.scale(G_3X, (config.CELL_SIZE, config.CELL_SIZE)),
	11: py.transform.scale(G_4X, (config.CELL_SIZE, config.CELL_SIZE)),
	12: py.transform.scale(D_B, (config.CELL_SIZE, config.CELL_SIZE)),
	13: py.transform.scale(T_M, (config.CELL_SIZE, config.CELL_SIZE)),
	14: py.transform.scale(T_1B, (config.CELL_SIZE, config.CELL_SIZE)),
	15: py.transform.scale(T_EC, (config.CELL_SIZE, config.CELL_SIZE)),
	16: py.transform.scale(T_1C, (config.CELL_SIZE, config.CELL_SIZE)),
	17: py.transform.scale(T_2C, (config.CELL_SIZE, config.CELL_SIZE)),
	18: py.transform.scale(T_2B, (config.CELL_SIZE, config.CELL_SIZE)),
	19: py.transform.scale(DIRT, (config.CELL_SIZE, config.CELL_SIZE)),
	20: py.transform.scale(WALL, (config.CELL_SIZE, config.CELL_SIZE)),
	21: py.transform.scale(S_FLOOR, (config.CELL_SIZE, config.CELL_SIZE)),
	22: py.transform.scale(ART_B, (config.CELL_SIZE, config.CELL_SIZE)),
	23: py.transform.scale(ART_S, (config.CELL_SIZE, config.CELL_SIZE)),
	24: py.transform.scale(ART_A, (config.CELL_SIZE, config.CELL_SIZE)),
	25: py.transform.scale(B_0, (config.CELL_SIZE, config.CELL_SIZE)),
    26: py.transform.scale(T_MORTAL_DOWN, (config.CELL_SIZE, config.CELL_SIZE)),
    27: py.transform.scale(C, (config.CELL_SIZE, config.CELL_SIZE)),
    28: py.transform.scale(S, (config.CELL_SIZE, config.CELL_SIZE)),
    29: py.transform.scale(BED_DOWN, (config.CELL_SIZE, config.CELL_SIZE)),
    30: py.transform.scale(BED_UP, (config.CELL_SIZE, config.CELL_SIZE)),
    31: py.transform.scale(BED_LEFT, (config.CELL_SIZE, config.CELL_SIZE)),
    32: py.transform.scale(BED_RIGHT, (config.CELL_SIZE, config.CELL_SIZE)),
    33: py.transform.scale(T_3C, (config.CELL_SIZE, config.CELL_SIZE)),
    34: py.transform.scale(T_4C, (config.CELL_SIZE, config.CELL_SIZE)),
    35: py.transform.scale(T_MORTAL_UP, (config.CELL_SIZE, config.CELL_SIZE)),
    36: py.transform.scale(T_MORTAL_LEFT, (config.CELL_SIZE, config.CELL_SIZE)),
    37: py.transform.scale(T_MORTAL_RIGHT, (config.CELL_SIZE, config.CELL_SIZE)),
    38: py.transform.scale(P, (config.CELL_SIZE//2, config.CELL_SIZE//2)),
    39: py.transform.scale(FRAME, (config.CELL_SIZE, config.CELL_SIZE))
}

CHARACTERS = {
	"WALRAM": {
        "PORTRAIT": py.transform.scale(py.image.load(resource_path("assets\image\portraits\walram.png")), (config.CELL_SIZE, config.CELL_SIZE*2)),
        "LASGUN": {
            "WAITING": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_waiting\{i}.png")).convert_alpha() for i in range(3)],
            "WALKING": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_walking\{i}.png")).convert_alpha() for i in range(6)],
            "RUNNING": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_running\{i}.png")).convert_alpha() for i in range(6)],
            "SHOOTING": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_shooting\{i}.png")).convert_alpha() for i in range(4)],
            "AIMING": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_aiming\{i}.png")).convert_alpha() for i in range(3)],
            "DEAD": [py.image.load(resource_path(f"assets\image\walram\Lasgun\_dead\{i}.png")).convert_alpha() for i in range(2)]
		},
        "BOLTPISTOL": {
            "WAITING": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_waiting\{i}.png")).convert_alpha() for i in range(3)],
            "WALKING": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_walking\{i}.png")).convert_alpha() for i in range(6)],
            "RUNNING": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_running\{i}.png")).convert_alpha() for i in range(6)],
            "SHOOTING": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_shooting\{i}.png")).convert_alpha() for i in range(4)],
            "AIMING": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_aiming\{i}.png")).convert_alpha() for i in range(3)],
            "DEAD": [py.image.load(resource_path(f"assets\image\walram\Boltpistol\_dead\{i}.png")).convert_alpha() for i in range(2)]
		}
	},
    "BLOODPACKSOLDIER": {
        "PORTRAIT": py.transform.scale(py.image.load(resource_path("assets\image\portraits\_blood_pack_soldier.png")), (config.CELL_SIZE, config.CELL_SIZE*2)),
		"LASGUN": {
	        "WAITING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Lasgun\_waiting\{i}.png")).convert_alpha() for i in range(3)],
            "SHOOTING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Lasgun\_shooting\{i}.png")).convert_alpha() for i in range(1)],
            "AIMING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Lasgun\_aiming\{i}.png")).convert_alpha() for i in range(3)],
            "DEAD": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Lasgun\_dead\{i}.png")).convert_alpha() for i in range(1)]
        },
        "PLASMAGUN": {
            "WAITING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Plasmagun\_waiting\{i}.png")).convert_alpha() for i in range(3)],
            "SHOOTING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Plasmagun\_shooting\{i}.png")).convert_alpha() for i in range(1)],
            "AIMING": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Plasmagun\_aiming\{i}.png")).convert_alpha() for i in range(3)],
            "DEAD": [py.image.load(resource_path(f"assets\image\_bloodpactsoldier\Plasmagun\_dead\{i}.png")).convert_alpha() for i in range(1)]
		}
	},
    "WORLD_EATER": {
        "PORTRAIT": py.transform.scale(py.image.load(resource_path("assets\image\portraits\world_eater.png")), (config.CELL_SIZE, config.CELL_SIZE*2)),
        "BOLTRIFLE": {
            "WAITING": [py.image.load(resource_path(f"assets\image\space_marines\world_eater\Boltrifle\_waiting\{i}.png")).convert_alpha() for i in range(1)],
            "SHOOTING": [py.image.load(resource_path(f"assets\image\space_marines\world_eater\Boltrifle\_shooting\{i}.png")).convert_alpha() for i in range(1)],
            "AIMING": [py.image.load(resource_path(f"assets\image\space_marines\world_eater\Boltrifle\_aiming\{i}.png")).convert_alpha() for i in range(1)],
            "DEAD": [py.image.load(resource_path(f"assets\image\space_marines\world_eater\Boltrifle\_dead\{i}.png")).convert_alpha() for i in range(1)]
		}
	},
    "COMMISSAR": {
        "PORTRAIT": py.transform.scale(py.image.load(resource_path("assets\image\portraits\commissar.png")), (config.CELL_SIZE, config.CELL_SIZE*2)),
        "_": py.image.load(resource_path("assets\image\commissar\commissar.png"))
	},
    "SALAMANDER": {
        "PORTRAIT": py.transform.scale(py.image.load(resource_path("assets\image\portraits\salamander.png")), (config.CELL_SIZE, config.CELL_SIZE*2)),
	}
}

BULLETS = {
    "BOLTER": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/bolter.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "LASER": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/laser.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "BIGBOLTER": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/bigbolter.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "FIRE": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/fire.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "GRENADE": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/grenade.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "NOTLASER": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/notlaser.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "PLASMA": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/plasma.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
    "BAYONET": py.transform.scale(py.image.load(resource_path(f"assets/image/bullets/bayonet.png")).convert_alpha(), (config.CELL_SIZE//10, config.CELL_SIZE//4)),
}

EXPLOSION = {
    "GRENADE": py.transform.scale(py.image.load(resource_path(f"assets/image/other/Grenade_explosion.png")).convert_alpha(), (config.CELL_SIZE*2, config.CELL_SIZE*2)),
    "PLASMA": py.transform.scale(py.image.load(resource_path(f"assets/image/other/plasma_explosion.png")).convert_alpha(), (config.CELL_SIZE*2, config.CELL_SIZE*2)),
}

ICONS = {
    "HP": py.transform.scale(py.image.load(resource_path("assets\image\other\hp.png")), (config.CELL_SIZE, config.CELL_SIZE)),
    "PLASMA_MODE_0": py.transform.scale(py.image.load(resource_path("assets\image\other\plasma_mod_0.png")), (config.CELL_SIZE, config.CELL_SIZE)),
    "PLASMA_MODE_1": py.transform.scale(py.image.load(resource_path("assets\image\other\plasma_mod_1.png")), (config.CELL_SIZE, config.CELL_SIZE)),
    "GRENADE": py.transform.scale(py.image.load(resource_path("assets\image\weapon\Grenade.png")), (config.CELL_SIZE//2, config.CELL_SIZE//2)),
    "LASGUN": py.transform.scale(py.image.load(resource_path(f"assets\image\weapon\Lasgun.png")), (config.CELL_SIZE*2, config.CELL_SIZE)),
    "BOLTPISTOL": py.transform.scale(py.image.load(resource_path(f"assets\image\weapon\Boltpistol.png")), (config.CELL_SIZE*2, config.CELL_SIZE)),
    "PLASMAGUN": py.transform.scale(py.image.load(resource_path(f"assets\image\weapon\Plasmagun.png")).convert_alpha(), (config.CELL_SIZE//2, config.CELL_SIZE//4)),
    "NONE": py.transform.scale(py.image.load(resource_path(f"assets\image\weapon\_none.png")).convert_alpha(), (config.CELL_SIZE//2, config.CELL_SIZE//4)),
}