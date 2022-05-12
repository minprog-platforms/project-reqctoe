from agents.cats import Cats

class CatModel(Model):
    
    def __init__(self, C, H, T, width, height):
        self.num_cats = C
        self.num_homes = H
        # self.num_traps = T
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        for i in range(self.num_cats):
            # make the cats
            a = Cats(i, self)
            self.schedule.add(a)

            # place cats at colony center
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a,(x,y))

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()