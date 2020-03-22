import pygame, pickle
from game import ui, entities

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
pygame.display.set_caption("PyWeek 29")

pygame.time.set_timer(pygame.USEREVENT + 1, 100)

#GAME SETUP STUFF
menubuttons = pygame.sprite.Group()
playbutton = ui.TextButton("Play", [400, 100], centered=True)
quitbutton = ui.TextButton("Quit", [400, 150], centered=True)
menubuttons.add(playbutton)
menubuttons.add(quitbutton)

ui.Color([255, 0, 0])
backbutton = ui.TextButton("Back", [10, 10])

#DEFINITION STUFF
running = True
screen = "menu"
prevscreen = "menu"
mouse = [0, 0]

boat = entities.Boat([360, 280])
pebbles = pygame.sprite.Group()
ripples = pygame.sprite.Group()

def newpebble():
    global mouse
    npebble = entities.Pebble(mouse)
    pebbles.add(npebble)
    nripple = entities.Ripple(npebble.rect.center, 0.1, centered=True)
    ripples.add(nripple)

#GAME LOOP STUFF
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = pygame.mouse.get_pressed()
            mouse = list(pygame.mouse.get_pos())
            if screen == "menu":
                if pressed[0] == 1:
                    if playbutton.click(mouse):
                        screen = "game"
                    elif quitbutton.click(mouse):
                        running = False
            elif screen == "game":
                if pressed[0] == 1:
                    newpebble()
        elif event.type == pygame.USEREVENT + 1:
            ripples.update(boat, ripples)

    if screen == "menu":
        window.fill([255, 255, 255])
        menubuttons.draw(window)
        backbutton.draw(window)
    if screen == "game":
        window.fill([57, 119, 155])
        pebbles.draw(window)
        ripples.draw(window)
        boat.draw(window)
    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()