from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from Agents.homes import Home, Trap
from Agents.cats import Cat
from uuid import uuid4


class CatModel(Model):
    
    def __init__(self, cats, homes, width, height):
        # super().__init_()
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
            # dit staat nu nog toe dat er huizen op dezelfde plek zijn
            self.grid.place_agent(home,(x,y))
            
            # TODO # traps laten variëren en op plek weg van huis plaatsen
            for _ in range(1):
                id = int(uuid4())
                trap = Trap(id, self)
                self.schedule.add(trap)
                self.grid.place_agent(trap,(x,y))
                home.traps.append(trap)


        # scheduler na alle homes en traps
        for _ in range(self.num_homes, self.num_homes + self.num_cats):
            # make the cats
            id = int(uuid4())
            cat = Cat(id, self, self.colony_center)
            self.schedule.add(cat)

            # place cats at center
            self.grid.place_agent(cat,(self.colony_center))

        # self.datacollector = DataCollector(
        #     model_reporters={"Gini": compute_gini}, agent_reporters={"Wealth": "wealth"}
        # )

    # def kill_agent(self, agent):
    #     self.schedule.remove(agent)
    #     self.grid.remove_agent(agent)

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()