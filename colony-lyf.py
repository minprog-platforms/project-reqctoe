from Agents.cats import Cat
from Agents.homes import Home, Trap
from Model.colonymodel import CatModel
import numpy as np
import matplotlib.pyplot as plt
# from Agents.cats import Cat
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Color": "red",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if type(agent) == Cat:
        portrayal["Color"] = "brown"

        if agent.hungry:
            portrayal["Color"] = "blue"

    if type(agent) == Home:
        portrayal["Shape"] = "square"

    if type(agent) == Trap:
        portrayal["Shape"] = "square"


    return portrayal


if __name__ == "__main__":
    width = 10
    height = 15
    params = {
        "cats": 15,
        "homes": 10,
        "width": width,
        "height": height,
    }
    grid = CanvasGrid(agent_portrayal, width, height, 500, round(500*height/width))

    server = ModularServer(CatModel,
                       [grid],
                       "Cat Model",
                       params)

    server.port = 8521 # The default
    server.launch()

    # model = CatModel(cats, homes, width, height)
    # for _ in range(100):
    #     model.step()

    # agent_counts = np.zeros((model.grid.width, model.grid.height))
    # for cell in model.grid.coord_iter():
    #     cell_content, x, y = cell
    #     cell_content = [x for x in cell_content if type(x) == Cat]
    #     agent_count = len(cell_content)
    #     agent_counts[x][y] = agent_count
    
    # plt.imshow(agent_counts, interpolation="nearest")
    # plt.colorbar()

    # plt.savefig("density.png")