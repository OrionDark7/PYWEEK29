import pygame

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/ENTITIES.PY
"""

pygame.init()

#OBJECT DEFINITION STUFF
class Pebble(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([4, 4])
        self.image.fill([128, 128, 128])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
    def update(self):
        self.coords = self.rect.left, self.rect.top

class Boat(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([80, 40])
        self.image.fill([237, 244, 161])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.coords = [self.rect.left, self.rect.top]
    def draw(self, surface):
        surface.blit(self.image, self.coords)
    def update(self, ripples):
        pass

class Ripples(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)