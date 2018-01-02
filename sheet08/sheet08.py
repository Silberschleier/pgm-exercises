import networkx as nx
import random
import numpy as np
from itertools import product
from skimage import io
import matplotlib.pyplot as plt


def cost_neighbour(x, y):
    return 1


def cost_label(label, node):
    return 1


def add_noise(img, percent):
    output = np.copy(img)
    output = np.reshape(output, (output.size, 1))

    population = random.sample(xrange(output.size), int(output.size * percent))
    for index in population:
        if output[index] == 255:
            output[index] = 0
        else:
            output[index] = 255
    return np.reshape(output, img.shape)


if __name__ == '__main__':
    # Initialize graph
    G = nx.DiGraph()
    G.add_nodes_from(['s', 't'])

    img_input = io.imread('images/a.png')
    img_noise = add_noise(img_input, 0.3)
    io.imshow(img_noise)
    plt.show()
    print(img_input.size)



