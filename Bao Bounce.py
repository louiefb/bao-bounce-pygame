#Louie Balderrama
#mlfbalderrama@gmail.com
#Created January 2019
#Free to use, to remix, to recycle with written permission

import os
import sys
import random
import pygame
import colorsys
import cv2
import numpy as np
from pygame.locals import *

os.environ["SDL_VIDEO_CENTERED"] = "True"

#Customizable Features
leftspawn = True #Boba allowed to come from left of screen
rightspawn = True #Boba allowed to come from right of screen
topspawn = True #Boba allowed to come from top of screen
spawnfrequency = 1000 #in milliseconds; easy: 1500 med: 1000 hard: 500
sensitivity = 15 #movement in pixels; 15 is default, min could be 10, max is 30
traction = 0.3 #higher traction for higher value; default is 0.3; 0 is possible but it is equal to no momentum, no wallbounce, perfect stickiness; max is maybe 2.0
gravity_flag = True #True is default
momentum_flag = True #True is default
wallbounce_flag = True #True for wall bounce; False disables momentum off wall
slippery_flag = False #False for sticky floor (realistic); True for slippery floor (not realistic)

def Hue_Shift(img, origin, axis):
    img = cv2.imread(img, -1)

    #RGB scale
    img_scaled = img[:,:,0:3]/255

    #convert to HSV
    hsv = []
    for i in img_scaled:
        row = []
        for j in i:
            row.append(colorsys.rgb_to_hsv(j[0],j[1],j[2]))
        hsv.append(row)
    hsv = np.array(hsv)

    #HSV scale
    hsv[:,:,0:1] *=255

    #Hue shift
    hsv[:,:,0:1] += (origin/axis)*255

    #HSV de-scale
    hsv[:,:,0:1] /=255

    #convert to RGB
    rgb = []
    for i in hsv:
        row = []
        for j in i:
            row.append(colorsys.hsv_to_rgb(j[0],j[1],j[2]))
        rgb.append(row)
    rgb = np.array(rgb)

    #RGB de-scale
    rgb = rgb*255

    #applying original alpha channel
    img = np.append(rgb, img[:,:,3:4], axis=2)

    return img

class Bao(pygame.sprite.Sprite):
    def __init__(self):
        super(Bao, self).__init__()
        self.surf = pygame.image.load("Bao.png")
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(x/2, y/2))
        self.delay = 0
        self.timekeep = 0

    def update(self, pressed_keys):
        global coeff
        global restitution
        global gravity
        global momentum
        global slippery
        global sensitivity
        global momentum_flag
        global slippery_flag
        global wallbounce_flag
        
        if gravity_flag == True:
            self.rect.move_ip(0, coeff)
        if momentum_flag == True:
            self.rect.move_ip(momentum, 0)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, sensitivity)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-sensitivity, 0)
            if momentum_flag == True:
                momentum -= traction*sensitivity
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(sensitivity, 0)
            if momentum_flag == True:
                momentum += traction*sensitivity
        if self.rect.left <= 0:
            self.rect.left = 0
            if wallbounce_flag == True:
                momentum = -momentum/2
            else:
                momentum = 0
        if self.rect.right >= x:
            self.rect.right = x
            if wallbounce_flag == True:
                momentum = -momentum/2
            else:
                momentum = 0
        if self.rect.top <= 0:
            self.rect.top = 0
            if gravity_flag == True:
                gravity *= 2
                self.timekeep = pygame.time.get_ticks()
                self.delay = 300
                slippery = True
        if self.rect.bottom >= y:
            if gravity_flag == True:
                self.rect.bottom = y-(restitution)
                restitution = restitution/2
                coeff = 1
                slippery = slippery_flag
            else:
                self.rect.bottom = y

    def jump(self, pressed_keys):
        global coeff
        global restitution
        global gravity
        now = pygame.time.get_ticks()
        if pressed_keys[K_UP]:
            if gravity_flag == True:
                if now - self.timekeep >= self.delay:
                    self.timekeep = 0
                    coeff = 5
                    self.rect.move_ip(0, -restitution)
                    gravity = 2
                    restitution = 6*sensitivity
            else:
                self.rect.move_ip(0, -sensitivity)

