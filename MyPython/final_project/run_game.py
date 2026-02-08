import pygame
import sys
import os
from pygame.constants import *
from player import Worker
from tiles import TestTile
vec2 = pygame.math.Vector2
from tilemap import build_static_layer
import json

pygame.init()
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h
FPS = 60

display_surf = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Winter game py")
frame_per_sec = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
test_level_path = os.path.join(game_folder, "test_level.json")
assets_path = os.path.join(game_folder, "assets")
atlas_path = os.path.join(assets_path, "icy_tiles.png")
tiledata = None
with open(test_level_path,"r") as tiles:
    tiledata = json.load(tiles)
tiles.close()

tilemap_rect = pygame.rect.Rect(28 * 16, 21 * 16, 16, 16)
static_layer, physics_layer = build_static_layer(tiledata, 16, tilemap_rect, atlas_path)
all_sprites = pygame.sprite.Group()
all_sprites.add()
PL = Worker(pos = vec2(160, 90),scale = 1 , speed = 4, physics_layer = physics_layer)

all_sprites.add(PL)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    display_surf.fill((0, 0, 0))
    PL.update()
    display_surf.blit(static_layer, (0, 0))
    all_sprites.draw(display_surf)

    pygame.display.update()
    frame_per_sec.tick(FPS)