import pygame, random
from pygame.math import Vector2

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/ENTITIES.PY
"""

pygame.init()

def getimage(path):
    img = pygame.image.load("./resources/images/"+path)
    return img

#OBJECT DEFINITION STUFF
class Pebble(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([4, 4])
        self.image.fill([128, 128, 128])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
        self.moving = False #Temp, set to true when throwing
    def update(self):
        self.coords = self.rect.left, self.rect.top
        if not self.moving:
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
    def draw(self, surface):
        surface.blit(self.image, self.coords)
    def checkwall(self, walls):
        hits = [False, False, False, False]
        if pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_mask):
            for wall in pygame.sprite.spritecollide(self, walls, False, pygame.sprite.collide_mask):
                wall.kill()
                hitpos = pygame.sprite.collide_mask(self, wall)
                print(hitpos)
                if hitpos[0] == 0 and not hitpos[1] == 0 and not hitpos[1] == 40:
                    hits[0] = True
                elif hitpos[0] == 80 and not hitpos[1] == 0 and not hitpos[1] == 40:
                    hits[1] = True
                elif hitpos[0] == 0 and hitpos[1] == 0 or hitpos[1] == 40:
                    hits[0] = True

                    print(1)
                    if hitpos[1] == 0:
                        print(2)
                        hits[2] = True
                    elif hitpos[1] == 40:
                        hits[3] = True
                elif hitpos[0] == 80 and hitpos[1] == 0 or hitpos[1] == 40:
                    hits[1] = True
                    if hitpos[1] == 0:
                        hits[2] = True
                    elif hitpos[1] == 40:
                        hits[3] = True
                walls.add(wall)
        return hits
    def accelerate(self, ripple, walls):
        self.velocity = Vector2(self.rect.centerx - ripple.rect.centerx, self.rect.centery - ripple.rect.centery).normalize() * (0.2*ripple.intensity)
        self.rect.left, self.rect.top = self.coords
    def update(self, walls):
        self.coords += self.velocity
        if self.coords[0] < 0:
            self.coords[0] = 0
        if self.coords[0] > 720:
            self.coords[0] = 720
        if self.coords[1] < 0:
            self.coords[1] = 0
        if self.coords[1] > 760:
            self.coords[1] = 760
        self.rect.left, self.rect.top = self.coords
        self.velocity = self.velocity*(2/3)

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
