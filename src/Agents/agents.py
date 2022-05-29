from errno import EEXIST
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from random import random
from statistics import NormalDist
from math import sqrt

class Cats(Agent):

    HUNGER_THRESHOLD = 1/2

    def __init__(self, age, colony, range):
        self.age = age
        self.fertile = True
        self.trapped = False
        self.colony_center = (6,6)
        self.max_distance = range
        self.hunger = 0

    def kittens(self):
        # hier moet een functie komen die nieuwe agents creeert 
        pass

    def interact(self, agents):
        # iterate through agents
        for agent in agents:
            # eating
            if type(agent) == Home:
                if agent.num_food > 0:
                    agent.num_food-= self.hunger
                    self.hunger = 0
            # mating
            elif self.fertile == True:
                if type(agent) == Cats and agent is not self:
                    if agent.fertile:
                        # neuken :)
                        pass
    
    # Movement 
    def move(self):
        # retrieve neighboring cells
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)
        possible_steps = []
        distances = []

        # check if steps allowed 
        for step in neighborhood:
            distance = (self.colony_center[0] - step[0])**2 + (self.colony_center[1] - step[1])**2
            distance = sqrt(distance)
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)

        # random walking
        if self.hunger > self.HUNGER_THRESHOLD:
            new_pos = random.choice(possible_steps)
            self.model.move_agent(self, new_pos)
        # Normal wandering
        else:
            # calculate weights based on normal distribution
            weights = []
            for r in distances:
                weight = 1 - NormalDist(mu=0, sigma=1).cdf(r)
                weights.append(weight)

            # take weighted step
            new_pos = random.choices(possible_steps, weights=weights, k=1)[0]
            self.model.grid.move_agent(self, new_pos)


    def step(self):
        # increase hunger and analyse location contents
        self.hunger += 0.01
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        # no actions when trapped
        if self.trapped:
            self.trapped = False
        # interaction with other agents
        elif len(cell_contents) > 1:
            self.interact(cell_contents)
        # movement
        else:
            self.move()


class Trap(Agent):

    def __init__(self, home, cell):
        # self.home = home
        self.location = cell
        self.chance = random()

    def step(self):
        # chance of trapping and neutering when cat in same cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if type(agent) == Cats and random() < self.chance:
                agent.trapped = True
                agent.fertile = False


class Home(Agent):
    
    def __init__(self, T):
        self.count = 0
        self.num_food = random()*10
        self.num_traps = T
        self.traps = []
        for trap in self.num_traps:
            cell = 0
            self.traps.append(Trap(self, cell))
            
    def step(self):
        self.count += 1
        if self.count % 5 == 0:
            self.num_food += random()*10
        if self.count % 30 == 0:
            for trap in self.traps:
                trap.location = (0,0)


class CatModel(Model):
    
    def __init__(self, C, H, T, width, height):
        self.num_cats = C
        self.num_homes = H
        # self.num_traps = T
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_cats):
            a = Cats(i, self)
            self.schedule.add(a)
            # make the cats

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

