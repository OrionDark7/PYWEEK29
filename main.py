import pygame, pickle, pytmx
from pygame.math import Vector2
from game import ui, entities, maploader, objects

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

pygame.time.set_timer(pygame.USEREVENT + 1, 40)
pygame.time.set_timer(pygame.USEREVENT + 2, 500)

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
addedripples = 0
npebble = None
level = 1

alltiles = pygame.sprite.Group()
walls = pygame.sprite.Group()
alltiles, walls = maploader.loadmap(level)

boat = entities.Boat([360, 280])
pebbles = pygame.sprite.Group()
ripples = pygame.sprite.Group()

def newpebble():
    global mouse, npebble, pebbles, ripples, addedripples
    npebble = entities.Pebble(mouse)
    pebbles.add(npebble)
    nripple = entities.Ripple(npebble.rect.center, 0.01, 1, centered=True)
    ripples.add(nripple)
    addedripples = 1
    pygame.time.set_timer(pygame.USEREVENT + 2, 500)

def addripples():
    global npebble, addedripples, ripples
    if addedripples == 1:
        nripple = entities.Ripple(npebble.rect.center, 0.015, 0.5, centered=True)
        ripples.add(nripple)
        addedripples+=1
    if addedripples == 2:
        nripple = entities.Ripple(npebble.rect.center, 0.0175, 0.25, centered=True)
        ripples.add(nripple)
        addedripples += 1
    if addedripples == 3:
        nripple = entities.Ripple(npebble.rect.center, 0.02, 0.2, centered=True)
        ripples.add(nripple)
        addedripples = 0

#GAME LOOP STUFF
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse = list(pygame.mouse.get_pos())
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
            pebbles.update()
        elif event.type == pygame.USEREVENT + 2:
            if not addedripples == 0:
                addripples()


    if screen == "menu":
        window.fill([255, 255, 255])
        menubuttons.draw(window)
        backbutton.draw(window)
    if screen == "game":
        window.fill([57, 119, 155])
        ripples.draw(window)
        alltiles.draw(window)
        walls.draw(window)
        pebbles.draw(window)
        boat.draw(window)
        hits = pygame.sprite.spritecollide(boat, ripples, False, pygame.sprite.collide_mask)
        walls.update(boat)
        boat.update(walls)
        alltiles.update(boat)
        if boat.reachedgate:
            screen = "menu"
            boat.reachedgate=False
        if len(hits) > 0:
            for ripple in hits:
                ripple.kill()
                if not ripple.hit:
                    boat.accelerate(ripple, walls)
                ripples.add(ripple)
    print(boat.velocity)
    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()