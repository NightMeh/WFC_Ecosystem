from constants import *
from pathfinder import PathFinder,Stack
import random
import math
import pygame


class CreatureCell:
    def __init__(self,position,tile) -> None:
        self.position = (position[0],position[1])
        self.tile = tile
        self.g_cost = 0 #dist from start
        self.h_cost = 0 #dist from end
        self.f_cost = 0 #Gcost+Hcost
        self.pointer = None
        self.traversable = self.tile.traversable

class Creature:
    def __init__(self,position,world,renderer):
        self.position = position
        self.energy = BASE_ENERGY
        self.urgeReproduce = URGE_REPRODUCE
        self.worldmap = world
        self.currentpath = Stack()
        self.renderer = renderer
        self.count = 0
        self.foodTarget = None
        self.mate = None
        self.matePosition = None
        self.sex = random.choice(SEXLIST)
        self.alive = True
        self.age = 0
        self.deathage = random.randint(MINDEATHAGE,MAXDEATHAGE)
        self.timebetweenmates = 0
        

        _map = self.CreateCreatureWorld()
        self.world = _map
    
    def RequestMate(self, mate):
        if self.mate == None:
            self.mate = mate
            return True
        else:return False


    def PotentialMateFound(self, mate):
        if mate.RequestMate(self):
            self.mate = mate
            return True
        else:return False

    def GetDistanceBetween(self,item1,item2):
        dx = item1.position[0] - item2.position[0]
        dy = item1.position[1] - item2.position[1]
        return math.sqrt(dx*dx + dy*dy)


    def CreateCreatureWorld(self):
        world = []
        for index,row in enumerate(self.worldmap):
            world.append([])
            for cell in row:
                world[index].append(CreatureCell(cell.position,cell.tile))

        return world

    def LocateMate(self,preyLookingForMate):
        self.energy -= LOSSPERSTEP
        if self not in preyLookingForMate:
            preyLookingForMate.append(self)
        lowest = 99999999
        closestmate = None
        for prey in preyLookingForMate:
            if self.GetDistanceBetween(self.position,prey.position) < lowest and prey.sex != self.sex:
                closestmate = prey

        if closestmate != None:
            if self.mate == None:
                if self.sex == "f":
                    if closestmate.sex == "m":
                        if self.PotentialMateFound(closestmate):
                            preyLookingForMate.remove(self)
                            preyLookingForMate.remove(self.mate)
                            #wait
                if self.sex == "m":
                    if closestmate.sex == "f":
                        if self.PotentialMateFound(closestmate):
                            preyLookingForMate.remove(self)
                            preyLookingForMate.remove(self.mate)
                            target = self.mate.position
                            if target.position != self.position.position:
                                self.currentpath = self.FindPath(target)
                       

    def AdvancePath(self):
        #self.position = self.worldmap[self.currentpath.stack[self.currentpath.size][0]][self.currentpath.stack[self.currentpath.size][1]]
        self.position = self.currentpath.stack[self.currentpath.size]
        self.currentpath.RemoveFromStack()
        if self.foodTarget and self.foodTarget.position == self.position.position:
            self.energy = BASE_ENERGY
            self.foodTarget.hasTarget = False
            return 0

        if self.mate and self.mate.position.position == self.position.position:
            self.timebetweenmates = 0
            self.urgeReproduce = URGE_REPRODUCE
            self.mate.urgeReproduce = URGE_REPRODUCE
            self.mate.mate = None
            self.mate = None
            return 1
        self.energy -= LOSSPERSTEP
        return -1
        #if len(self.currentpath.stack) == 0: self.currentpath = None
        

    def FindPath(self,target):
        if target.position == self.position.position:print("error")
        self.world = self.CreateCreatureWorld() # i wanna remove THIS
        #move towards target, otherwise create a random target position
        pathfinder = PathFinder(self,target)
        pathfinder.InitiatePathfind()
        currentpath = pathfinder.path
        
        return currentpath
        

    def Wander(self,spawnableList):
        possibleWanderTiles = []
        for item in spawnableList:
            if self.GetDistanceBetween(self.position,item) <= MAXWANDERDISTANCE and item.position != self.position.position:
                possibleWanderTiles.append(item)

        cell = random.choice(possibleWanderTiles)
        cell = self.world[cell.position[0]][cell.position[1]]
        return cell


