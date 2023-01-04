import os
import sys
import pygame
from pygame import *
from player import *
from blocks import *


pygame.init()
size = width, height = 900, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ESCAPE из гауптвахты")
clock = pygame.time.Clock()
fps = 60
g = 10

def load_image(name, colorkey=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print("файл не существует")
        sys.exit()
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_map(name):
    fullname = os.path.join("maps", name)
    if not os.path.isfile(fullname):
        print("файл не существует")
        sys.exit()
    else:
        maps = open(fullname)
    return maps

class graund(pygame.sprite.Sprite):
    image = load_image("dirt.png", colorkey=-1)
    def __init__(self, *group):
        super().__init__(*group)
        self.image = graund.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 550

'''
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + width / 2, -t + width / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - width), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - height), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)
''' # огрызок с кодом от камеры

class Elephant(pygame.sprite.Sprite):
    image = load_image("elephant.png", colorkey=-1)
    image1 = load_image("elephant1.png", colorkey=-1)
    image2 = load_image("elephant2.png", colorkey=-1)
    uskor_x = 0
    uskor_y = 0
    fall = False
    right = False
    up = False
    left = False
    right = False
    down = False
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Elephant.image
        self.rect = self.image.get_rect()
        self.image = graund.image
        self.rect.x = 100
        self.rect.y = 550
        self.moving = False


    def update(self, tot_time):
        self.rect = self.rect.move(self.uskor_x // 100, self.uskor_y // 100)
        if self.rect.y > 900:
            self.rect.y = 0
        if self.fall:
            self.uskor_y = self.uskor_y + g
            if self.uskor_x > 0:
                self.uskor_x -= 1
            elif self.uskor_x < 0:
                self.uskor_x += 1
        if self.uskor_y > 500:
            self.uskor_y = 500
        #print(self.uskor_y)
        if self.moving:
            if self.right:
                if 0 <= tot_time <= 500:
                    self.image = Elephant.image
                else:
                    self.image = Elephant.image1
            else:
                if 0 <= tot_time <= 500:
                    self.image = pygame.transform.flip(Elephant.image, True, False)
                else:
                    self.image = pygame.transform.flip(Elephant.image1, True, False)
        else:
            self.image = Elephant.image2

        #if self.rect.colliderect(self.earth):
        #    self.fall = False

        if max(list(pygame.key.get_pressed())):
            if self.up and not self.fall:
                self.uskor_y = -500
                self.fall = True
                self.moving = True

                #self.rect = self.rect.move(self.uskor_x, self.uskor_y // 10)

            elif self.down:
                self.uskor_y = 0
                self.fall = False
                self.moving = True

                #self.rect = self.rect.move(self.uskor_x, self.uskor_y // 10)

            else:
                self.moving = False
            if self.right:
                self.right = True
                self.uskor_x = 300
                self.moving = True

                #self.rect = self.rect.move(self.uskor_x, self.uskor_y // 10)

            elif self.left:
                self.right = False
                self.uskor_x = -300
                self.moving = True

                #self.rect = self.rect.move(self.uskor_x, self.uskor_y // 10)

            else:
                self.uskor_x = 0
        else:
            self.uskor_x = self.uskor_x * self.fall
            self.moving = False


all_sprites = pygame.sprite.Group()
earth = pygame.sprite.Group()
a = graund(earth)
running = True
pleer = Elephant(all_sprites)
pleer.earth = earth
total_time = 0
#bg = pygame.transform.scale(load_image('background.png'), (1700, 800))
#screen.blit(bg, (0, 0))
#camera = Camera(camera_configure, 10, 10)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pleer.up = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            pleer.left = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            pleer.right = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            pleer.down = True

        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            pleer.up = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            pleer.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            pleer.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            pleer.down = False

    screen.fill(pygame.Color("white"))
    #screen.blit(bg, (0, 0))
    total_time += clock.get_time()
    if total_time >= 1000:
        total_time = 0
    clock.tick(fps)
    all_sprites.update(total_time)
    earth.draw(screen)
    #camera.update(pleer)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
