import pytmx, pygame
from game import objects

"""
PyWeek 29 Game
Copyright (c) 2020 Orion Williams
See LICENSE file

Current File: /GAME/MAPLOADER.PY
"""

pygame.init()
linelengths = [0, 1, 1]

def strtolist(string):
    string = string.split(",")
    newlist = []
    for i in string:
        if "(" in i:
            i = i.split("(")[1]
        if ")" in i:
            i = i.split(")")[0]
        newlist.append(float(i))
    return newlist

def metaloader(level):
    meta = open("./resources/tiles/"+str(level)+"/meta.txt", "r")

    data = {"drain":[], "shark":[]}
    finished = False
    for i in range(linelengths[level-1]):
        line = meta.readline()
        if not finished:
            line = line.split(" ")
        if line[1] == ">" and not finished:
            coordinates = line[0], line[2]
            newcoordinates = []
            newcoordinates.append(strtolist(coordinates[0]))
            newcoordinates.append(strtolist(coordinates[1]))
            data["drain"].append(newcoordinates)
        if line[1] == "^" and not finished:
            coordinates = line[0], line[2]
            newcoordinates = []
            newcoordinates.append(strtolist(coordinates[0]))
            newcoordinates.append(strtolist(coordinates[1]))
            data["shark"].append(newcoordinates)
        elif finished:
            break
    return data

def loadmap(level):
    data = pytmx.TiledMap("./resources/tiles/"+str(level)+"/level.tmx")
    metadata = {}
    if linelengths[level-1] > 0:
        metadata = metaloader(level)
    print(metadata)
    print("META")
    alltiles = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    floatys = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    drains = pygame.sprite.Group()
    sharks = pygame.sprite.Group()
    for x in range(20):
        for y in range(15):
            properties = data.get_tile_properties(x, y, 0)
            if properties["type"] == "ground" or properties["type"] == "ground-2":
                if properties["type"] == "ground":
                    obj = objects.Wall([x*40, y*40], 1)
                elif properties["type"] == "ground-2":
                    obj = objects.Wall([x*40, y*40], 2)
                walls.add(obj)
                alltiles.add(obj)
            if properties["type"] == "gate":
                obj = objects.Gate([x*40, y*40])
                alltiles.add(obj)
            if properties["type"] == "rock" or properties["type"] == "lilly" or properties["type"] == "grass":
                obj = objects.Floaty([x * 40, y * 40], properties["type"])
                floatys.add(obj)
                alltiles.add(obj)
            if properties["type"] == "coin":
                obj = objects.Floaty([x * 40, y * 40], properties["type"])
                floatys.add(obj)
                alltiles.add(obj)
            if properties["type"] == "drain":
                linkedto = None
                for entry in metadata["drain"]:
                    if entry[0] == [x, y]:
                        linkedto = entry[1]
                        break
                obj = objects.Drain([x*40, y*40], linkedto)
                alltiles.add(obj)
                drains.add(obj)
            if properties["type"] == "shark":
                goto = [x, y]
                for entry in metadata["shark"]:
                    if entry[0] == [x, y]:
                        goto = entry[1]
                        break
                obj = objects.Shark([x*40, y*40], goto)
                alltiles.add(obj)
                sharks.add(obj)

    return alltiles, walls, floatys, coins, drains, sharks