"""
	@authors: Marcelo Sandoval-Castañeda and Daniel Firebanks-Quevedo

	Sample usage
	- To create new graphs from indices 5 to 10 and run the base model:
		python base_model_script.py 1 5 10
	- To only run the base model on graphs from 1 to 5:
		python base_model_script.py 0 1 5"""

import sys 
sys.path.append("/Users/dafirebanks/Projects/network_model_python")

import matplotlib.pyplot as plt
from seirsplus.models import *
from network_utils import *
from stats_utils import *
from intervention_utils import *
from camp_params import *
from model_params import *


# Crate n graphs and store all of them - Only create new graphs ONCE
# if new_graphs:
# 	for i in range(start_idx, start_idx + n_graphs):
# 		graph, nodes_per_struct = create_graph(n_structs, 0, n_pop, max_pop_per_struct, 
# 		                                       edge_weight=household_weight, label="household",
# 		                                       age_list=list(sample_pop["age"]),
# 		                                       sex_list = list(sample_pop["sex"]),
# 		                                       n_ethnicities=n_ethnic_groups)
# 		# Connect people from neighboring isoboxes
# 		graph = connect_neighbors(graph, 0, n_isoboxes, nodes_per_struct,
# 		                              grid_isoboxes, neighbor_proximity, neighbor_weight, 'friendship')
# 		graph = connect_neighbors(graph, dims_isoboxes[0]*dims_isoboxes[1], dims_block1[0]*dims_block1[1], nodes_per_struct,
# 		                              grid_block1, neighbor_proximity, neighbor_weight, 'friendship')
# 		graph = connect_neighbors(graph, dims_block1[0]*dims_block1[1], dims_block2[0]*dims_block2[1], nodes_per_struct,
# 		                              grid_block2, neighbor_proximity, neighbor_weight, 'friendship')
# 		graph = connect_neighbors(graph, dims_block2[0]*dims_block2[1], dims_block3[0]*dims_block3[1], nodes_per_struct,
# 		                              grid_block3, neighbor_proximity, neighbor_weight, 'friendship')

# 		save_graph(graph, nodes_per_struct, f"experiments/networks/Moria_wNeighbors_{i}")

# Load graphs and process
graph, nodes_per_struct = load_graph(f"Moria_wNeighbors")

# Base model with 1 food queue
graph = connect_food_queue(graph, nodes_per_struct, food_weight, "food")

# Initialize age based parameters because they depend on graph
PCT_ASYMPTOMATIC = get_values_per_node(ageGroup_pctAsymp, graph)
PCT_HOSPITALIZED = get_values_per_node(ageGroup_pctHospitalized, graph)
PCT_FATALITY = get_values_per_node(ageGroup_hospitalFatalityRate, graph)
ALPHA = get_values_per_node(ageGroup_susceptibility, graph)

# Model construction
model = ExtSEIRSNetworkModel(G=graph, p=P_GLOBALINTXN,
                      beta=BETA, sigma=SIGMA, lamda=LAMDA, gamma=GAMMA, 
                      gamma_asym=GAMMA, eta=ETA, gamma_H=GAMMA_H, mu_H=MU_H, 
                      a=PCT_ASYMPTOMATIC, h=PCT_HOSPITALIZED, f=PCT_FATALITY,              
                      alpha=ALPHA, beta_pairwise_mode=BETA_PAIRWISE_MODE, delta_pairwise_mode=DELTA_PAIRWISE_MODE,
                      initE=INIT_EXPOSED)

# Run model
t_steps = 200
node_states, simulation_results = run_simulation(model, t_steps)

# Model name for storage + store the model params in csv
param_combo_i = 0
fig_name = f"FinalBaseModel{param_combo_i}"
# add_model_name("experiments/model_names.csv", fig_name, household_weight, neighbor_weight, food_weight, transmission_rate, recovery_rate, progression_rate, hosp_rate, round(sum(crit_rate)/len(crit_rate), 3), death_rate, init_symp_cases, init_asymp_cases, t_steps)

# Construct results dataframe
output_df = results_to_df(simulation_results, store=True, store_name=f"experiments/results/{fig_name}.csv")

# Plot and store
fig, ax = model.figure_basic(show=False)
fig.savefig(f"experiments/plots/{fig_name}_basic.png")

fig1, ax1 = model.figure_infections(show=False)
fig1.savefig(f"experiments/plots/{fig_name}_infections.png")


