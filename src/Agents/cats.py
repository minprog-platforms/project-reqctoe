"""
cats.py
Programmeerproject
Eline van de Lagemaat (11892900)

TODO
"""

from mesa import Agent
import Agents.homes as homes
from functions import get_distance, get_normed_diff
from statistics import NormalDist
from uuid import uuid4
from random import random, choice


class Cat(Agent):
    """TODO hail whlceihs"""

    HUNGER_THRESHOLD = 0.5

    def __init__(self, unique_id, model, age=0):
        super().__init__(unique_id, model)
        self.model = model

        self.age = age
        self.mating = 0
        # these parameters are altered by trap agents in homes.py
        self.trapped = False
        self.neutered = False

        # roaming parameters
        self.max_distance = model.colony_center[1]/2
        self.hunger = 0
    

    @property
    def hungry(self):
        """Determine if cat is hungry"""
        return self.hunger > self.HUNGER_THRESHOLD


    @property
    def fertile(self):
        """Determine if cat is fertile"""
        return self.age > 10 and not self.neutered and self.mating < 1
    

    @property
    def dead(self):
        """Determine if cat is dead and if so kill cat"""
        # different life expectancy based on fertility
        if self.fertile:
            avg_age = 100
        else:
            avg_age = 400

        # kitten disease death
        if self.age < 12 and random() < 0.05:
            pass
        # death from old age
        elif self.age > avg_age and random() < 0.05:
            pass
        # death from hunger
        elif self.hunger > 2.5:
            pass
        # still alive 
        else:
            return False

        # kill cat
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

        return True


    def make_kittens(self, mate):
        """Generate new cat agents"""
        # partners can't mate for a few steps
        self.mating = 5
        mate.mating = 1

        # produce 2 to 6 kittens
        litter = choice(range(2,7))
        for _ in range(litter):
            cat = Cat(uuid4(), self.model)

            # place cat at position of parent
            self.model.schedule.add(cat)
            self.model.grid.place_agent(cat, self.pos)


    def interact(self, agents):
        """TODO function description"""
        # iterate through agents in cell
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
                    self.model.move_colony(self.pos)
            # mating
            elif self.fertile:
                if type(agent) == Cat and agent is not self:
                    if agent.fertile and random() < 0.01:
                        self.make_kittens(agent)
                        return
    

    def move(self):
        """TODO function description"""
        # retrieve neighboring cells
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)
        possible_steps = []
        distances = []

        # check if steps allowed 
        for step in neighborhood:
            distance = get_distance(self.model.colony_center, step)
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)
        
        # when cat is out of bounds, take step toward colony
        if len(possible_steps) == 0:
            # calculate direction to move in 
            direction = get_normed_diff(self.pos, self.model.colony_center)
            
            x = self.pos[0] + round(direction[0])
            y = self.pos[1] + round(direction[1])

            self.model.grid.move_agent(self, (x,y))
            return

        # calculate preferred direction based on normal distribution
        weights = []
        for r in distances:
            weight = NormalDist(mu=0, sigma=(self.max_distance/4)).pdf(r) 
            # away from colony if hungry
            if self.hungry:
                weight = 1 - weight
            # toward colony otherwise
            if r > get_distance(self.pos, self.model.colony_center):
                weights.append(weight)  
            else:
                weights.append(1 - weight)

        # take weighted step
        new_pos = self.random.choices(possible_steps, weights=weights, k=1)[0]
        self.model.grid.move_agent(self, new_pos)


    def step(self):
        """TODO function description"""
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
        
        self.move()
        self.mating -= 1 
