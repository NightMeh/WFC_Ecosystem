from os import path

FPS = 999
RECURSIONDEPTH = 10**6
SCREENHEIGHT = 880
SCREENWIDTH = 880
CELLSIZE = 20
WFCWEIGHTS = [100,30,10,5,1,1]
MAXWEIGHT = 100000
MINWEIGHT = 0.0000001
MAIN_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets")
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles")

#Animal Stats
BASEENERGY = 200
URGEHUNT = 100
URGEREPRODUCE = 100
