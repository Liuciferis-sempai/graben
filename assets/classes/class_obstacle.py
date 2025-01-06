import pygame as py
from assets.config import *
from assets.sprits import *
import assets.config as config
import assets.initialization as init
import random
from assets.commands import *

class Obstacle(py.sprite.Sprite):
    # Предварительно масштабированные изображения
    def __init__(self, position_on_map: list, coords: list, cell: str):
        super().__init__()
        if init.game_map["map_version"] == "0.1":
            cell = VERSION_TRANSLATION[cell]
        cell = cell.split("_")
        cell_type = self._get(cell, 0, "o")
        cell_angle = tr_int(self._get(cell, 1, 0), 0)
        self.image = BLIT_MAP[cell_type]
        self.image = py.transform.rotate(self.image, cell_angle)
        self.rect = self.image.get_rect()
        self.rect.topleft = position_on_map
        self.type = cell_type
        self.angle = cell_angle
        self.group = self._get(cell, 2, "0")


        if self.type == "O":
            self.frame_index = 0
            self.animations = [
                py.transform.scale(TERRAIN_IMAGES["bunker 0"], (config.CELL_SIZE, config.CELL_SIZE)),
                py.transform.scale(TERRAIN_IMAGES["bunker 1"], (config.CELL_SIZE, config.CELL_SIZE))
            ]
            self.cooldown = random.randint(config.BUNKER_COOLDOWN[0], config.BUNKER_COOLDOWN[1])
            self.last_animation_update_time = py.time.get_ticks()
            init.animated_obstacle.append(self)
        self.coords = coords

    def _get(self, request: list, index: int, default):
        try:
            return request[index]
        except:
            return default

    def add_to_group(self):
        if self.group == "0":
            init.chr_collision_and_bullet_collision.add(self)
        elif self.group == "1":
            init.bullet_collision.add(self)
        elif self.group == "2":
            init.interactive_cells.add(self)
        elif self.group == "3":
            init.chr_collision.add(self)
        elif self.group == "4":
            init.no_collision.add(self)
    
    def animation_update(self):
        if py.time.get_ticks() - self.last_animation_update_time > self.cooldown:
            self.last_animation_update_time = py.time.get_ticks()
            self.image = self.animations[self.frame_index]
            self.frame_index += 1
            if self.frame_index >= len(self.animations):
                self.frame_index = 0

class Mark(py.sprite.Sprite):
    def __init__(self, position_on_map, coords, cell):
        super().__init__()
        self.image = MARKS_IMAGES[cell]
        self.rect = self.image.get_rect()
        self.rect.topleft = position_on_map
        self.coords = coords

        init.markers.add(self)

class S_Mark(Mark):
    def __init__(self, position_on_map, coords):
        super().__init__(position_on_map, coords, "s")

class C_Mark(Mark):
    def __init__(self, position_on_map, coords):
        super().__init__(position_on_map, coords, "c")

class P_Mark(Mark):
    def __init__(self, position_on_map, coords):
        super().__init__(position_on_map, coords, "p")

class M_Mark(Mark):
    def __init__(self, position_on_map, coords):
        super().__init__(position_on_map, coords, "frame")

class F_Mark(Mark):
    def __init__(self, position_on_map, coords):
        super().__init__(position_on_map, coords, "f")