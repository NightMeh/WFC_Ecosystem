from os import path

FPS = 10
SCREENWIDTH = 880
SCREENHEIGHT = 880
CELLSIZE = 80
WFCWEIGHTS = [100,30,10,5,1,1]
MAXWEIGHT = 100000
MINWEIGHT = 0.0000001
MAIN_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets")
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles")
CREATURE_FOLDER = path.join(ASSETS_FOLDER, "creatures")
BERRYIMG = path.join(ASSETS_FOLDER, "objects", "berrybush.png")
NONTRAVERSABLE_MOVEMENT_MODIFYER = 1000000
BERRYCONST = 0.3

#Animal Stats
PREYCOUNT = 10
PREDATORCOUNT = 1
BASE_ENERGY = 200
BASE_HEALTH = 100
URGE_HUNT = 100
URGE_REPRODUCE = 500
TIMEBETWEENMATES = 100
MINDEATHAGE = 2000
MAXDEATHAGE = 3000
TIMEBETWEENMATES_PREDATOR = 100
MINDEATHAGE_PREDATOR = 2000
MAXDEATHAGE_PREDATOR = 3000
MINREPROAGE_PREDATOR = 150
MINREPROAGE = 10
MAXWANDERDISTANCE = 10
MULTI = 0.1
BASECHOICEWEIGHTS = [1,1,1] #eat,wander,reproduce
MAXCHOICEWEIGHT = 300
LOSSPERSTEP = 3
URGELOSSPERSTEP = 2
BERRYENERGYREFILL = 100
LOWENERGYTHRESHOLD_PERCENT = 0.4
LOWENERGYTHRESHOLD = BASE_ENERGY * LOWENERGYTHRESHOLD_PERCENT
SEXLIST = ["m","f"]

