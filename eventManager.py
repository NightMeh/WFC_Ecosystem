from random import choice
from constants import *
from ecosystem import Predator,Prey
from renderer import Renderer
from engine import Engine
import pygame
from waveFunctionCollapse import GenerateMap
import pstats
from numpy import random
import matplotlib.pyplot as plt

class EventManager:
    def __init__(self):
        self.world = [] #The current map
        self.berryList = [] #A list of all berrys
        self.preyList = [] #A list of prey instantiated
        self.predatorList = [] #A list of all predators instantiated
        self.engine = Engine() #Create a new engine, for deltatime and FPS
        self.tilelist = [] #A list of all possible tiles
        self.tiledict = {} #Dictionary of all tile types
        self.fertileList = [] #A list of all fertile land where berrys can grow
        self.spawnableList = [] #A list of all tiles where creatures can spawn
        self.deadPreyList = [] #A list of all prey objects which are deceased
        self.deadPredatorList = [] #A list of all predator objects which are deceased
        self.preyLookingForMate = [] #A list of all prey looking for a mate
        self.predatorLookingForMate = [] #A list of all predators looking for a mate
        self.preyListLength_perframe = []
        self.predatorListLength_perframe = []

    def TempMapViewer(self):
        running = True
        smallrenderer = Renderer(SCREENWIDTH/2,SCREENHEIGHT/2,CELLSIZE/2)

        world = self.CreateWorld()
        smallrenderer.RenderWorld(world)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.world = world
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        world = self.CreateWorld()
                        smallrenderer.RenderWorld(world)
                        pygame.display.flip()
                    elif event.key == pygame.K_ESCAPE:
                        self.world = world
                        running = False
                        pygame.quit()


    def CreateWorld(self): #create a world
        while True:
            #attempt to create a new world
            world,self.tilelist = GenerateMap()
            return world
        

    def SplitWorld(self): #split the world into fertile, spawnable land into a dictionary
        #reset all values, a new world was created
        self.preyList = []
        self.predatorList = []
        self.deadPreyList = []
        self.deadPredatorList = []
        self.tiledict = {}
        self.berryList = []
        self.fertileList = []
        self.spawnableList = []
        self.preyListLength_perframe = []
        self.predatorListLength_perframe = []

        #expand the dictionary to allow all tiles to be added as keys
        for tile in self.tilelist:
            self.tiledict[tile] = []
        #tiles get added as keys
        for row in self.world:
            for cell in row:
                for key in self.tiledict:
                    if cell.tile == key:
                        self.tiledict[key].append(cell)

        #create list of fertile tiles and traversable from the dictionary
        for key in self.tiledict:
            if key.fertile:
                for item in self.tiledict[key]:
                    self.fertileList.append(item)

            if key.traversable:
                for item in self.tiledict[key]:
                    self.spawnableList.append(item)
                


    


    def SpawnBerry(self): #spawn a berry at a random fertile spot
        if len(self.fertileList) != 0:
            newberry = choice(self.fertileList)
            newberry.hasBerry = True #ensure the tile knows it has a berry attatched
            newberry.hasTarget = False 
            self.berryList.append(newberry)
            self.fertileList.remove(newberry)
            self.renderer.RenderBerry(newberry) #render the berry
    
    def BerryUpdate(self):
        for x in range(random.poisson(lam=BERRYCONST,size=1)[0]):
            self.SpawnBerry()

    def InitializeCreatures(self): #instantiate all creatures using the amount of creatures determined from constants
        
        for creature in range(PREYCOUNT):
            #give them a random position, an image and pass both world + renderer as parameters
            self.preyList.append(Prey(choice(self.spawnableList),self.world,self.renderer))
        for creature in range(PREDATORCOUNT):
            self.predatorList.append(Predator(choice(self.spawnableList),self.world,self.renderer))

    def Update(self): #update to be looped once per frame
        self.renderer.RenderWorld(self.world) #draw world
        for berry in self.berryList:
            self.renderer.RenderBerry(berry)
        #update all creatures
        for creature in self.preyList:
            action = creature.Update(self.berryList,self.fertileList,self.spawnableList,self.preyLookingForMate)
            if action == -1: #if dead remove them from preylist
                self.preyList.remove(creature)
            elif action == 0:
                for x in range(random.randint(MINOFFSPRING_PREY,MAXOFFSPRING_PREY)):
                    self.preyList.append(Prey(creature.position,self.world,self.renderer))

        for creature in self.predatorList:
            action = creature.Update(self.preyList,self.spawnableList,self.predatorLookingForMate)
            if action == -1: #if dead remove them from predatorlist
                self.predatorList.remove(creature)
            elif action == 0:
                self.predatorList.append(Predator(creature.position,self.world,self.renderer))

        self.preyListLength_perframe.append(len(self.preyList))
        self.predatorListLength_perframe.append(len(self.predatorList))

        self.BerryUpdate()
        pygame.display.flip()
        pygame.display.set_caption("{:.2f}".format(self.engine.clock.get_fps()))
        

    def Main(self): #main program
        self.renderer = Renderer(SCREENWIDTH,SCREENHEIGHT,CELLSIZE) #Creature a new renderer, for renderering
        if self.world == []:
            self.world = self.CreateWorld()
        
        #self.world = self.CreateWorld() #generate a world
        self.SplitWorld() #split the world into fertile,spawnable,etc.
        self.InitializeCreatures()
        playing = True # create a playing loop
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.world = self.CreateWorld()
                        self.SplitWorld()
                        self.InitializeCreatures()
                    if event.key == pygame.K_u:
                        self.SpawnBerry()
                if event.type == pygame.QUIT:
                    fig = plt.figure()
                    ax = fig.add_subplot(1,1,1)
                    ax.spines["left"].set_position("zero")
                    ax.spines["bottom"].set_position("zero")
                    ax.spines["right"].set_color("none")
                    ax.spines["top"].set_color("none")
                    plt.plot(self.preyListLength_perframe,label="Prey",color="b")
                    plt.plot(self.predatorListLength_perframe,label="Predators",color="r")
                    plt.xlabel("Number of Frames")
                    plt.ylabel("Amount of Creatures")
                    plt.legend()
                    plt.show()
                    
                    """stats = pstats.Stats(pr)
                    stats.sort_stats(pstats.SortKey.TIME)
                    stats.dump_stats(filename="test.prof")"""

                    pygame.quit()
            self.Update()
            self.engine.update_dt()

                