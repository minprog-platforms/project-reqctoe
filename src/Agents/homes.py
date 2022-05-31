"""
homes.py
Programmeerproject
Eline van de Lagemaat (11892900)

The Trap agent class creates cat traps with a chance of trapping cats 
in same cell every step. When a cat is trapped, it is neutered.

The Home agent class can have their own trap which they occasionally move. 
They also regularly put out food for the cats.
"""

from mesa import Agent
import Agents.cats as cats
from functions import get_distance
from random import random 


class Trap(Agent):
    """ Agent class representing traps."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.chance = random()


    def step(self):
        """ Trap cat agents in same cell and neuter them."""
        # retrieve agents in same cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            # try to neuter found cats
            if type(agent) == cats.Cat and agent.fertile and random() < self.chance:
                agent.trapped = True
                agent.neutered = True
                # neuter only one cat per step
                return


class Home(Agent):
    """ Agent class representing homes."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.count = 0
        self.num_food = random()*10
        self.trap_dist = 5
        self.traps = []


    def move_trap(self, trap):
        """ Move traps belonging to current home"""
        found_empty_pos = False

        # generate new location and check if allowed
        while not found_empty_pos:
            x = self.random.randrange(self.model.grid.width)
            y = self.random.randrange(self.model.grid.height)

            # requirements for new location
            if len(self.model.grid.get_cell_list_contents((x,y))) == 0 and (get_distance(self.pos, (x,y)) < self.trap_dist):
                found_empty_pos = True

        self.model.grid.move_agent(trap,(x,y))
            


    def step(self):
        """ Provide food every 5 steps and move traps."""
        self.count += 1
        # regularly put out food
        if self.count % 5 == 0:
            self.num_food += random()*100
        # move traps sometimes
        for trap in self.traps:
            if random() < 1/30:
                self.move_trap(trap)