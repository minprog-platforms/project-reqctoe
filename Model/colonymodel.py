from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from Agents.cats import Cats
from Agents.homes import Home


class CatModel(Model):
    
    def __init__(self, C, H, width, height):
        # super().__init_()
        self.colony_center = (round(1/2*width), round(1/2*height))
        self.num_cats = C
        self.num_homes = H
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_homes):
            a = Home(i,self)
            self.schedule.add(a)
            
            # place home at random location
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            # dit staat nu nog toe dat er huizen op dezelfde plek zijn
            self.grid.place_agent(a,(x,y))

        for i in range(self.num_homes, self.num_homes + self.num_cats):
            # make the cats
            b = Cats(i, self)
            self.schedule.add(b)

            # place cats at center
            self.grid.place_agent(b,(self.colony_center))



    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()