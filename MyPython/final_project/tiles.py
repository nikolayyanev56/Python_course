import pygame
from pygame.constants import *
import os
vec2 = pygame.math.Vector2

game_folder = os.path.dirname(__file__)
assets_folder = os.path.join(game_folder, "assets")
test_platform_path = os.path.join(assets_folder, "test_platform.png")

class StaticTile(pygame.sprite.Sprite):
    """Base class for all tiles in the game"""
    
    def __init__(
            self,
            pos: vec2,
            sprite_path: os.path 
            ):
            super().__init__()
            
            self.image = pygame.image.load(sprite_path)
            self.rect = self.image.get_rect(center = pos)


class BaseHorizontalMoveTile(StaticTile):
      def __init__(self, pos, sprite_path):
            super().__init__(pos, sprite_path)


class TestTile(StaticTile):
      def __init__(self, pos: vec2):
            super().__init__(pos, sprite_path = test_platform_path)