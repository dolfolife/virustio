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

level = -1
defensin_sprite = 36, 35
defensin_frames = [spritesheet.Spritesheet("plaqueta.png").imgsat([(0, defensin_sprite[1], defensin_sprite[0], defensin_sprite[1]),   
                           (defensin_sprite[0], defensin_sprite[1], defensin_sprite[0], defensin_sprite[1]),
                           (defensin_sprite[0] * 2, defensin_sprite[1], defensin_sprite[0], defensin_sprite[1])]),
                   spritesheet.Spritesheet("plaqueta.png").imgsat([(0, 0, defensin_sprite[0], defensin_sprite[1]),   
                           (defensin_sprite[0], 0, defensin_sprite[0], defensin_sprite[1]),
                           (defensin_sprite[0] * 2, 0, defensin_sprite[0], defensin_sprite[1])])]

class DefensinCharacter(character.Character):
    
    def __init__(self, screen, initial_pos, defs, cels, virus):
        character.Character.__init__(self, screen, initial_pos, defs, cels, virus)
        self.sprite = 36, 35
        self.frames[1] = spritesheet.Spritesheet("plaqueta.png").imgsat([(0, 0, self.sprite[0], self.sprite[1]),   
                           (self.sprite[0], 0, self.sprite[0], self.sprite[1]),
                           (self.sprite[0] * 2, 0, self.sprite[0], self.sprite[1])]) 
        self.frames[0] = spritesheet.Spritesheet("plaqueta.png").imgsat([(0, self.sprite[1], self.sprite[0], self.sprite[1]),   
                           (self.sprite[0], self.sprite[1], self.sprite[0], self.sprite[1]),
                           (self.sprite[0] * 2, self.sprite[1], self.sprite[0], self.sprite[1])])
        self.frame = [0, random.randint(0, self.no_frames - 1)]
        self.accel = [0.125, 0.125]      
        self.speed = vector2d.Vector(random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0))
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
        self.rect = pygame.Rect(self.pos[0] + 3, self.pos[1] + 3, self.sprite[0] - 3, self.sprite[1] - 3)
        # Pursue variables
        self.maxPrediction = 0.1
        self.targetRadius = 20
        self.slowRadius = 5
        self.timeToTarget = 0.1
        self.maxAccel = 0.1

    def update(self, i):
        global level
        if level <= 1 or level >= 5:
            self.update_linear(i)
        elif level == 2:
            self.update_seek(i)
        elif level == 3 or level == 4:
            self.update_pursue(i)
        self.pos = max(0, min(self.pos[0] + self.speed.x, self.screen[0] - self.sprite[0])), max(0, min(self.pos[1] + self.speed.y, self.screen[1] - self.sprite[1]))
        self.rect.topleft = (self.pos[0], self.pos[1])

    def update_linear(self, i):
        global level
        j = 0
        #~ while (j < len(self.defensins)):
            #~ if (j != i and self.detect_collision(self.defensins[j])):
                #~ self.change_direction()
                #~ break
            #~ j = j + 1
        #~ j = 0
        while (j < len(self.celulosos)):
            if (self.detect_collision(self.celulosos[j])):
                self.change_direction()
                self.speed.x = random.uniform(-2.0, 2.0)
                self.speed.y = random.uniform(-2.0, 2.0)
            j = j + 1
        if (self.pos[0] == self.screen[0] - self.sprite[0] or self.pos[0] == 0):
            self.speed.x = -self.speed.x
            self.speed.y = random.uniform(-2.0, 2.0)
        if (self.pos[1] == self.screen[1] - self.sprite[1] or self.pos[1] == 0):
            self.speed.y = -self.speed.y
            self.speed.x = random.uniform(-2.0, 2.0)
        if level == 5 and self.virus.alive:
            level = 4

    def update_seek(self, i):
        self.max_sp = 2
        if self.virus.alive:
            direction = vector2d.Vector(self.virus.rect.center[0] - self.pos[0], self.virus.rect.center[1] - self.pos[1])
            self.speed = vector2d.Normalize(direction) * self.max_sp
        else:
            self.update_linear(i)

    def update_pursue(self, i):
        global level
        self.max_sp = 2.5
        if self.virus.alive:
            direction = vector2d.Vector(self.virus.pos[0]+(self.virus.sprite[0]/2)-self.pos[0],self.virus.pos[1]+(self.virus.sprite[1]/2)-self.pos[1])
            distance = vector2d.Length(direction)
            speed = vector2d.Length(self.speed)
            if (speed<=distance/self.maxPrediction):
                prediction = self.maxPrediction
            else:
                prediction=distance/speed
            futurePos = vector2d.Vector(self.virus.pos[0]+(self.virus.sprite[0]/2)+self.virus.speed[0]*prediction,self.virus.pos[1]+(self.virus.sprite[1]/2)+self.virus.speed[1]*prediction)
            self.arrive(futurePos)
            self.speed.x = max(-self.max_sp, min(self.speed.x + self.accel.x, self.max_sp))
            self.speed.y = max(-self.max_sp, min(self.speed.y + self.accel.y, self.max_sp))
        else:
            level = 5
            self.update_linear(i)

    def arrive(self,futurePos):
        direction = futurePos - vector2d.Vector(self.pos[0],self.pos[1])
        distance = vector2d.Length(direction)
        if (distance<self.targetRadius):
            return None
        if (distance>self.slowRadius):
            targetSpeed = self.max_sp
        else:
            targetSpeed = self.max_sp * distance / self.slowRadius
        targetVelocity = direction
        targetVelocity = vector2d.Normalize(targetVelocity)
        targetVelocity *= targetSpeed
        self.accel = targetVelocity - self.speed
        self.accel /= self.timeToTarget
        if (vector2d.Length(self.accel)>self.maxAccel):
            self.accel = vector2d.Normalize(self.accel)
            self.accel *= self.maxAccel
        return None
        
def binomial():
    return random.random() - random.random()