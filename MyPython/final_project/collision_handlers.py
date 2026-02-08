import pygame
from player import Player
from tiles import BaseTile

class Player_Collider():
    def __init__(self, player: Player, physics_layer: list, tile_size: int):
        self.player_rect = player.rect
        self.physics_layer = physics_layer
        self.tile_size = tile_size

    def wall_snap(self):
        player_x = self.player_rect.x // self.tile_size
        player_y = self.player_rect.y // self.tile_size

        