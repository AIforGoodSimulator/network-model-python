import networkx as nx
# from scipy.stats import poisson
import itertools
from tqdm import tqdm
# from seirsplus.models import *
# import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt


def create_graph(n_structures, population, max_pop_per_struct, edge_weight):
    """ Creates a networkX graph containing all the population in the camp that is in a given structure (currently just isoboxes).
        Draws edges between people from the same isobox and returns the networkX graph and an adjacency list
    """
    # For now we will only add ethnicity as a node property, but we can expand on this
    n_ethnicities = 8

    # Graph is a networkX graph object
    g = nx.Graph()

    # Keep track of how many nodes we have put in an isobox already
    struct_count = np.zeros(shape=n_structures)

    # Store the indices of the nodes we store in each isobox in a 2D array where array[i] contains the nodes in isobox i
    nodes_per_struct = [[] for i in range(n_structures)]

    available_structs = list(range(n_structures))

    # Add the nodes to the graph
    for node in tqdm(range(population)):
        g.add_node(node)

        # Assign nodes to isoboxes randomly, until we reach the capacity of that isobox
        struct_num = np.random.choice(available_structs)

        # Assign properties to nodes
        g.nodes[node]["location"] = struct_num
        g.nodes[node]["ethnicity"] = np.random.choice(range(n_ethnicities))

        # Update number of nodes per isobox and which nodes were added to iso_num
        struct_count[struct_num] += 1
        nodes_per_struct[struct_num].append(node)

        if struct_count[struct_num] > max_pop_per_struct[struct_num]:
            available_structs.remove(struct_num)

    # Now we connect nodes inside of the same isobox
    for node_list in nodes_per_struct:
        # Use the cartesian product to get all possible edges within the nodes in an isobox
        # and only add if they are not the same node
        edge_list = [tup for tup in list(itertools.product(node_list, repeat=2)) if tup[0] != tup[1]]
        g.add_edges_from(edge_list, weight=edge_weight)

    return g, nodes_per_struct


def create_grid(width, height):
    """ Create a grid of isoboxes that resembles the isobox area of the camp, for ease of measuring proximity between nodes
        Returns a numpy array of shape (width, height) """

    iso_grid = np.zeros(shape=(width, height)).astype(int)
    iso_n = 0

    for i in range(width):
        for j in range(height):
            iso_grid[i][j] = iso_n
            iso_n += 1

    return iso_grid


def get_neighbors(grid, structure_num, proximity):
    """ Given a grid of structures, returns the closest proximity neighbors to the given structure

        params:
        - Grid: 2D numpy array
        - structure_num: int
        - proximity: int

        :returns
        - A list of neighboring structures to the current structure_num
    """

    # Get the number of columns for ease of access
    width = len(grid)
    height = len(grid[0])

    # We'll make it a set initially to avoid duplicate neighbors
    neighbors = set()

    for i in range(-proximity, proximity + 1):
        for j in range(-proximity, proximity + 1):
            if not (i == 0 and j == 0):
                x = min(max((structure_num // height) - i, 0), width - 1)
                y = min(max((structure_num % height) - j, 0), height - 1)

                if grid[x][y] != structure_num:
                    neighbors.add(grid[x][y])

    return list(neighbors)


def connect_neighbors(base_graph, n_structures, nodes_per_structure, grid, proximity, edge_weight):
    """ Draw edges in the given graph between people of neighboring structures (currently isoboxes)
        f they have the same ethnicity """

    graph = base_graph.copy()

    # For every possible structure:
    for structure in range(n_structures):

        # Given an isobox number get its neighbor isoboxes
        neighbors = get_neighbors(grid, structure, proximity)

        # For every neighbor isobox:
        for neighbor in neighbors:

            # If they share the same properties, draw an edge between them
            graph.add_edges_from([(i, j) for i in nodes_per_structure[structure] \
                                  for j in nodes_per_structure[neighbor] if
                                  graph.nodes[i]["ethnicity"] == graph.nodes[j]["ethnicity"]], weight=edge_weight)

    return graph


def connect_food_queue(base_graph, nodes_per_structure, edge_weight):
    """ Connect 1-2 people per structure (currently just isoboxes) randomly to represent that they go to the food queue
        We have 3 options:
            - Either have a range of people (2-5 per isobox) that go to food queue, same edge weights
            - Connect all people in the food queue, same edge weights
            - Connect all people in food queue with different edge weights
    """

    graph = base_graph.copy()

    food_bois = set()

    # Choose half of the people randomly from each structure
    for node_list in nodes_per_structure:
        for i in range(len(node_list) // 2):
            food_bois.add(np.random.choice(node_list))

    # This list represents the food queue
    food_bois = list(food_bois)
    np.random.shuffle(food_bois)

    # Draw an edge between everyone in the list in order, since we have already shuffled them
    for i in range(len(food_bois) - 6):
        for j in range(i + 1, i + 6):
            if not graph.has_edge(food_bois[i], food_bois[j]):
                graph.add_edge(food_bois[i], food_bois[j], weight=edge_weight)
    return graph


# Some helper functions
def min_degree(graph):
    return min(graph.degree, key=lambda kv: kv[1])[1]


def max_degree(graph):
    return max(graph.degree, key=lambda kv: kv[1])[1]
