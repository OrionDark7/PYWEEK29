import pygame

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/UI.PY
"""

pygame.init()

#VARIABLE DEFINITION STUFF
font = pygame.font.Font("./resources/font/eurof55.ttf", 24)
fontcolor = [0, 0, 0]

#FUNCTION DEFENITION STUFF
def Color(color):
    global fontcolor
    if type(color) == str:
        if color == "b":
            fontcolor = [0, 0, 0]
        elif color == "w":
            fontcolor = [255, 255, 255]
        else:
            print("Invalid String Color Option - " + color)
    elif type(color) == list or type(color) == tuple:
        fontcolor = color
    else:
        print("Invalid Color Option - " + str(color))

def Size(size):
    global font
    font = pygame.font.Font("./resources/font/eurof55.ttf", int(size))

def SetFont(color, size):
    global fontcolor, font

    font = pygame.font.Font("./resources/font/eurof55.ttf", int(size))

    if type(color) == str:
        if color == "b":
            fontcolor = [0, 0, 0]
        elif color == "w":
            fontcolor = [255, 255, 255]
        else:
            print("Invalid String Color Option - " + color)
    elif type(color) == list or type(color) == tuple:
        fontcolor = color
    else:
        print("Invalid Color Option - " + str(color))

def Text(text, surface, position):
    global font, fontcolor
    drawtext = font.render(str(text), 0, fontcolor)
    surface.blit(drawtext, list(position))

class TextButton(pygame.sprite.Sprite):
    def __init__(self, text, position, centered=False):
        global font, fontcolor
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(text), 0, list(fontcolor))
        self.rect = self.image.get_rect()
        if centered:
            self.rect.centerx, self.rect.top = list(position)
        else:
            self.rect.left, self.rect.top = list(position)
        self.coords = [self.rect.left, self.rect.top]
    def draw(self, surface): #Single Draw
        surface.blit(self.image, self.coords)
    def update(self, surface): #Group Draw
        surface.blit(self.image, self.coords)
    def click(self, coords):
        clicked = False
        if self.rect.collidepoint(coords):
            clicked = True
        return clicked