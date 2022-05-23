from mesa import Agent
import Agents.homes as homes
from math import sqrt
from statistics import NormalDist
from uuid import uuid4
from random import random 

class Cat(Agent):

    HUNGER_THRESHOLD = 1/2

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.age = 0
        self.fertile = True
        # self.colony = colony
        self.trapped = False
        self.colony_center = (6,6)
        self.max_distance = 50
        self.hunger = 0
    
    @property
    def hungry(self):
        return self.hunger > self.HUNGER_THRESHOLD

    def make_kittens(self):
        # hier moet een functie komen die nieuwe agents creeert 
        id = uuid4()
        cat = Cat(id, self.model)
        # anders
        cat.fertile = False
        self.model.schedule.add(cat)
        # TODO place cat at posotion of parent
        self.model.grid.place_agent(cat, self.colony_center)

        # model.grid
        pass

    def interact(self, agents):
        # iterate through agents
        for agent in agents:
            # eating
            if type(agent) == homes.Home:
                if agent.num_food > 0:
                    agent.num_food-= self.hunger
                    self.hunger = 0
            # mating
            elif self.fertile:
                if type(agent) == Cat and agent is not self:
                    if agent.fertile and random() < 0.010:
                        print("kitten!")
                        self.make_kittens()
                    pass
    
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
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)

        
        # calculate weights based on normal distribution
        weights = []
        for r in distances:
            weight = NormalDist(mu=0, sigma=1).cdf(r)
            if self.hunger > self.HUNGER_THRESHOLD:
                # Away from colony
                weights.append(weight)
            else:
                # Towards colony
                weights.append(1 - weight)


        # take weighted step
        new_pos = self.random.choices(possible_steps, weights=weights, k=1)[0]
        print(new_pos)
        self.model.grid.move_agent(self, new_pos)


    def step(self):
        # increase hunger and analyse location contents
        self.hunger += 0.05
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
