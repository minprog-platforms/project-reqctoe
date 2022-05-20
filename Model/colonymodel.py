from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from Agents.homes import Home, Trap
from Agents.cats import Cat
from uuid import uuid4


class CatModel(Model):
    
    def __init__(self, C, H, width, height):
        # super().__init_()
        self.colony_center = (round(width/2), round(height/2))
        self.num_cats = C
        self.num_homes = H
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
            # dit staat nu nog toe dat er huizen op dezelfde plek zijn
            self.grid.place_agent(home,(x,y))
            
            for _ in range(2):
                id = int(uuid4())
                trap = Trap(id, self)
                self.schedule.add(trap)
                home.traps.append(trap)


        # scheduler na alle homes en traps
        for _ in range(self.num_homes, self.num_homes + self.num_cats):
            # make the cats
            id = int(uuid4())
            cat = Cat(id, self)
            self.schedule.add(cat)

            # place cats at center
            self.grid.place_agent(cat,(self.colony_center))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )


    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()