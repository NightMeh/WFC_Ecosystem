from os import path

FPS = 999
SCREENHEIGHT = 880
SCREENWIDTH = 880
CELLSIZE = 40
WFCWEIGHTS = [100,30,10,5,1,1]
MAXWEIGHT = 100000
MINWEIGHT = 0.0000001
MAIN_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets")
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles")
BERRYIMG = path.join(ASSETS_FOLDER, "objects", "berrybush.png")
NONTRAVERSABLE_MOVEMENT_MODIFYER = 1000000

#Animal Stats
CREATURECOUNT = 1
BASE_ENERGY = 200
BASE_HEALTH = 100
URGE_HUNT = 100
URGE_REPRODUCE = 100

