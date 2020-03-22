import pygame

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
        self.image.fill([237, 244, 161])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
        self.mask = pygame.mask.from_surface(self.image)
        self.xvelocity = 0
        self.yvelocity = 0
        self.rotation = 0
    def draw(self, surface):
        surface.blit(self.image, self.coords)
    def accelerate(self, ripple):
        collision = self.mask.overlap(ripple.mask, [0,0])
        print("COLLISION" + str(collision))
        print("EDGES" + str([self.rect.left, self.rect.right, self.rect.top, self.rect.bottom]))
        if collision[0] < self.rect.centerx:
            self.xvelocity += ripple.intensity
        elif collision[0] > self.rect.centerx:
            self.xvelocity -= ripple.intensity
        if collision[1] < self.rect.centery:
            self.yvelocity += ripple.intensity
        elif collision[1] > self.rect.centery:
            self.yvelocity -= ripple.intensity
        self.rect.left += self.xvelocity
        self.rect.top += self.yvelocity
    def update(self):
        self.coords = self.rect.left, self.rect.top
        if self.xvelocity < 0:
            self.xvelocity += 1
        elif self.xvelocity > 0:
            self.xvelocity -= 1
        if self.yvelocity < 0:
            self.yvelocity += 1
        elif self.yvelocity > 0:
            self.yvelocity -= 1

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
    def update(self, boat, ripples): #Handles growth and intensity change
        self.radius += self.radspeed
        oldcenter = [self.rect.centerx, self.rect.centery]
        self.image = getimage("/objects/ripple.png")
        self.image = pygame.transform.scale(self.image, [int(self.radius*2), int(self.radius*2)])
        try:
            pygame.draw.ellipse(self.image, [84+int(171*(1-self.intensity)), 171+int(84*(1-self.intensity)), 191+int(64*(1-self.intensity))], [0, 0, int(self.radius*2), int(self.radius*2)], int(8*self.intensity)+1)
        except:
            pygame.draw.ellipse(self.image, [84+int(171*(1-self.intensity)), 171+int(84*(1-self.intensity)), 191+int(64*(1-self.intensity))], [0, 0, int(self.radius * 2), int(self.radius * 2)],
                                1)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter
        self.intensity -= self.speed
        if self.intensity <= 0:
            self.kill()
