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
from mesa.visualization.TextVisualization import TextData
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

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
    # food alterations
    elif type(agent) == Food:
        portrayal["Color"] = "grey"
        portrayal["r"] = 0.2
    # home alterations
    elif type(agent) == Home:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    # trap alterations
    elif type(agent) == Trap:
        portrayal["Shape"] = "rect"
        portrayal["w"] = 0.7
        portrayal["h"] = 0.3
        portrayal["Color"] = "black"

    return portrayal


if __name__ == "__main__":
    runmode = "server"

    # parameters for running model
    width = 30
    height = 30
    params = {
        "cats": UserSettableParameter('number', 'Number of cats', value = 15),
        "max_cats": UserSettableParameter('number', 'Maximum number of cats', value = 2000),
        "homes": UserSettableParameter('number', 'Number of homes', value = 75),
        "traps": UserSettableParameter('slider', 'Maximum number of traps per home', value = 2, min_value = 0, max_value = 5, step = 1),
        "food": UserSettableParameter('number', 'Ammount of food in environment', value = 100) ,
        "width": width,
        "height": height,
    }

    # animated visualisation
    if runmode == "server":
        grid = CanvasGrid(agent_portrayal, width, height, 500, round(500*height/width))

        # visualization stats
        fertility_graph = ChartModule([
            {'Label': 'Fertile cats', 'Color': 'red'},
            {'Label': 'Infertile cats', 'Color': 'grey'},
            {'Label': 'Total cats', 'Color': 'green'}])
            
        population_graph = ChartModule([
            {'Label': 'Birthrate', 'Color': 'red'},
            {'Label': 'Deathrate', 'Color': 'grey'}])
        
        # initialize server
        server = ModularServer(ColonyModel,
                        [grid, 
                        fertility_graph, 
                        population_graph],
                        "Colony Model",
                        params)

        # run server
        server.port = 8521 # The default
        server.launch()
