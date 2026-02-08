import pygame
import os
import sys

this_file = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(this_file)
sys.path.append(parent_dir)

pygame.init()
display = pygame.display.set_mode((320, 160))
sprite_sheet = None
try:
    sprite_sheet = pygame.image.load("mine_worker.png").convert_alpha() 
except Exception as e:
    print(f"exception:{e}")


class PL(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = sprite_sheet
        self.rect = image
    
