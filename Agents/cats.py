from mesa import Agent
import Agents.homes as homes
from math import sqrt
from statistics import NormalDist
from uuid import uuid4
from random import random 

class Cat(Agent):

    HUNGER_THRESHOLD = 1/2

    def __init__(self, unique_id, model, center):
        super().__init__(unique_id, model)
        self.model = model
        # TODO maak fertility age dependent
        # TODO maak age optional argument voor kittens
        self.age = 0
        self.fertile = True
        # self.colony = colony
        self.trapped = False
        self.colony_center = center
        self.max_distance = model.colony_center[1]/2
        self.hunger = 0
    
    @property
    def hungry(self):
        return self.hunger > self.HUNGER_THRESHOLD

    def make_kittens(self):
        # maak kat agent
        id = uuid4()
        cat = Cat(id, self.model, self.colony_center)
        # TODO deze kan weg als fertility age dependent is in init
        cat.fertile = False

        # plaats kat en voeg toe aan planning
        self.model.schedule.add(cat)
        # TODO place cat at position of parent
        self.model.grid.place_agent(cat, self.colony_center)


    def interact(self, agents):
        # iterate through agents
        for agent in agents:
            # eating
            if type(agent) == homes.Home:
                # TODO voedsel kan nu nog negatief zijn 
                if agent.num_food > 0:
                    agent.num_food-= self.hunger
                    self.hunger = 0
            # mating
            elif self.fertile:
                if type(agent) == Cat and agent is not self:
                    if agent.fertile and random() < 0.07:
                        print("kitten!")
                        self.make_kittens()
    
    # Movement 
    def move(self):
        # retrieve neighboring cells
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        possible_steps = []
        distances = []

        # check if steps allowed 
        for step in neighborhood:
            distance = (self.colony_center[0] - step[0])**2 + (self.colony_center[1] - step[1])**2
            distance = sqrt(distance)
            print(distance, self.max_distance)
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)
        
        # calculate weights based on normal distribution
        weights = []
        for r in distances:
            weight = NormalDist(mu=0, sigma=(self.max_distance/2)).cdf(r)
            print(weight)
            if self.hunger > self.HUNGER_THRESHOLD:
                # away from colony
                weights.append(weight)
            else:
                # towards colony
                # TODO tijdelijke print
                print("toward colony")
                weights.append(1 - weight)
        
        # TODO tijdelijke prints
        print(self.pos)
        print(distances, weights)

        # take weighted step
        new_pos = self.random.choices(possible_steps, weights=weights, k=1)[0]
        self.model.grid.move_agent(self, new_pos)


    def step(self):
        # increase hunger and analyse location contents
        self.hunger += 0.05
        # TODO increase cat age
        # TODO kans op doodgaan vanwege age

        # if not found food in 5/0.05 steps, cat dies
        if self.hunger > 5:
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)
            print("dede")
            return

        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        # no actions when trapped
        if self.trapped:
            self.trapped = False
            return

        # interaction with other agents
        if len(cell_contents) > 1:
            self.interact(cell_contents)
        
        # movement
        self.move()
