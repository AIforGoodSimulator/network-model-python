from network_utils import *
from stats_utils import sample_population
from scipy.stats import poisson


def create_moria():

    # ===================== Camp parameters ==========================
    n_pop = 18700

    # Grid info for isoboxes
    dims_isoboxes = (29, 28)  # 812

    # Grid info for tents
    dims_block1 = (20, 67)  # 1340
    dims_block2 = (53, 15)  # 795
    dims_block3 = (19, 28)  # 532

    # Isoboxes
    pop_isoboxes = 8100
    pop_per_isobox = 10
    n_isoboxes = dims_isoboxes[0] * dims_isoboxes[1]

    # Tents
    n_tents = 2650
    pop_tents = 10600
    pop_per_tent = 4

    # Others
    n_bathrooms = 144
    n_ethnic_groups = 8

    # We define neighboring structures within a range of 2 in the structure grid
    proximity = 2

    # Define the maximum population per structures (tents and isoboxes) drawn from a poisson distribution
    max_pop_per_struct = list(poisson.rvs(mu=pop_per_isobox, size=n_isoboxes))
    max_pop_per_struct = max_pop_per_struct + list(poisson.rvs(mu=pop_per_tent, size=dims_block1[0] * dims_block1[1]))
    max_pop_per_struct = max_pop_per_struct + list(poisson.rvs(mu=pop_per_tent, size=dims_block2[0] * dims_block2[1]))
    max_pop_per_struct = max_pop_per_struct + list(poisson.rvs(mu=pop_per_tent, size=dims_block3[0] * dims_block3[1]))

    n_structs = len(max_pop_per_struct)

    # Sample the population age, and parameter rates
    sample_pop = sample_population(n_pop, "data/augmented_population.csv")

    # ===================== 1. Create basic network with tents and isoboxes ===========================================
    household_weight = 0.98  # Edge weight for connections within each structure
    graph, nodes_per_struct = create_graph(n_structs, 0, n_pop, max_pop_per_struct,
                                           edge_weight=household_weight, label="household",
                                           age_list=list(sample_pop["age"]),
                                           sex_list=list(sample_pop["sex"]),
                                           n_ethnicities=n_ethnic_groups)

    # ======== 2. Create the grids that will help with positioning when measuring proximity ===========================
    # We will create 4 different grids: 1 for the isobox area and 3 for the big tent blocks
    grid_isoboxes = create_grid(dims_isoboxes[0], dims_isoboxes[1], 0)
    grid_block1 = create_grid(dims_block1[0], dims_block1[1], grid_isoboxes[-1][-1] + 1)
    grid_block2 = create_grid(dims_block2[0], dims_block2[1], grid_block1[-1][-1] + 1)
    grid_block3 = create_grid(dims_block3[0], dims_block3[1], grid_block2[-1][-1] + 1)

    # ========== 3. Connect the nodes that are within a certain degree of proximity ===================================
    # We call the `connect_neighbors` method 4 times because we are connecting nodes within the isobox grid,
    # and within the 3 other tent block grids
    neighbor_weight = 0.017
    graph = connect_neighbors(graph, 0, n_isoboxes, nodes_per_struct,
                              grid_isoboxes, 2, neighbor_weight, 'friendship')
    graph = connect_neighbors(graph, dims_isoboxes[0] * dims_isoboxes[1], dims_block1[0] * dims_block1[1],
                              nodes_per_struct,
                              grid_block1, 2, neighbor_weight, 'friendship')
    graph = connect_neighbors(graph, dims_block1[0] * dims_block1[1], dims_block2[0] * dims_block2[1], nodes_per_struct,
                              grid_block2, 2, neighbor_weight, 'friendship')
    graph = connect_neighbors(graph, dims_block2[0] * dims_block2[1], dims_block3[0] * dims_block3[1], nodes_per_struct,
                              grid_block3, 2, neighbor_weight, 'friendship')

    # ===================== 4. Connect the nodes that go to the food line =============================================
    # Assumption: 2 people from each structure are randomly selected to get food,
    # and then we connect each person from the food queue with the previous + next 5 people near them.
    food_weight = 0.407  # Edge weight for connections in the food queue
    graph = connect_food_queue(graph, nodes_per_struct, food_weight, "food")

    # ===================== 5. Create node groups of 10 year age bucket to track the results ==========================
    node_groups = create_node_groups(graph)

    return graph, node_groups
