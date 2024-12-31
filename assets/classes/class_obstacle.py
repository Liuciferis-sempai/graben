import pygame as py
from assets.config import *
from assets.sprits import *
import assets.config as config
import assets.initialization as init
import random

class Obstacle(py.sprite.Sprite):
    # Предварительно масштабированные изображения
    def __init__(self, coords, position_on_map, obstacle_type):
        super().__init__()
        self.image = IMAGE_MAP.get(OBSTACLE_MAP[obstacle_type], DIRT)  # Подстраховка на случай некорректного типа
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.type = OBSTACLE_MAP[obstacle_type]
        if self.type == 25:
            self.frame_index = 0
            self.animations = [
                py.transform.scale(B_0, (config.CELL_SIZE, config.CELL_SIZE)),
                py.transform.scale(B_1, (config.CELL_SIZE, config.CELL_SIZE))
            ]
            self.cooldown = random.randint(config.BUNKER_COOLDOWN[0], config.BUNKER_COOLDOWN[1])
            self.last_animation_update_time = py.time.get_ticks()
            init.animated_obstacle.append(self)
        self.coords = coords
        self.position = position_on_map
    
    def animation_update(self):
        if py.time.get_ticks() - self.last_animation_update_time > self.cooldown:
            self.last_animation_update_time = py.time.get_ticks()
            self.image = self.animations[self.frame_index]
            self.frame_index += 1
            if self.frame_index >= len(self.animations):
                self.frame_index = 0

    def on_collision(self, ray):
        print(f"Obstacle hit by ray at {ray.rect.center}")

class S_Mark(Obstacle):
    def __init__(self, coords, position_on_map):
        super().__init__(coords, position_on_map, 28)

class C_Mark(Obstacle):
    def __init__(self, coords, position_on_map):
        super().__init__(coords, position_on_map, 27)

class P_Mark(Obstacle):
    def __init__(self, coords, position_on_map):
        super().__init__(coords, position_on_map, 38)

class M_Mark(Obstacle):
    def __init__(self, coords, position_on_map):
        super().__init__(coords, position_on_map, 39)