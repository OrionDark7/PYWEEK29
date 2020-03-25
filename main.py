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
completebuttons = pygame.sprite.Group()
ui.Color("w")
nextbutton = ui.TextButton("Next Level", [305, 275])
replaybutton = ui.TextButton("Replay Level", [305, 300])
returnbutton = ui.TextButton("Return to Menu", [305, 325])
completebuttons.add(nextbutton)
completebuttons.add(replaybutton)
completebuttons.add(returnbutton)

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
coins = 0
collected: int = 0
startclicked = False
startpos = [Vector2(400, 300), Vector2(100, 100), Vector2(500, 80)]

alltiles = pygame.sprite.Group()
walls = pygame.sprite.Group()
floatys = pygame.sprite.Group()
coingrp = pygame.sprite.Group()
drains = pygame.sprite.Group()
sharks = pygame.sprite.Group()
alltiles, walls, floatys, coingrp, drains, sharks = maploader.loadmap(level)

boat = entities.Boat([360, 280])
pebbles = pygame.sprite.Group()
ripples = pygame.sprite.Group()

def loadLevel(level):
    global boat, alltiles, walls, floatys, drains, startpos, collected, coingrp, sharks
    alltiles = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    floatys = pygame.sprite.Group()
    coingrp = pygame.sprite.Group()
    drains = pygame.sprite.Group()
    sharks = pygame.sprite.Group()
    alltiles, walls, floatys, coingrp, drains, sharks = maploader.loadmap(level)
    boat.rect.center = startpos[level-1]
    boat.coords = boat.rect.left, boat.rect.top
    boat.reachedgate = False
    collected = 0
    boat.collected = 0
    boat.health = 100

def newpebble():
    global mouse, npebble, pebbles, ripples, addedripples
    npebble = entities.Pebble([400, 596], mouse)
    pebbles.add(npebble)
    addedripples = 0
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

def levelcomplete():
    surface = pygame.surface.Surface([200, 150])
    surface.set_alpha(128)
    window.blit(surface, [300, 225])
    ui.SetFont("w", 28)
    ui.Text("Level " + str(level) + " Complete!", window, [305, 225])
    completebuttons.draw(window)

def infobox():
    global boat, collected, window
    surface = pygame.surface.Surface([220, 75])
    surface.set_alpha(127)
    window.blit(surface, [10, 515])
    ui.SetFont("w", 30)
    ui.Text("health - " + str(boat.health) + "%", window, [15, 520])
    ui.Text("coins collected - " + str(collected), window, [15, 555])

def pebbletrail():
    pass

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
                        startclicked = True
                    elif quitbutton.click(mouse):
                        running = False
            if screen == "level complete":
                if pressed[0] == 1:
                    if nextbutton.click(mouse):
                        screen = "game"
                        level += 1
                        loadLevel(level)
                    if replaybutton.click(mouse):
                        screen = "game"
                        loadLevel(level)
                    if returnbutton.click(mouse):
                        screen = "menu"
                        level = 1
            elif screen == "game" and not screen == "menu":
                if pressed[0] == 1:
                    if not startclicked:
                        newpebble()
                    else:
                        startclicked = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.USEREVENT + 1:
            ripples.update(boat, ripples)
            pebbles.update(boat)
            if boat.startripples:
                boat.startripples = False
                nripple = entities.Ripple(boat.startripplesat, 0.01, 1, centered=True)
                ripples.add(nripple)
                addedripples = 1
                pygame.time.set_timer(pygame.USEREVENT + 2, 500)
        elif event.type == pygame.USEREVENT + 2:
            if not addedripples == 0:
                addripples()


    if screen == "menu":
        window.fill([255, 255, 255])
        menubuttons.draw(window)
    if screen == "game":
        collected = boat.collected
        window.fill([57, 119, 155])
        ripples.draw(window)
        alltiles.draw(window)
        walls.draw(window)
        pebbles.draw(window)
        sharks.draw(window)
        boat.draw(window)
        infobox()
        hits = pygame.sprite.spritecollide(boat, ripples, False, pygame.sprite.collide_mask)
        coingrp.update(boat)
        floatys.update(boat)
        drains.update(boat)
        sharks.update(boat)
        boat.update(walls, startpos[level-1])
        alltiles.update(boat)
        if boat.reachedgate:
            screen = "level complete"
            boat.reachedgate=False
            coins += collected
        if len(hits) > 0 and not boat.hitrock:
            for ripple in hits:
                ripple.kill()
                if not ripple.hit:
                    boat.accelerate(ripple, walls)
                ripples.add(ripple)
    if screen == "level complete":
        window.fill([57, 119, 155])
        ripples.draw(window)
        alltiles.draw(window)
        walls.draw(window)
        pebbles.draw(window)
        sharks.draw(window)
        boat.draw(window)
        hits = pygame.sprite.spritecollide(boat, ripples, False, pygame.sprite.collide_mask)
        floatys.update(boat)
        drains.update(boat)
        sharks.update(boat)
        boat.update(walls, startpos[level-1])
        alltiles.update(boat)
        if len(hits) > 0:
            for ripple in hits:
                ripple.kill()
                if not ripple.hit:
                    boat.accelerate(ripple, walls)
                ripples.add(ripple)
        levelcomplete()

    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()