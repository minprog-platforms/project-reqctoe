class Trap(Agent):

    def __init__(self, home, cell):
        # self.home = home
        self.location = cell
        self.chance = random()

    def step(self):
        # chance of trapping and neutering when cat in same cell
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cell_contents:
            if type(agent) == Cats and random() < self.chance:
                agent.trapped = True
                agent.fertile = False


class Home(Agent):
    
    def __init__(self, T):
        self.count = 0
        self.num_food = random()*10
        self.num_traps = T
        self.traps = []
        for trap in self.num_traps:
            cell = 0
            self.traps.append(Trap(self, cell))
            
    def step(self):
        self.count += 1
        if self.count % 5 == 0:
            self.num_food += random()*10
        if self.count % 30 == 0:
            for trap in self.traps:
                trap.location = (0,0)