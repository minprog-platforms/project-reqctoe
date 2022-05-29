from Agents.cats import Cat
from Agents.homes import Home, Trap
from Models.colony import ColonyModel
# import numpy as np
# import matplotlib.pyplot as plt
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    # TODO plaatjes toevoegen voor alle agents
    portrayal = {"Shape": "circle",
                 "Color": "green",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if type(agent) == Cat:
        portrayal["Color"] = "brown"

        if agent.hungry:
            portrayal["Color"] = "blue"

    if type(agent) == Home:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5

    if type(agent) == Trap:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.8
        portrayal["h"] = 0.5
        portrayal["Color"] = "black"

    return portrayal


if __name__ == "__main__":
    width = 20
    height = 25
    params = {
        "cats": 75,
        "homes": 30,
        "width": width,
        "height": height,
    }
    grid = CanvasGrid(agent_portrayal, width, height, 500, round(500*height/width))

    server = ModularServer(ColonyModel,
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