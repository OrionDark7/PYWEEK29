import pytmx, pygame
from game import objects

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/MAPLOADER.PY
"""

pygame.init()

def loadmap(level):
    data = pytmx.TiledMap("./resources/tiles/"+str(level)+".tmx")
    alltiles = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    floatys = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    for x in range(20):
        for y in range(15):
            properties = data.get_tile_properties(x, y, 0)
            if properties["type"] == "ground":
                obj = objects.Wall([x*40, y*40])
                walls.add(obj)
                alltiles.add(obj)
            if properties["type"] == "gate":
                obj = objects.Gate([x*40, y*40])
                alltiles.add(obj)
            if properties["type"] == "rock" or properties["type"] == "lilly":
                obj = objects.Floaty([x * 40, y * 40], properties["type"])
                floatys.add(obj)
                alltiles.add(obj)
            if properties["type"] == "coin":
                obj = objects.Floaty([x * 40, y * 40], properties["type"])
                floatys.add(obj)
                alltiles.add(obj)

    return alltiles, walls, floatys, coins