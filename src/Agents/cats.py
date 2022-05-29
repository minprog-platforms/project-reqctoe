from mesa import Agent
import Agents.homes as homes
from math import sqrt
from statistics import NormalDist
from uuid import uuid4
from random import random, choice

class Cat(Agent):

    HUNGER_THRESHOLD = 1/2

    def __init__(self, unique_id, model, center, age=0):
        super().__init__(unique_id, model)
        self.model = model

        # TODO "kitten locked" als ze aan het maten zijn

        self.age = age
        self.trapped = False
        self.neutered = False
        self.mating = 0

        self.colony_center = center
        self.max_distance = model.colony_center[1]/2
        self.hunger = 0
    
    @property
    def hungry(self):
        return self.hunger > self.HUNGER_THRESHOLD

    @property
    def fertile(self):
        return self.age > 10 and not self.neutered and self.mating < 1
    
    @property
    def dead(self):
        # different life expectancy based on fertility
        if self.fertile:
            avg_age = 100
        else:
            avg_age = 400

        # kitten disease death
        if self.age < 12 and random() < 0.05:
            # TODO print("disease")
            pass
        
        # death from old age
        elif self.age > avg_age and random() < 0.05:
            # TODO print("old age")
            pass

        # death from hunger
        elif self.hunger > 2.5:
            # TODO print("starved")
            pass
        
        # still alive 
        else:
            return False

        # kill cat
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

        return True

    def make_kittens(self, mate):
        # produce 1 to 4 kittens
        self.mating = 5
        mate.mating = 1

        litter = choice(range(2,7))
        # TODO temporary print
        # print(litter)
        for _ in range(litter):
            id = uuid4()
            cat = Cat(id, self.model, self.colony_center)

            # plaats kat en voeg toe aan planning
            self.model.schedule.add(cat)
            # place cat at position of parent
            self.model.grid.place_agent(cat, self.pos)

    def interact(self, agents):
        # iterate through agents
        for agent in agents:
            # eating
            if type(agent) == homes.Home:
                # check if food available
                if agent.num_food > 0:
                    # eat belly full
                    if agent.num_food > self.hunger :
                        agent.num_food -= self.hunger
                        self.hunger = 0
                    # eat bowl empty
                    else:
                        self.hunger -= agent.num_food
                        agent.num_food = 0
                        print("empty!")
                    # TODO move colony center
            # mating
            elif self.fertile:
                if type(agent) == Cat and agent is not self:
                    if agent.fertile and random() < 0.01:

                        self.make_kittens(agent)
                        return
    
    # Movement 
    def move(self):
        # retrieve neighboring cells
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        possible_steps = []
        distances = []

        # check if steps allowed 
        for step in neighborhood:
            distance = self.get_distance()
            distance = (self.colony_center[0] - step[0])**2 + (self.colony_center[1] - step[1])**2
            distance = sqrt(distance)
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)
        
        # calculate weights based on normal distribution
        weights = []
        for r in distances:
            weight = NormalDist(mu=0, sigma=(self.max_distance/2)).cdf(r)
            if self.hungry:
                # away from colony
                weights.append(weight)
            else:
                # towards colony
                weights.append(1 - weight)
        
        # take weighted step
        new_pos = self.random.choices(possible_steps, weights=weights, k=1)[0]
        self.model.grid.move_agent(self, new_pos)


    def step(self):
        # increase hunger and analyse location contents
        self.hunger += 0.05
        self.age += 1  

        if self.dead:
            return
        
        # no actions when trapped
        if self.trapped:
            self.trapped = False
            return
        
        # interaction with other agents in cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        if len(cell_contents) > 1:
            self.interact(cell_contents)
        
        # movement
        self.move()

        self.mating -= 1 
