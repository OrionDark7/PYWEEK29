import pygame
from game import ui

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: MAIN.PY
"""

#INITIATION STUFF
pygame.init()
pygame.display.init()
pygame.mixer.init()

#PYGAME SETUP STUFF
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("PYWEEK 29")

#GAME SETUP STUFF
menubuttons = pygame.sprite.Group()
playbutton = ui.TextButton("Play", [400, 100], centered=True)
quitbutton = ui.TextButton("Quit", [400, 150], centered=True)
menubuttons.add(playbutton)
menubuttons.add(quitbutton)

#DEFINITION STUFF
running = True
screen = "menu"
mouse = [0, 0]

#GAME LOOP STUFF
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            mouse = list(pygame.mouse.get_pos())
            if screen == "menu":
                if playbutton.click(mouse):
                    screen = "game"
                elif quitbutton.click(mouse):
                    running = False

    if screen == "menu":
        window.fill([255, 255, 255])
        menubuttons.draw(window)
    if screen == "game":
        window.fill([255, 255, 255])
    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()