class NPC_Right(pygame.sprite.Sprite):
    def __init__(self):
        super(NPC_Right, self).__init__()
        self.origin = random.randint(0,y)
        self.img = Hue_Shift("Boba.png", self.origin, x)
        cv2.imwrite("Boba_Hue.png",self.img)
        self.surf = pygame.image.load("Boba_Hue.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(x, self.origin))
        self.x_speed = random.randint(1,10)
        self.y_speed = random.randint(-5,5)

    def update(self):
        self.rect.move_ip(-self.x_speed, self.y_speed)
        if self.rect.right <= 0:
            self.kill()

class NPC_Left(pygame.sprite.Sprite):
    def __init__(self):
        super(NPC_Left, self).__init__()
        self.origin = random.randint(0,y)
        self.img = Hue_Shift("Boba.png", self.origin, x)
        cv2.imwrite("Boba_Hue.png",self.img)
        self.surf = pygame.image.load("Boba_Hue.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(0, self.origin))
        self.x_speed = random.randint(1,10)
        self.y_speed = random.randint(-5,5)

    def update(self):
        self.rect.move_ip(self.x_speed, self.y_speed)
        if self.rect.left >= x:
            self.kill()

class NPC_Top(pygame.sprite.Sprite):
    def __init__(self):
        super(NPC_Top, self).__init__()
        self.origin = random.randint(0,x)
        self.img = Hue_Shift("Boba.png", self.origin, y)
        cv2.imwrite("Boba_Hue.png",self.img)
        self.surf = pygame.image.load("Boba_Hue.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(center=(self.origin, 0))
        self.x_speed = random.randint(-5,5)
        self.y_speed = random.randint(1,10)

    def update(self):
        self.rect.move_ip(self.x_speed, self.y_speed)
        if self.rect.top >= y:
            self.kill()

x = 800
y = 600

coeff = 1
gravity = 2
momentum = 0
restitution = 6*sensitivity
slippery = True

pygame.init()
pygame.display.set_caption("Bao Bounce")
screen = pygame.display.set_mode((x, y), pygame.HWSURFACE)
background = pygame.image.load("Background.jpg").convert()

bao = Bao()
sprites_bao = pygame.sprite.Group()
sprites_bao.add(bao)
sprites_npc = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(bao)
gameover_flag = False

ENABLEJUMP = pygame.USEREVENT + 1
pygame.time.set_timer(ENABLEJUMP, 50)

SPAWNLNPC = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNLNPC, spawnfrequency)

SPAWNRNPC = pygame.USEREVENT + 3
pygame.time.set_timer(SPAWNRNPC, spawnfrequency)

SPAWNTNPC = pygame.USEREVENT + 4
pygame.time.set_timer(SPAWNTNPC, spawnfrequency)

BLINK = pygame.USEREVENT + 5
pygame.time.set_timer(BLINK, 1300)

UNBLINK = pygame.USEREVENT + 6
pygame.time.set_timer(UNBLINK, 300)

run = True
while run:
    clock = pygame.time.Clock()
    clock.tick(60)
    if coeff != 100:
        coeff += gravity
    if slippery == False:
        if momentum > 0:
            momentum -= traction
        elif momentum < 0:
            momentum += traction
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif (event.type == ENABLEJUMP) and (gameover_flag == False):
            pressed_keys = pygame.key.get_pressed()
            bao.jump(pressed_keys)
        elif (event.type == SPAWNRNPC) and (rightspawn == True) and (gameover_flag == False):
            npc = NPC_Right()
            sprites_npc.add(npc)
            sprites.add(npc)
        elif (event.type == SPAWNLNPC) and (leftspawn == True) and (gameover_flag == False):
            npc = NPC_Left()
            sprites_npc.add(npc)
            sprites.add(npc)
        elif (event.type == SPAWNTNPC) and (topspawn == True) and (gameover_flag == False):
            npc = NPC_Top()
            sprites_npc.add(npc)
            sprites.add(npc)
        elif (event.type == BLINK) and (gameover_flag == False):
            bao.surf = pygame.image.load("Bao_Blink.png")
        elif (event.type == UNBLINK) and (gameover_flag == False):
            bao.surf = pygame.image.load("Bao.png")

    if gameover_flag == False:
        pressed_keys = pygame.key.get_pressed()
        if pygame.sprite.spritecollide(bao, sprites_npc, True, pygame.sprite.collide_mask):
            bao.surf = pygame.image.load("Bao_Hit.png")
            for i in sprites_npc:
                i.left_ = i.rect.left
                i.top_ = i.rect.top
            gameover_flag = True
    else:
        pressed_keys = [0 for i in range(len(pressed_keys))]
        if bao.rect.bottom >= y*.99:
            momentum = 0
        for i in sprites_npc:
            i.rect.left = i.left_
            i.rect.top = i.top_
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    bao.update(pressed_keys)
    sprites_npc.update()
    for i in sprites:
        screen.blit(i.surf, i.rect)
    pygame.display.flip()
