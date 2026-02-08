"""Handles the resizing of the screen and the intitializiation of the window"""

import pygame
import sys
from pygame.locals import *
from pygame import display
from player import Player
from tiles import BasePlatform

pygame.init()
window = None

def create_fullscren():
    """
    Create an initial fullscreen for the game
    from the monitor size of the computer
    """

    screen_info = pygame.display.Info()
    screen_w = screen_info.current_w
    screen_h = screen_info.current_h

    full = pygame.display.set_mode((screen_w, screen_h), RESIZABLE)
    full.fill((0,0,0))
    return full

window = create_fullscren()

def draw_game_screen(sprites: list = [], scale: float = 1.0):
    """
    Draws all sprites on a smaller surface and
    then resizes it to fit the screen
    """

    game_screen = pygame.Surface((1080, 720))
    for sprite in sprites:
        game_screen.blit(sprite, sprite.pos)
    game_screen = pygame.transform.scale(game_screen, (scale, scale)) 
    return game_screen



def update_screen(window: pygame.Surface, game_screen):
    window.blit(game_screen, (0,0), RESIZABLE)
