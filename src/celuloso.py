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

import pygame, sys, os, vector2d, math, character, random
import spritesheet
from pygame.locals import *

# Frames del celuloso
sndpath = os.path.join("data", "snd")

celuloso_sprite = 55, 52
celuloso_frames = [spritesheet.Spritesheet("celuloso.png").imgsat([(0, 0, celuloso_sprite[0], celuloso_sprite[1]),   
                   (celuloso_sprite[0], 0, celuloso_sprite[0], celuloso_sprite[1]),
                   (celuloso_sprite[0] * 2, 0, celuloso_sprite[0], celuloso_sprite[1])])]
scared_sound = pygame.mixer.Sound(os.path.join(sndpath,"juan.wav"))

class CelulosoCharacter(character.Character):
    
    def __init__(self, screen, initial_pos, defs, cels, virus):
        character.Character.__init__(self, screen, initial_pos, defs, cels, virus)
        self.sprite = celuloso_sprite
        self.frames = celuloso_frames
        self.frame = [0, 0]
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
        self.rect = pygame.Rect(self.pos[0] + 3, self.pos[1] + 3, self.sprite[0] - 3, self.sprite[1] - 3)
        self.frame_count = 0
        self.max_sp = 0.25
        self.angle = random.uniform(-2*math.pi, 2*math.pi)
        self.speed = vector2d.Vector(math.sin(self.angle), math.cos(self.angle)) * self.max_sp
        self.awareness = pygame.Rect(self.pos[0] - 100, self.pos[1] - 100, self.sprite[0] + 200, self.sprite[1] + 200)
        self.rotation = 0
        self.tick_wow = 0
        self.scared = False
        
    def tick(self):
        self.frame_count = (self.frame_count + 1) % 6
        if self.frame_count == 0:
            self.angle = self.angle + ((math.pi / 5) * binomial())
            self.speed.x = math.sin(self.angle)
            self.speed.y = math.cos(self.angle)
            self.speed = self.speed * self.max_sp
        if self.virus.alive and self.awareness.colliderect(self.virus.rect):
            if not self.scared:
                scared_sound.play()
                self.scared = True
            if self.tick_wow == 0:
                self.frame = 0, 1
            self.max_sp = 1
            self.trigger_flee()
        else:
            if self.tick_wow == 0:
                self.frame = 0, 0
            self.max_sp = 0.25
            self.scared = False
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
        self.rotation = self.rotation + 5
        self.actual_frame = pygame.transform.rotate(self.actual_frame, self.rotation)
        self.tick_wow = max(0, self.tick_wow - 1)

    def update(self, i):
        if (self.pos[0] == self.screen[0] - self.sprite[0] or self.pos[0] == 0):
            self.angle = self.angle + math.pi
            self.speed.x = math.sin(self.angle)
            self.speed.y = math.cos(self.angle)
            self.speed = self.speed * self.max_sp
        elif (self.pos[1] == self.screen[1] - self.sprite[1] or self.pos[1] == 0):
            self.angle = self.angle - math.pi
            self.speed.x = math.sin(self.angle)
            self.speed.y = math.cos(self.angle)
            self.speed = self.speed * self.max_sp
        else:
            j = 0
            while (j < len(self.celulosos)):
                if (j != i and self.detect_collision(self.celulosos[j])):
                    self.angle = self.angle + math.pi
                    self.speed.x = math.sin(self.angle)
                    self.speed.y = math.cos(self.angle)
                    self.speed = self.speed * self.max_sp
                j = j + 1 
        self.pos = max(0, min(self.pos[0] + self.speed.x, self.screen[0] - self.sprite[0])), max(0, min(self.pos[1] + self.speed.y, self.screen[1] - self.sprite[1]))
        self.rect.topleft = (self.pos[0] + 3, self.pos[1] + 3)
        self.awareness.topleft = (self.pos[0] - 100, self.pos[1] - 100)

    def trigger_flee(self):
        direction = vector2d.Vector(self.pos[0] - self.virus.pos[0], self.pos[1] - self.virus.pos[1])
        self.speed = vector2d.Normalize(direction) * self.max_sp

    def wow(self):
        self.frame = 0, 2
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
        self.tick_wow = 6
        self.actual_frame = pygame.transform.rotate(self.actual_frame, self.rotation)
    
def binomial():
    return random.random() - random.random()