import pygame

#Copyright Orion Williams 2020
#See LICENSE

#INITIATION STUFF
pygame.init()
pygame.display.init()
pygame.mixer.init()

#PYGAME SETUP STUFF
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption("PYWEEK 29")

#DEFINITION STUFF
running = True
screen = "game"

#GAME LOOP STUFF
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

#CLOSE GAME STUFF
pygame.quit()