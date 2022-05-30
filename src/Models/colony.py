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
    
    def __init__(self, cats, homes, width, height):
        # TODO super().__init_()
        self.running = True
        # TODO optioneel verschillende kolonieën met verschillende center/ center ook randomly generated maken
        self.colony_center = (round(width/2), round(height/2))
        self.num_cats = cats
        self.num_homes = homes
        self.grid = MultiGrid(width, height, True)
        self.schedule = BaseScheduler(self)

        # huis trap trap, huis trap trap
        for _ in range(self.num_homes):
           
            id = int(uuid4())
            home = Home(id,self)
            self.schedule.add(home)
            
            # place home at random location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # TODO dit staat nu nog toe dat er huizen op dezelfde plek zijn
            self.grid.place_agent(home,(x,y))
            
            # TODO traps laten variëren en op plek weg van huis plaatsen
            # place a variable number of traps for every home
            num_traps = self.random.randrange(2)
            for _ in range(num_traps):
                id = int(uuid4())
                trap = Trap(id, self)
                self.schedule.add(trap)
                self.grid.place_agent(trap,(x,y))
                home.traps.append(trap)


        # scheduler na alle homes en traps
        for _ in range(self.num_homes, self.num_homes + self.num_cats):
            # make the cats
            id = int(uuid4())
            age = self.random.randrange(150)
            cat = Cat(id, self, self.colony_center, age)
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
        # self.datacollector.collect(self)
        self.schedule.step()