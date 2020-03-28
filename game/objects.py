import pygame
from pygame.math import Vector2

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/OBJECTS.PY
"""

pygame.init()
pygame.mixer.init()

def getimage(path):
    img = pygame.image.load("./resources/images/"+path)
    return img

def getsfx(path):
    sfx = pygame.mixer.Sound("./resources/sfx/"+path)
    return sfx

class Wall(pygame.sprite.Sprite):
    def __init__(self, position, type):
        pygame.sprite.Sprite.__init__(self)
        if type == 2:
            self.image = getimage("/objects/wall2.png")
        elif type == 3:
            self.image = getimage("/objects/wall3.png")
        elif type == 4:
            self.image = getimage("/objects/wall4.png")
        elif type == 5:
            self.image = getimage("/objects/wall5.png")
        else:
            self.image = getimage("/objects/wall.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.mask = pygame.mask.from_surface(self.image)
        self.hit = False
    def update(self, boat):
        if pygame.sprite.collide_mask(self, boat):
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
                boat.sfx.play()
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
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, boat):
        if pygame.sprite.collide_mask(self, boat):
            boat.reachedgate = True

class Drain(pygame.sprite.Sprite):
    def __init__(self, position, linkedto, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/drain"+direction+".png")
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
        self.sfx = None
        if type == "coin":
            self.sfx = getsfx("coin.ogg")
        elif type == "ice":
            self.sfx = getsfx("ice.ogg")
        self.type = str(type)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(position)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        self.hit = False
    def update(self, boat):
        if self.rect.colliderect(boat.rect) and not self.type == "grass":
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
                boat.health -= 100
                self.hit = True
                boat.sfx.play()
            if self.type == "lilly" or self.type == "coin" or self.type == "ice":
                self.kill()
                if self.type == "coin":
                    boat.collected += 1
                    self.sfx.play()
                elif self.type == "lilly":
                    boat.velocity = boat.velocity/2
                    boat.health -= 5
                elif self.type == "ice":
                    boat.velocity = boat.velocity/2
                    boat.health -= 15
                    self.sfx.play()
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

class Waterfall(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.velocitychange = 0
        if direction == "up":
            self.velocitychange = Vector2(0, -0.4)
        elif direction == "down":
            self.velocitychange = Vector2(0, 0.4)
        elif direction == "left":
            self.velocitychange = Vector2(-0.4, 0)
        elif direction == "right":
            self.velocitychange = Vector2(0.4, 0)
        self.direction = direction
        self.image = getimage("/objects/waterfall-"+str(direction)+".png")
        self.rect = self.image.get_rect()
        self.coords = Vector2(position[0], position[1])
        self.rect.left, self.rect.top = self.coords
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, boat):
        if self.rect.colliderect(boat.rect):
            if self.direction == "up":
                self.velocitychange += Vector2(0, -0.01)
            elif self.direction == "down":
                self.velocitychange += Vector2(0, 0.01)
            elif self.direction == "left":
                self.velocitychange += Vector2(-0.01, 0)
            elif self.direction == "right":
                self.velocitychange += Vector2(0.01, 0)
            boat.velocity += self.velocitychange
