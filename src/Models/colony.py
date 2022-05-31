"""
colony.py
Programmeerproject
Eline van de Lagemaat (11892900)

ColonyModel generates a model for a cat colony living in an urban setting.
The model includes homes, cat traps and cats which are all called upon 
in the step function.
"""

from uuid import uuid4

from Agents.cats import Cat
from Agents.food import Food
from Agents.homes import Home, Trap
from functions import get_normed_diff
from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import BaseScheduler


class ColonyModel(Model):
    """ Model class representing an urban cat colony. """

    def __init__(self, cats, max_cats, homes, traps, food, width, height):
        self.running = True
        self.colony_center = (round(width/2), round(height/2))
        self.num_cats = cats
        self.max_cats = max_cats
        self.num_homes = homes
        self.max_traps = traps
        self.food_sources = food
        self.grid = MultiGrid(width, height, True)
    
        self.birth = 0
        self.death = 0
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
            
            # allow for no traps in model
            if self.max_traps == 0:
                continue
            # place a variable number of traps for every home
            num_traps = self.random.randrange(self.max_traps)
            for _ in range(num_traps):
                trap = Trap(uuid4(), self)
                self.schedule.add(trap)

                # place trap at location of home and add to list
                home.traps.append(trap)
                self.grid.place_agent(trap,(x,y))

        # create randomly placed food source
        for _ in range(self.food_sources):
            ammount = self.random.random()
            food_source = Food(uuid4(), self, ammount)
            self.schedule.add(food_source)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)

            self.grid.place_agent(food_source, (x,y))

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

        # create list of data to keep track of
        self.datacollector = DataCollector(model_reporters={
            'Fertile cats': 'count_fertile',
            'Infertile cats': 'count_infertile',
            'Total cats': 'count_cats',
            'Birthrate': 'birth',
            'Deathrate': 'death'})


    @property
    def count_fertile(self):
        """ Calculate number of fertile cats."""
        agents = self.schedule.agents
        n = 0
        # filter agents for cats and check fertility
        for agent in agents:
            if type(agent) == Cat and agent.fertile:
                n += 1
        return n
    

    @property
    def count_infertile(self):
        """ Calculate number of infertile cats."""
        agents = self.schedule.agents
        n = 0
        # filter agents for cats and check fertility
        for agent in agents:
            if type(agent) == Cat and not agent.fertile:
                n += 1
        return n

    @property
    def count_cats(self):
        """ Calculate total number of cats."""
        return self.schedule.get_agent_count() - self.num_noncat_agents
    

    def move_colony(self, pos):
        """ Move colony center according to found food location."""
        direction = get_normed_diff(self.colony_center, pos)
        
        # displace one cell toward location of food
        x = self.colony_center[0] + round(direction[0])
        y = self.colony_center[1] + round(direction[1])

        self.colony_center = (x,y)


    def step(self):
        """ Call on step function of all agents on grid."""
        self.birt = self.death = 0
        self.schedule.step()
        self.datacollector.collect(self)

        # stop de run wanneer alle katten dood zijn of het maximum aantal katten is overschreden
        if not 0 < (self.schedule.get_agent_count() - self.num_noncat_agents) < self.max_cats:
            self.running = False
        print(self.schedule.get_agent_count() - self.num_noncat_agents)
