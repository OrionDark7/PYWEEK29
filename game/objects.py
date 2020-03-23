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
            boat.velocity -= oldvelocity*2


class Gate(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/gate.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            boat.reachedgate = True