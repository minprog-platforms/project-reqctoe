"""
colony.py
Programmeerproject
Eline van de Lagemaat (11892900)

ColonyModel generates a model for a cat colony living in an urban setting.
The model includes homes, cat traps and cats which are all called upon 
in the step function.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from paramiko import Agent
from Agents.homes import Home, Trap
from Agents.cats import Cat
from Agents.food import Food
from functions import get_normed_diff
from uuid import uuid4
from random import random


class ColonyModel(Model):
    """ Model class representing an urban cat colony. """

    def __init__(self, cats, homes, traps, food, width, height):
        self.running = True
        self.colony_center = (round(width/2), round(height/2))
        self.num_cats = cats
        self.num_homes = homes
        self.max_traps = traps
        self.food_sources = food
        self.grid = MultiGrid(width, height, True)
        self.schedule = BaseScheduler(self)

        for _ in range(self.num_homes):
            # create home agent
            home = Home(uuid4(), self)
            self.schedule.add(home)
            
            found_empty_pos = False
            while not found_empty_pos:
                # generate random location
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                
                # check if cell empty
                if len(self.grid.get_cell_list_contents((x,y))) == 0:
                    found_empty_pos = True

            # place home in found empty spot
            self.grid.place_agent(home,(x,y))
            
            # place a variable number of traps for every home
            num_traps = self.random.randrange(self.max_traps)
            for _ in range(num_traps):
                trap = Trap(uuid4(), self)
                home.traps.append(trap)

                self.schedule.add(trap)
                self.grid.place_agent(trap,(x,y))

        # keep track of number of houses/traps
        self.num_noncat_agents = self.schedule.get_agent_count()

        # create cat agents
        for _ in range(self.num_cats):
            # make the cats
            age = self.random.randrange(150)
            cat = Cat(uuid4(), self, age)
            self.schedule.add(cat)

            # place cats at center
            self.grid.place_agent(cat,(self.colony_center))

        # create randomly placed food source
        for _ in range(self.food_sources):
            ammount = self.random.random()
            food_source = Food(uuid4(), self, ammount)
            self.schedule.add(food_source)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(food_source, (x,y))


    def move_colony(self, pos):
        """ Move colony center according to found food location."""
        direction = get_normed_diff(self.colony_center, pos)
        
        # displace one cell toward location of food
        x = self.colony_center[0] + round(direction[0])
        y = self.colony_center[1] + round(direction[1])

        self.colony_center = (x,y)


    def step(self):
        """ Call on step function of all agents on grid."""
        # self.datacollector.collect(self)
        self.schedule.step()
        if not 0 < (self.schedule.get_agent_count() - self.num_noncat_agents) < 1000:
            self.running = False
        print(self.schedule.get_agent_count() - self.num_noncat_agents)