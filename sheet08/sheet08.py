import networkx as nx
import random
import numpy as np
from skimage import io
from itertools import product
import matplotlib.pyplot as plt

WHITE = 255
BLACK = 0
LABEL_COST = 1


def add_noise(img, percent):
    output = np.copy(img)
    output = np.reshape(output, (output.size, 1))

    population = random.sample(range(output.size), int(output.size * percent))
    for index in population:
        if output[index] == WHITE:
            output[index] = BLACK
        else:
            output[index] = WHITE
    return np.reshape(output, img.shape)


def add_neighbourhood_edges(G, img, x, y):
    # Four-neighbourhood
    neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    # Eight-neighbourhood
    #neighbours.extend([(x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)])

    for xn, yn in neighbours:
        # Skip neighbours outside of the image
        if xn < 0 or yn < 0 or xn > img.shape[0]-1 or yn > img.shape[1]-1:
            continue

        cost_lambda = 1 if img[x, y] == img[xn, yn] else 0
        G.add_edge((x, y), (xn, yn), capacity=cost_lambda)


def graph_cut_denoise(img):
    # Initialize graph
    G = nx.DiGraph()
    G.add_nodes_from(['s', 't'])

    # Construct the graph
    for x, y in product(range(img.shape[0]), range(img.shape[1])):
        add_neighbourhood_edges(G, img, x, y)
        if img[x, y] == WHITE:
            G.add_edge((x, y), 't', capacity=LABEL_COST)
        else:
            G.add_edge('s', (x, y), capacity=LABEL_COST)

    print('Nodes: {}, Edges: {}'.format(G.number_of_nodes(), G.number_of_edges()))
    value, partition = nx.minimum_cut(G, 's', 't')
    print(value)
    print(partition[0])
    print(partition[1])


if __name__ == '__main__':
    img_input = io.imread('images/a.png')
    io.imshow(img_input)
    plt.show()

    img_noise = add_noise(img_input, 0.1)
    io.imshow(img_noise)
    plt.show()

    graph_cut_denoise(img_noise)



