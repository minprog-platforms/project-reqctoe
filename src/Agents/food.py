"""
food.py
Programmeerproject
Eline van de Lagemaat (11892900)

Randomly placed food source for the cats. 
There's a chance of movement every step and it also moves when "eaten".
"""

from mesa import Agent


class Food(Agent):
    """ Agent class for food source."""
    
    def __init__(self, unique_id, model, ammount):
        super().__init__(unique_id, model)
        self.model = model
        self.ammount = ammount


    def move(self):
        """ Random movement function."""
        x = self.model.random.randrange(self.model.grid.width)
        y = self.model.random.randrange(self.model.grid.height)

        self.model.grid.move_agent(self,(x,y))


    def step(self):
        """ Small chance of movement every step."""
        if self.random.random() < 0.05:
            self.move()
