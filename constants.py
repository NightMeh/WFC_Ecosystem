from os import path

FPS = 4
SCREENWIDTH = 880
SCREENHEIGHT = 880
CELLSIZE = 40
WFCWEIGHTS = [100,30,10,5,1,1]
MAXWEIGHT = 100000
MINWEIGHT = 0.0000001
MAIN_FOLDER = path.dirname(__file__)
ASSETS_FOLDER = path.join(MAIN_FOLDER, "assets")
TILES_FOLDER = path.join(ASSETS_FOLDER, "tiles")
CREATURE_FOLDER = path.join(ASSETS_FOLDER, "creatures")
BERRYIMG = path.join(ASSETS_FOLDER, "objects", "berrybush.png")
NONTRAVERSABLE_MOVEMENT_MODIFYER = 1000000
BERRYCONST = 0.5

#Animal Stats
PREYCOUNT = 1
PREDATORCOUNT = 1

MAXWANDERDISTANCE = 10
MULTI = 0.1
BASECHOICEWEIGHTS = [1,1,1] #eat,wander,reproduce
MAXCHOICEWEIGHT = 300

URGELOSSPERSTEP = 5
SEXLIST = ["m","f"]

#Prey
BASE_ENERGY_PREY = 200
MINDEATHAGE_PREY = 700
MAXDEATHAGE_PREY = 1000
MAXOFFSPRING_PREY = 7
MINOFFSPRING_PREY = 3
URGE_REPRODUCE_PREY = 500
TIMEBETWEENMATES_PREY = 10
MINREPROAGE_PREY = 10
BERRYENERGYREFILL = 100
ENERGYLOSSPERSTEP_PREY = 3

#Predator
BASE_ENERGY_PREDATOR = 400
URGE_REPRODUCE_PREDATOR = 600
TIMEBETWEENMATES_PREDATOR = 100
ENERGYLOSSPERSTEP_PREDATOR = 5
MINDEATHAGE_PREDATOR = 2000
MAXDEATHAGE_PREDATOR = 3000
MINREPROAGE_PREDATOR = 100



