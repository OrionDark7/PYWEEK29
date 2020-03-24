import pygame
from pygame.math import Vector2

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/OBJECTS.PY
"""

pygame.init()

def getimage(path):
    img = pygame.image.load("./resources/images/"+path)
    return img

class Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/wall.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            if boat.velocity[0] < 0:
                boat.rect.left = self.rect.right
            elif boat.velocity[0] > 0:
                boat.rect.right = self.rect.left
            if boat.velocity[1] < 0:
                boat.rect.top = self.rect.bottom
            elif boat.velocity[1] > 0:
                boat.rect.bottom = self.rect.top
            oldvelocity = boat.velocity
            boat.velocity = Vector2(0,0)
            boat.velocity -= oldvelocity*4


class Gate(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/gate.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            boat.reachedgate = True

class Floaty(pygame.sprite.Sprite):
    def __init__(self, position, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/"+str(type)+".png")
        self.type = str(type)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        self.hit = False
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            if boat.velocity[0] < 0:
                boat.rect.left = self.rect.right
            elif boat.velocity[0] > 0:
                boat.rect.right = self.rect.left
            if boat.velocity[1] < 0:
                boat.rect.top = self.rect.bottom
            elif boat.velocity[1] > 0:
                boat.rect.bottom = self.rect.top
            oldvelocity = boat.velocity
            boat.velocity = Vector2(0, 0)
            boat.velocity -= oldvelocity * 2
            if self.type == "rock" and not self.hit:
                boat.health -= 10
                self.hit = True
            if self.type == "lilly" or self.type == "coin":
                self.kill()
                if self.type == "coin":
                    boat.collected += 1
                elif self.type == "lilly":
                    boat.velocity = boat.velocity/2
        else:
            self.hit = False