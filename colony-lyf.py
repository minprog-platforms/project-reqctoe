from agents import CatModel

if __name__ == "__main__":
    model = CatModel(15,2,3)
    for i in range(1000):
        model.step()

