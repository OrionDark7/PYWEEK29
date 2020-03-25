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
    def __init__(self, position, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 2:
            self.image = getimage("/objects/wall2.png")
        else:
            self.image = getimage("/objects/wall.png")
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
            if self.hit == False:
                oldvelocity = boat.velocity
                boat.velocity = Vector2(0,0)
                boat.velocity -= oldvelocity*4
                self.hit = True
            else:
                boat.velocity = Vector2(0, 0)
        else:
            self.hit = False


class Gate(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/gate.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            boat.reachedgate = True

class Drain(pygame.sprite.Sprite):
    def __init__(self, position, linkedto):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/drain.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.linkpos = None  # A gate you can't return through.
        if not linkedto == None:
            self.linkpos = list(linkedto)
            self.linkpos = [40*self.linkpos[0], 40*self.linkpos[1]]
    def update(self, boat):
        if self.rect.colliderect(boat.rect) and not self.linkpos == None:
            boat.coords = self.linkpos

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
            boat.velocity -= oldvelocity * 4
            if self.type == "rock" and self.hit:
                oldvelocity /= 4
                boat.velocity = -oldvelocity
            if self.type == "rock" and not self.hit:
                boat.health -= 5
                boat.hitrock = True
                self.hit = True
            if self.type == "lilly" or self.type == "coin":
                self.kill()
                if self.type == "coin":
                    boat.collected += 1
                elif self.type == "lilly":
                    boat.velocity = boat.velocity/2
        else:
            self.hit = False

class Shark(pygame.sprite.Sprite):
    def __init__(self, position, goto):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/shark.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.coords = self.rect.left, self.rect.top
        self.goto = self.coords  # A non moving shark?
        self.goto = list(goto)
        self.goto = [40 * self.goto[0], 40 * self.goto[1]]
        self.goingto = self.goto
        self.startpos = self.coords
    def update(self, boat):
        self.coords = self.rect.left, self.rect.top
        if self.rect.left < self.goingto[0]:
            self.rect.left += 1
        elif self.rect.left > self.goingto[0]:
            self.rect.left -= 1
        if self.rect.top < self.goingto[1]:
            self.rect.top += 1
        elif self.rect.top > self.goingto[1]:
            self.rect.top -= 1

        if [self.rect.left, self.rect.top] == self.goingto:
            if self.goingto == self.goto:
                self.goingto = self.startpos
            else:
                self.goingto = self.goto

        if self.rect.colliderect(boat.rect):
            boat.health = 0
