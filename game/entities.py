import pygame, random, math
from pygame.math import Vector2

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/ENTITIES.PY
"""

pygame.init()

def distance(x1, x2, x3, x4):
    return math.sqrt(abs( ( (x2-x1)^2 ) + ( (x2-x1)^2 ) ))

def getimage(path):
    img = pygame.image.load("./resources/images/"+path)
    return img

#OBJECT DEFINITION STUFF
class Pebble(pygame.sprite.Sprite):
    def __init__(self, pos, goto):
        global window
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("objects/ripple.png")
        self.image.fill([128, 128, 128])
        self.image = pygame.transform.scale(self.image, [6, 6])
        self.originalimage = self.image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = Vector2(self.rect.left, self.rect.top)
        self.goto = list(goto)
        self.originaldist = distance(self.rect.centerx, self.goto[0], self.rect.centery, self.goto[1])
        self.speed = 22.5 + self.originaldist
        self.dist = self.originaldist
        self.velocity = Vector2(self.rect.centerx - self.goto[0], self.rect.centery - self.goto[1]).normalize() * -self.speed
        self.radius, self.angle = self.velocity.as_polar()
        self.image = pygame.transform.rotate(self.image, int(-self.angle))
    def update(self, boat):
        self.rect.left, self.rect.top = self.coords
        self.speed -= 0.5
        self.dist = distance(self.rect.centerx, self.goto[0], self.rect.centery, self.goto[1])
        try:
            self.velocity = Vector2(self.rect.centerx - self.goto[0], self.rect.centery - self.goto[1]).normalize() * -self.speed
        except:
            pass
        self.radius, self.angle = self.velocity.as_polar()
        self.image.blit(pygame.transform.rotate(self.originalimage, int(-self.angle)), [0, 0])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.coords
        self.coords += self.velocity
        if self.rect.centerx > self.goto[0] - 15 and self.rect.centerx < self.goto[0] + 15:
            if self.rect.centery > self.goto[1] - 15 and self.rect.centery < self.goto[1] + 15:
                self.rect.centerx, self.rect.centery = self.goto
                self.velocity = 0
                boat.startripples = True
                boat.startripplesat = self.rect.center
                self.kill()

class Boat(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/boat.png")
        self.originalimg = self.image
        self.image.fill([237, 244, 161])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = Vector2(0, 0)
        self.reachedgate = False
        self.health = 100
        self.collected = 0
        self.hitrock = False
        self.startripples = False
    def draw(self, surface):
        surface.blit(self.image, self.coords)
    def accelerate(self, ripple, walls):
        try:
            self.velocity = Vector2(self.rect.centerx - ripple.rect.centerx, self.rect.centery - ripple.rect.centery).normalize() * (0.4*ripple.intensity)
        except:
            pass
        ripple.effect = False
        self.rect.left, self.rect.top = self.coords
    def update(self, walls, startpos):
        self.coords += self.velocity

        if self.coords[0] < 0:
            self.coords[0] = 0
            if self.coords[0] < -80:
                self.coords = startpos
        if self.coords[0] > 720:
            self.coords[0] = 720
            if self.coords[0] > 800:
                self.coords = startpos
        if self.coords[1] < 0:
            self.coords[1] = 0
            if self.coords[0] < -40:
                self.coords = startpos
        if self.coords[1] > 560:
            self.coords[1] = 560
            if self.coords[0] > 600:
                self.coords = startpos
        self.rect.left, self.rect.top = self.coords
        self.velocity = self.velocity*(2/3)

        if pygame.sprite.spritecollide(self, walls, False) or self.health <= 0:
            self.coords = startpos[0] - 40, startpos[1] - 20
            self.health = 100

        if self.velocity[0] < 0.05 and self.velocity[0] > -0.05: #Yeah just not worth it at this point.
            self.velocity[0] = 0
        if self.velocity[1] < 0.05 and self.velocity[1] > -0.05: #Yeah just not worth it at this point.
            self.velocity[1] = 0


class Ripple(pygame.sprite.Sprite):
    def __init__(self, pos, speed, radspeed, centered=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = getimage("/objects/ripple.png")
        self.radius = 2
        self.radspeed = radspeed
        self.speed = float(speed)
        self.intensity = 1
        self.rect = self.image.get_rect()
        if centered:
            self.rect.centerx, self.rect.centery = list(pos)
        else:
            self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
        self.mask = pygame.mask.from_surface(self.image)
        self.hit = False
    def update(self, boat, ripples): #Handles growth and intensity change
        self.radius += self.radspeed
        oldcenter = [self.rect.centerx, self.rect.centery]
        self.image = getimage("/objects/ripple.png")
        self.image = pygame.transform.scale(self.image, [int(self.radius*2), int(self.radius*2)])
        try:
            pygame.draw.ellipse(self.image, [84-int(27*(1-self.intensity)), 171-int(52*(1-self.intensity)), 191-int(36*(1-self.intensity))], [0, 0, int(self.radius*2), int(self.radius*2)], int(self.intensity*8)+1)
        except:
            pygame.draw.ellipse(self.image, [84-int(27*(1-self.intensity)), 171-int(52*(1-self.intensity)), 191-int(36*(1-self.intensity))], [0, 0, int(self.radius * 2), int(self.radius * 2)],
                                1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        self.intensity -= self.speed
        if self.intensity <= 0:
            self.kill()
