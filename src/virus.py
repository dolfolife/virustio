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

import pygame, sys, os, vector2d, math, character, random, defensin
import spritesheet
from pygame.locals import *

main_game = None
sndpath = os.path.join("data", "snd")

# Frames del virus.
virus_sprite = 120, 78
virus_frames = [spritesheet.Spritesheet("sprite_Virus.png").imgsat([(0, 0, virus_sprite[0], virus_sprite[1]),   
               (virus_sprite[0], 0, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 2, 0, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 3, 0, virus_sprite[0], virus_sprite[1])]),
               spritesheet.Spritesheet("sprite_Virus.png").imgsat([(0, virus_sprite[1], virus_sprite[0], virus_sprite[1]),   
               (virus_sprite[0], virus_sprite[1], virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 2, virus_sprite[1], virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 3, virus_sprite[1], virus_sprite[0], virus_sprite[1])]), 
               spritesheet.Spritesheet("sprite_Virus.png").imgsat([(0, virus_sprite[1] * 2, virus_sprite[0], virus_sprite[1]), 
               (virus_sprite[0], virus_sprite[1] * 2, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 2, virus_sprite[1] * 2, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 3, virus_sprite[1] * 2, virus_sprite[0], virus_sprite[1])]), 
               spritesheet.Spritesheet("sprite_Virus.png").imgsat([(0, virus_sprite[1] * 3, virus_sprite[0], virus_sprite[1]),   
               (virus_sprite[0], virus_sprite[1] * 3, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 2, virus_sprite[1] * 3, virus_sprite[0], virus_sprite[1]),
               (virus_sprite[0] * 3, virus_sprite[1] * 3, virus_sprite[0], virus_sprite[1])])]
virus_respawn_box = pygame.Rect(340, 600 - virus_sprite[1], virus_sprite[0], virus_sprite[1] - 3)

golpe_vir = pygame.mixer.Sound(os.path.join(sndpath,"virus_dead.wav"))
muerte = pygame.mixer.Sound(os.path.join(sndpath,"advertencia.wav"))
golpes = [pygame.mixer.Sound(os.path.join(sndpath,"d1.wav")),pygame.mixer.Sound(os.path.join(sndpath,"d2.wav")),pygame.mixer.Sound(os.path.join(sndpath,"d3.wav")),pygame.mixer.Sound(os.path.join(sndpath,"d4.wav")),pygame.mixer.Sound(os.path.join(sndpath,"d5.wav"))]

class VirusCharacter(character.Character):
    
    def __init__(self, screen, initial_pos, defs, cels, virus):
        character.Character.__init__(self, screen, initial_pos, defs, cels, virus)
        self.sprite = virus_sprite
        self.no_frames = 4
        self.frames = virus_frames
        self.frame = [0, 0]
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
        self.rect = pygame.Rect(self.pos[0] + 3, self.pos[1] + 3, self.sprite[0] - 3, self.sprite[1] - 3)
        self.lives = 3
        self.alive = True
        self.revival_time = 0
        self.killed = 0
        self.rand = 0
        
    def response(self):
        pygame.event.pump()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.accel.x = -self.start
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.accel.x = self.start
        else:
            if (math.floor(self.speed.x) != 0):
                self.accel.x = (-self.speed.x / abs(self.speed.x)) * self.brake
            else:
                self.accel.x = 0
                self.speed.x = 0
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.accel.y = -self.start
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.accel.y = self.start
        else:
            if (math.floor(self.speed.y) != 0):
                self.accel.y = (-self.speed.y / abs(self.speed.y)) * self.brake
            else:
                self.accel.y = 0
                self.speed.y = 0
    
    def update(self, spawn):
        if not self.alive:
            self.respawn()
            return True
        else:
            self.speed.x = max(-self.max_sp, min(self.speed.x + self.accel.x, self.max_sp))
            self.speed.y = max(-self.max_sp, min(self.speed.y + self.accel.y, self.max_sp))
            self.pos = max(0, min(self.pos[0] + self.speed.x, self.screen[0] - self.sprite[0])), max(0, min(self.pos[1] + self.speed.y, self.screen[1] - self.sprite[1]))
            if (self.pos[0] == self.screen[0] - self.sprite[0] or self.pos[0] == 0):
                self.speed.x = 0
            if (self.pos[1] == self.screen[1] - self.sprite[1] or self.pos[1] == 0):
                self.speed.y = 0
            self.rect.topleft = (self.pos[0] + 3, self.pos[1] + 3)
            will_die = map(self.in_def_radius, self.defensins)
            if any(will_die):
                k = random.randint(0,4)
                golpes[k].play()
                self.lives = self.lives - 1
                if (self.lives == 0):
                    return False
                else:
                    self.revival_time = 120
                    self.alive = False
                    self.rect = None
            else:
                to_die = map(self.in_cell_radius, self.celulosos)
                if any(to_die):
                    golpe_vir.play()
                    muerte.play()
                j = 0
                while (j < len(self.celulosos)):
                    if to_die[j]:
                        to_die.pop(j)
                        self.celulosos.pop(j)
                        if self.rect.center[0] < 400:
                            self.bring_defensin(1, spawn)
                        else:
                            self.bring_defensin(0, spawn)
                        k = 0
                        self.killed = self.killed + 1
                        while (k < len(self.celulosos)):
                            self.celulosos[k].wow()
                            k = k + 1
                    else:
                        j = j + 1
            return True
    
    def tick(self):
        self.no_frames = 4
        if (self.speed.x == 0 and self.speed.y == 0):
            self.frame[0] = 0
            self.frame[1] = (self.frame[1] + 1) % self.no_frames
        elif (self.speed.y != 0):
          if (self.speed.y > 0):
              self.frame[0] = 1
              self.frame[1] = 2
          else:
              self.frame[0] = 1
              self.frame[1] = 1
        else:
          if (self.speed.x > 0):
              self.frame[0] = 2
              self.frame[1] = (self.frame[1] + 1) % self.no_frames
          else:
              self.frame[0] = 3
              self.frame[1] = (self.frame[1] + 1) % self.no_frames
        self.actual_frame = self.frames[self.frame[0]][self.frame[1]]

    def in_def_radius(self, character):
        radius = 25
        return math.sqrt((self.rect.center[0] - character.rect.center[0])**2 + (self.rect.center[1] - character.rect.center[1])**2) <= radius
    
    def in_cell_radius(self, character):
        radius = 35
        return math.sqrt((self.rect.center[0] - character.rect.center[0])**2 + (self.rect.center[1] - character.rect.center[1])**2) <= radius
    
    def respawn(self):
        if self.revival_time > 0:
            self.revival_time = self.revival_time - 1
        else:
            would_kill_me = map(respawn_invaded, self.defensins)
            if not any(would_kill_me):
                self.pos = [340, 600 - self.sprite[1]]
                self.frame = [0, 0]
                self.actual_frame = self.frames[self.frame[0]][self.frame[1]]
                self.rect = pygame.Rect(self.pos[0] + 3, self.pos[1] + 3, self.sprite[0] - 3, self.sprite[1] - 3)
                self.alive = True

    def bring_defensin(self, side, spawn):
        self.rand = (self.rand + 1) % 5
        self.defensins.append(defensin.DefensinCharacter([800, 600], [spawn[side][self.rand].topleft[0], spawn[side][self.rand].topleft[1]], self.defensins, self.celulosos, self))

def respawn_invaded(character):
    global virus_respawn_box
    return virus_respawn_box.colliderect(character.rect)