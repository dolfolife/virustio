# 
# The Virus!!!!!!
#
# Developed by Hefesto Games:
#  - Juan Enrique Cifuentes
#  - Leonardo Da Costa
#  - Rodolfo Sánchez
#  - Carlos Alberto Pérez
#
# Address: hefesto.games@gmail.com
# 
# This game is subject to the Creative Commons Attribution-Noncommercial-No Derivative Works 3.0 Unported
# (http://creativecommons.org/licenses/by-nc-nd/3.0/)
#

import pygame, sys, os
from pygame.locals import *

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(os.path.join(os.path.join("data", "img"), filename))  
        
    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pygame.Surface(rect.size, SRCALPHA, 32)
        image = image.convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image
        
    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs