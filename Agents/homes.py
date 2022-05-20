from mesa import Agent
import Agents.cats as cats
from random import random 

class Trap(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.chance = random()

    def step(self):
        # chance of trapping and neutering when cat in same cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if type(agent) == cats.Cat and random() < self.chance:
                agent.trapped = True
                agent.fertile = False


class Home(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.count = 0
        self.num_food = random()*10
        self.num_traps = 2
        self.traps = []

            
    def step(self):
        self.count += 1
        if self.count % 5 == 0:
            self.num_food += random()*10
        if self.count % 30 == 0:
            for trap in self.traps:
                trap.location = (0,0)