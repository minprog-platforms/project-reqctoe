from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from Agents.homes import Home, Trap
from Agents.cats import Cat
from functions import get_distance, get_normed_diff
from uuid import uuid4
from random import random


class ColonyModel(Model):
    
    def __init__(self, cats, homes, traps, width, height):
        self.running = True
        self.colony_center = (round(width/2), round(height/2))
        self.num_cats = cats
        self.num_homes = homes
        self.max_traps = traps
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


        # create cat agents
        for _ in range(self.num_homes, self.num_homes + self.num_cats):
            # make the cats
            age = self.random.randrange(150)
            cat = Cat(uuid4(), self, self.colony_center, age)
            self.schedule.add(cat)

            # place cats at center
            self.grid.place_agent(cat,(self.colony_center))


    # move colony center according to found food locations
    def move_colony(self, pos):
        # displace one cell toward location of food
        direction = get_normed_diff(self.colony_center, pos)
        x = self.colony_center[0] + round(direction[0])
        y = self.colony_center[1] + round(direction[1])

        self.colony_center = (x,y)


    def step(self):
        # TODO self.datacollector.collect(self)
        self.schedule.step()
        print(self.schedule.get_agent_count())