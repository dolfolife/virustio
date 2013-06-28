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

import pygame, sys, os, time, random

imgpath = os.path.join("data", "img")
sndpath = os.path.join("data", "snd")
fontpath = os.path.join("data", "fonts")

pygame.init()
bgimg = pygame.image.load(os.path.join(imgpath,"backgr.png"))
size = bgimg.get_size()
window = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.HWSURFACE)
screen = pygame.display.get_surface()

import virus, defensin, celuloso, time, spritesheet
from pygame.locals import *

portada = pygame.image.load(os.path.join(imgpath,"Portada.png"))
youare = pygame.image.load(os.path.join(imgpath,"youare.png"))
thevirus = pygame.image.load(os.path.join(imgpath,"thevirus.png"))
yougotta = pygame.image.load(os.path.join(imgpath,"yougotta.png"))
killthem = pygame.image.load(os.path.join(imgpath,"killthem.png"))
ande = pygame.image.load(os.path.join(imgpath,"and.png"))
run = pygame.image.load(os.path.join(imgpath,"run.png"))
areyouready = pygame.image.load(os.path.join(imgpath, "areyouready.png"))

youwin = pygame.image.load(os.path.join(imgpath, "youwin.png"))
youlost = pygame.image.load(os.path.join(imgpath, "youlost.png"))

font1 = pygame.font.Font(os.path.join(fontpath, "AlphaMaleModern.ttf"), 20)
font2 = pygame.font.Font(os.path.join(fontpath, "AlphaMaleModern.ttf"), 25)

pygame.mixer.music.load(os.path.join(sndpath,"fondo_musica.wav"))

class Virustio:

    def __init__(self):
        global bgimg, size, window, screen
        pygame.display.set_caption("Virustio")
        self.bgimg = bgimg
        self.size = size
        self.window = window
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.count = 0
        self.game_over = 0
        self.food = []
        self.enemies = []
        self.time_control = 0
        self.timer = [5, 00]
        self.pc = virus.VirusCharacter(self.size, [350, 522], self.enemies, self.food, None)
        self.food_spawn = [pygame.Rect(150, 150, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(300, 300, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(450, 450, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(600, 180, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(200, 310, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(350, 440, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(500, 450, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(650, 320, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(175, 190, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(325, 180, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(475, 330, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1]),
                           pygame.Rect(620, 420, celuloso.celuloso_sprite[0], celuloso.celuloso_sprite[1])]
        self.enemy_spawn = [[pygame.Rect(0, 80, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(0, 200, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(0, 320, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(0, 440, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(0, 560, defensin.defensin_sprite[0], defensin.defensin_sprite[1])],
                            [pygame.Rect(764, 80, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(764, 200, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(764, 320, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(764, 440, defensin.defensin_sprite[0], defensin.defensin_sprite[1]),
                             pygame.Rect(764, 560, defensin.defensin_sprite[0], defensin.defensin_sprite[1])]]
        self.fill_food(3)
        self.cell_timer = 0
    
    def start(self):
        global portada, youare, thevirus, yougotta, killthem, ande, run, youwin, youlost

        virus.main_game = self

        self.screen.blit(portada, (0,0))
        pygame.display.flip()
        time.sleep(4)

        map(self.print_screen, [youare, thevirus, yougotta, killthem, ande, run])

        self.screen.blit(areyouready, (0,0))
        pygame.display.flip()

        time.sleep(2)
        pygame.mixer.music.play(0,0.0)
        time.sleep(2)

        while not self.game_over and not (self.timer[0] == 0 and self.timer[1] == 0):
            self.clock.tick(60)
            self.pc.response()
            self.count = (self.count + 1) % 10
            self.game_over = not self.pc.update(self.enemy_spawn)
            self.update(self.enemies)
            self.update(self.food)
            if self.count == 0:
                self.pc.tick()
                map(self.tick, self.enemies)
                map(self.tick, self.food)
                self.time_control = (self.time_control + 1) % 6
                if self.time_control == 0:
                    self.decrease_timer()
                    self.cell_timer = (self.cell_timer + 1) % 5
                    if self.cell_timer == 0:
                        self.fill_food(5)
            self.screen.blit(self.bgimg, (0,0))
            if self.pc.alive:
                self.draw(self.pc)
            map(self.draw, self.enemies)
            map(self.draw, self.food)
            self.print_life(self.pc.lives)
            self.print_score(self.pc.killed)
            if self.timer[1] >= 0 and self.timer[1] <= 9:
                self.print_time(str(self.timer[0]) + ':0' + str(self.timer[1]))
            else:
                self.print_time(str(self.timer[0]) + ':' + str(self.timer[1]))
            pygame.display.flip()
        if self.game_over:
            pygame.mixer.music.load(os.path.join(sndpath,"u_lose.wav"))
            pygame.mixer.music.play(0,0.0)
            time.sleep(2)
            self.screen.blit(youlost, (0,0))
            pygame.display.flip()
            time.sleep(4)
        else:
            pygame.mixer.music.load(os.path.join(sndpath,"u_win.wav"))
            pygame.mixer.music.play(0,0.0)
            time.sleep(2)
            self.screen.blit(youwin, (0,0))
            pygame.display.flip()
            time.sleep(4)

    def fill_food(self, howmuch):
        retries = 0
        filled = 0
        while len(self.food) < len(self.food_spawn) and retries < 6 and filled < howmuch:
            rand = random.randint(0, len(self.food_spawn) - 1)
            if not self.pc.alive or not self.food_spawn[rand].colliderect(self.pc.rect):
                i = 0
                while i < len(self.food) and not self.food_spawn[rand].colliderect(self.food[i].rect):
                    i = i + 1
                if i < len(self.food):
                    retries = retries + 1
                else:
                    self.summon(True, rand)
                    filled = filled + 1

    def summon(self, type, x, y = 0):
        if type:
            self.food.append(celuloso.CelulosoCharacter(self.size, [self.food_spawn[x].topleft[0], self.food_spawn[x].topleft[1]], self.enemies, self.food, self.pc))
        else:
            self.enemies.append(defensin.DefensinCharacter(self.size, [self.enemy_spawn[x][y].topleft[0], self.enemy_spawn[x][y].topleft[1]], self.enemies, self.food, self.pc))
    
    def draw(self, character):
        self.screen.blit(character.actual_frame, character.pos)

    def tick(self, character):
        character.tick()
        
    def update(self, charlist):
        i = 0
        while i < len(charlist):
            charlist[i].update(i)
            i = i + 1

    def decrease_timer(self):
        if self.timer[1] == 0:
            self.timer[0] = self.timer[0] - 1
            self.timer[1] = 60
            defensin.level = defensin.level + 1
        self.timer[1] = self.timer[1] - 1
        
    def print_screen(self, image):
        self.screen.blit(image, (0,0))
        pygame.display.flip()
        time.sleep(2)

    def print_time (self, time):
        text = font2.render(time, True, (255,255,255))
        self.screen.blit(text, (360,5))
      

    def print_life (self, life):
        text = font1.render(str(life), True, (255,255,255))
        image = pygame.transform.scale(virus.virus_frames[0][0], (40,25))
        self.screen.blit(image, (1,1))
        self.screen.blit(text, (43,1))
      
      
    def print_score (self, score):      
        #text = font1.render('Score: ' + str(score), True, (255,255, 255))
        #screen.blit(text, (680,5))
         
        text = font1.render(str(score), True, (255,255,255))
        image = pygame.transform.scale(celuloso.celuloso_frames[0][2], (22,22))
        self.screen.blit(text, (745,5))
        self.screen.blit(image, (715,1))

pygame.init()
Virustio().start()