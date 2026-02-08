import pygame
import os
vec2 = pygame.math.Vector2
from pygame.constants import *

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")
worker_sprite_sheet_path = os.path.join(assets_folder, "miner_worker_sheet.png")
worker_pic_path = os.path.join(assets_folder, "miner_worker.png")
worker_pic = pygame.image.load(worker_pic_path)
JUMP = -16
GRAVITY = 2

class Player(pygame.sprite.Sprite):
    """Base class for the different charachters"""

    """def fill_animation_frames(self, sprite_sheet: pygame.image, rows: int, width: int, height: int, scale: vec2):
        for row in rows:
            anim = ""
            if row == 0:
                anim = "idle"
            elif row == 1:
                anim = "run"
            elif row == 2:
                anim = "jump"
            elif row == 3:
                anim = "attack"
            elif row == 4:
                anim = "action"

            for frame in 8:
                self.animations[anim].append(pygame.image.load())"""
        


    def __init__(
        self,
        pos: vec2,
        scale: int,
        speed: int,
        sprite_path: os.path,
        physics_layer: list
        ):
        super().__init__()

    
        self.__scale: int = scale
        raw_image = pygame.image.load(sprite_path).convert_alpha()
        size = (16*scale, 16*scale)
        self.image_right = pygame.transform.scale(raw_image, size)
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.pos = pos
        self.rect = self.image.get_rect(center = pos)
        pygame.transform.scale(surface = self.image, size = (self.__scale * 16, self.__scale * 16))
        self.vel = vec2(0, 0)
        self.speed = speed
        self.physics_layer = physics_layer
        self.is_on_floor = True

        """
        self.h_flip = True
        self.animations = {"idle": [], "run": [], "jump": [], "attack": [], "action": []}
        self.curr_anim = "idle"
        self.animation_frame = 0
        """

    def move(self):
        #split up the input and the actions, and build a working jumping function
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.vel.x = -self.speed
            self.image = self.image_left
        elif pressed_keys[K_RIGHT]:
            self.vel.x = self.speed
            self.image = self.image_right
        else:
            self.vel.x = 0

        if self.is_on_floor and pressed_keys[K_SPACE]:
            if self.vel.y > -64:
                self.vel.y += JUMP
                self.is_on_floor = False

    """def animate(self):
        if self.curr_anim == "jump":
            pass
        elif self.h_flip:
            self.animations[self.curr_anim[self.animation_frame]]
        else:
            pass"""

    
    def update(self):
        self.move()
        
        self.vel.y += GRAVITY
        
        self.pos.x += self.vel.x
        self.rect.x = round(self.pos.x)
        for wall in self.physics_layer:
            if self.rect.colliderect(wall):
                if self.vel.x > 0: self.rect.right = wall.left
                if self.vel.x < 0: self.rect.left = wall.right
                self.pos.x = self.rect.x
                self.vel.x = 0

        self.is_on_floor = False
        self.pos.y += self.vel.y
        self.rect.y = round(self.pos.y)
        for wall in self.physics_layer:
            if self.rect.colliderect(wall):
                if self.vel.y > 0: 
                    self.rect.bottom = wall.top
                    self.vel.y = 0
                    self.is_on_floor = True
                elif self.vel.y < 0:
                    self.rect.top = wall.bottom
                    self.vel.y = 0
                self.pos.y = self.rect.y

    
        


class Worker(Player):
    def __init__(
        self,
        pos: vec2,
        scale: float,
        speed: int,
        physics_layer: list
            ):
        super().__init__(pos ,scale , speed, sprite_path = worker_pic_path, physics_layer = physics_layer)
        


class Engineer(Player):
    pass



class Scout(Player):
    pass



class Automaton(Player):
    pass