class Predator(Creature):
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"fox.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.urgeHunt = URGE_HUNT

    def Hunt(self,preyList):
        lowest = 99999999
        lowestprey = None
        for prey in preyList:
            dist = self.GetDistanceBetween(prey,self)
            if not(prey.hasTarget) and dist < lowest:
                lowest = dist
                lowestprey = prey
        lowestpreyInCreatureWorld = self.world[lowestprey.position[0]][lowestprey.position[1]]
        lowestpreyInCreatureWorld.hasPredator = True
        return lowestpreyInCreatureWorld

    def Update(self):
        pass

class Prey(Creature):
    def __init__(self,position,world,renderer):
        super().__init__(position,world,renderer)
        self.img = pygame.transform.scale(pygame.image.load(path.join(CREATURE_FOLDER,"rabbit.png")).convert_alpha(),(CELLSIZE,CELLSIZE))
        self.hasPredator = False
        self.health = BASE_HEALTH
        self.lookingForMate = False
        

    def Update(self,berryList,fertileList,spawnableList,preyLookingForMate):
        self.age += 1
        self.timebetweenmates += 1
        if self.age < MINREPROAGE or self.timebetweenmates <= TIMEBETWEENMATES:
            self.urgeReproduce -= URGELOSSPERSTEP
        if self.energy <= 0 or (self.age >= self.deathage):
            if self.mate:
                self.mate.mate = None
                self.mate = None
            if self.foodTarget:
                self.foodTarget.hasTarget = False
                self.foodTarget = None
                
            if self in preyLookingForMate:
                preyLookingForMate.remove(self)
            self.alive = False
            return -1
        if len(self.currentpath.stack) == 0:
            self.foodTarget = None
            option = self.ChooseActivity()
            match option[0]:
                case "f":
                    pass
                case "e":
                    target = self.Forage(berryList)
                    if target == -1:
                        target = self.Wander(spawnableList)
                        self.currentpath = self.FindPath(target)
                    elif target.position == self.position.position:
                        self.currentpath.AddToStack(target)
                        self.AdvancePath()
                    else:
                        self.currentpath = self.FindPath(target)
                case "w":
                    target = self.Wander(spawnableList)
                    self.currentpath = self.FindPath(target)
                case "r":
                    self.LocateMate(preyLookingForMate)
                        
        else:
            if self.mate:
                if self.foodTarget:
                    self.foodTarget.hasTarget = False
                    self.foodTarget.target = None
                    self.foodTarget = None
                if self.currentpath.stack[0].position != self.mate.position.position and self.position.position != self.mate.position.position:
                    target = self.mate.position
                    self.currentpath = self.FindPath(target)
                elif self.sex[0] == "m" and self.mate.position.position != self.position.position:
                    action = self.AdvancePath()
                    if action == 1:
                        return 0
                elif self.sex[0] == "m" and self.mate.position.position == self.position.position:
                    return 0

                pass
            else:
                action = self.AdvancePath()
                if action == 0:
                    berryList.remove(self.foodTarget)
                    fertileList.append(self.foodTarget)
                
                    

        self.renderer.DrawCreature(self)

    def ChooseActivity(self):
        choiceweights = BASECHOICEWEIGHTS.copy()
        if self.hasPredator:
            return "f"

        choiceweights[0] += (BASE_ENERGY-self.energy) #eat chance
        choiceweights[1] += (self.energy/BASE_ENERGY + self.urgeReproduce/URGE_REPRODUCE)*10 #chance to wander
        choiceweights[2] += (URGE_REPRODUCE-self.urgeReproduce)*MULTI  #chance to reproduce
        
        for index,weight in enumerate(choiceweights):
            weight = min(max(weight,0.1),MAXCHOICEWEIGHT)
            choiceweights[index] = weight
        if self.age < MINREPROAGE or self.timebetweenmates <= TIMEBETWEENMATES:
            choiceweights[2] = 0
        return random.choices(["e","w","r"],choiceweights,k=1)

    def Forage(self,berryList):
        lowest = 99999999
        lowestberry = None
        for berry in berryList:
            dist = self.GetDistanceBetween(berry,self.position)
            if not(berry.hasTarget) and dist < lowest:
                lowest = dist
                lowestberry = berry
        if lowestberry == None:
            return -1
        lowestberry.target = self
        lowestberry.hasTarget = True
        self.foodTarget = lowestberry
        lowestberryInCreatureWorld = self.world[lowestberry.position[0]][lowestberry.position[1]]
        return lowestberryInCreatureWorld

    def Flee(self):
        #run from the predator chasing
        pass


         


