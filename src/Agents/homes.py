from mesa import Agent
import Agents.cats as cats
from functions import get_distance
from random import random 


class Trap(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.chance = random()


    def step(self):
        # chance of trapping and neutering when cat in same cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if type(agent) == cats.Cat and agent.fertile and random() < self.chance:
                agent.trapped = True
                agent.neutered = True
                return


class Home(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.count = 0
        self.num_food = random()*10
        self.trap_dist = 5
        self.traps = []


    def move_trap(self, trap):
        found_empty_pos = False

        # generate new location and check if allowed
        while not found_empty_pos:
            x = self.random.randrange(self.model.grid.width)
            y = self.random.randrange(self.model.grid.height)

            if len(self.model.grid.get_cell_list_contents((x,y))) == 0 and (get_distance(self.pos, (x,y)) < self.trap_dist):
                found_empty_pos = True

        self.model.grid.move_agent(trap,(x,y))
            

    def step(self):
        self.count += 1
        # regularly put out food
        if self.count % 5 == 0:
            self.num_food += random()*100
        # move traps sometimes
        for trap in self.traps:
            if random() < 1/30:
                self.move_trap(trap)