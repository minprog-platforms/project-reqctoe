from Model.colonymodel import CatModel
import numpy as np

if __name__ == "__main__":
    cats = 15
    homes = 1
    width = 10
    height = 15

    model = CatModel(cats, homes, width, height)
    for _ in range(1000):
        model.step()

    agent_counts = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y = cell
        agent_count = len(cell_content)
        agent_counts[x][y] = agent_count
    plt.imshow(agent_counts, interpolation="nearest")
    plt.colorbar()

    plt.save_fig()