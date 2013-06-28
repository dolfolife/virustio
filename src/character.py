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

import pygame, sys, os, vector2d, math
from pygame.locals import *

class Character:
    
    def __init__(self, screen, initial_pos, defs, cels, virus):
        self.sprite = 36, 35
        self.frames = [0, 0]
        self.start = 0.125
        self.brake = 0.075
        self.max_sp = 5
        self.screen = screen
        self.accel = vector2d.Vector(0, 0)
        self.speed = vector2d.Vector(0, 0)
        self.pos = initial_pos
        self.frame = [0, 0]
        self.no_frames = 3
        self.rect = None
        self.defensins = defs
        self.celulosos = cels
        self.virus = virus
        self.frame_wait = 0

    def tick(self):
        if (self.speed.x == 0):
            self.frame = self.frame[0], (self.frame[1] + 1) % self.no_frames
        elif (self.speed.x > 0):
            self.frame = 0, (self.frame[1] + 1) % self.no_frames
        elif (self.speed.x < 0):
            self.frame = 1, (self.frame[1] + 1) % self.no_frames
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
    
    def detect_collision(self, character):
        return self.rect.colliderect(character.rect)

    def eq(self, char):
        return self == char
    
    def change_direction(self):
        self.speed.x = -self.speed.x
        self.speed.y = -self.speed.y