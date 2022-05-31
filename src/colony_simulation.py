"""
colony_simulation.py
Programmeerproject
Eline van de Lagemaat (11892900)

This file runs the created colonymodel and a webserver for 
the visualization of the results.

"""

import matplotlib.pyplot as plt
import numpy as np
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from Agents.cats import Cat
from Agents.food import Food
from Agents.homes import Home, Trap
from Models.colony import ColonyModel


def agent_portrayal(agent):
    """ Provide different visuals for all agents depending on properties. """
    # general visuals
    portrayal = {"Shape": "circle",
                 "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    # cat alterations
    if type(agent) == Cat:
        portrayal["Color"] = "brown"

        if agent.hungry:
            portrayal["Color"] = "blue"

        if agent.fertile:
            portrayal["Filled"] = "false"
    # home alterations
    elif type(agent) == Food:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
    elif type(agent) == Home:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    # trap alterations
    elif type(agent) == Trap:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.8
        portrayal["h"] = 0.5
        portrayal["Color"] = "black"

    return portrayal


if __name__ == "__main__":
    runmode = "server"

    # parameters for running model
    width = 30
    height = 30
    params = {
        "cats": 15,
        "homes": 75,
        "traps": 2,
        "food": 100,
        "width": width,
        "height": height,
    }

    # animated visualisation
    if runmode == "server":
        grid = CanvasGrid(agent_portrayal, width, height, 500, round(500*height/width))

        # initialize server
        server = ModularServer(ColonyModel,
                        [grid],
                        "Cat Model",
                        params)

        # run server
        server.port = 8521 # The default
        server.launch()
    
    # graph type visualisation
    elif runmode == "standalone":
        model = ColonyModel(**params)
        for _ in range(100):
            model.step()

        agent_counts = np.zeros((model.grid.width, model.grid.height))
        for cell in model.grid.coord_iter():
            cell_content, x, y = cell
            cell_content = [x for x in cell_content if type(x) == Cat]
            agent_count = len(cell_content)
            agent_counts[x][y] = agent_count
        
        plt.imshow(agent_counts, interpolation="nearest")
        plt.colorbar()

        plt.savefig("density.png")

