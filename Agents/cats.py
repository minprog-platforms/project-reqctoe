from mesa import Agent

class Cats(Agent):

    HUNGER_THRESHOLD = 1/2

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.age = 0
        self.fertile = True
        # self.colony = colony
        self.trapped = False
        self.colony_center = (6,6)
        self.max_distance = 5
        self.hunger = 0

    def kittens(self):
        # hier moet een functie komen die nieuwe agents creeert 
        pass

    def interact(self, agents):
        # iterate through agents
        for agent in agents:
            # eating
            if type(agent) == Home:
                if agent.num_food > 0:
                    agent.num_food-= self.hunger
                    self.hunger = 0
            # mating
            elif self.fertile == True:
                if type(agent) == Cats and agent is not self:
                    if agent.fertile:
                        # neuken :)
                        pass
    
    # Movement 
    def move(self):
        # retrieve neighboring cells
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)
        possible_steps = []
        distances = []

        # check if steps allowed 
        for step in neighborhood:
            distance = (self.colony_center[0] - step[0])**2 + (self.colony_center[1] - step[1])**2
            distance = sqrt(distance)
            if distance <= self.max_distance:
                possible_steps.append(step)
                distances.append(distance)

        # random walking
        if self.hunger > self.HUNGER_THRESHOLD:
            new_pos = random.choice(possible_steps)
            self.model.move_agent(self, new_pos)
        # Normal wandering
        else:
            # calculate weights based on normal distribution
            weights = []
            for r in distances:
                weight = 1 - NormalDist(mu=0, sigma=1).cdf(r)
                weights.append(weight)

            # take weighted step
            new_pos = random.choices(possible_steps, weights=weights, k=1)[0]
            self.model.grid.move_agent(self, new_pos)


    def step(self):
        # increase hunger and analyse location contents
        self.hunger += 0.01
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        
        # no actions when trapped
        if self.trapped:
            self.trapped = False
        # interaction with other agents
        elif len(cell_contents) > 1:
            self.interact(cell_contents)
        # movement
        else:
            self.move()
