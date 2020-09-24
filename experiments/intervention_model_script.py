"""
	@authors: Marcelo Sandoval-Castañeda and Daniel Firebanks-Quevedo

	Sample usage:
		- To run the interventions model with one food queue for graphs 1-5:
			python experiments/food_queues_script.py 0 1 5"""

import sys 
sys.path.append("/Users/dafirebanks/Projects/network_model_python")

import matplotlib.pyplot as plt
from seirsplus.models import *
from network_utils import *
from stats_utils import *
from intervention_utils import *
from camp_params import *
from model_params import *

# Load graphs and process
graph, nodes_per_struct = load_graph(f"Moria_wNeighbors")

# Base model with 1 food queue
graph = connect_food_queue(graph, nodes_per_struct, food_weight, "food")

# Initialize age based parameters because they depend on graph
PCT_ASYMPTOMATIC = get_values_per_node(ageGroup_pctAsymp, graph)
PCT_HOSPITALIZED = get_values_per_node(ageGroup_pctHospitalized, graph)
PCT_FATALITY = get_values_per_node(ageGroup_hospitalFatalityRate, graph)
ALPHA = get_values_per_node(ageGroup_susceptibility, graph)

# Base model with 1 food queue
food_weight = 0.407
graph = connect_food_queue(graph, nodes_per_struct, food_weight, "food")

# Create quarantine graph - This also includes neighbor/friendship edges
quarantine_graph = remove_edges_from_graph(graph, scale=2, edge_label_list=["food", "friendship"], min_num_edges=2)

# Create interventions
interventions = Interventions()


# Simulate quarantine + masks
q_start = 30
interventions.add(quarantine_graph, q_start, beta=BETA_Q)

# Simulate HALT of quarantine but people still have to wear masks
q_end = 100
interventions.add(graph, q_end, beta=BETA_Q)

# Simulate HALT of wearing masks
m_end = 150
interventions.add(graph, m_end, beta=BETA)

checkpoints = interventions.get_checkpoints()


# Iterate through the tweakable parameters
param_combo_i = 0

# Model construction
model = ExtSEIRSNetworkModel(G=graph, p=P_GLOBALINTXN, q=Q_GLOBALINTXN,
                      beta=BETA, sigma=SIGMA, lamda=LAMDA, gamma=GAMMA, 
                      gamma_asym=GAMMA, eta=ETA, gamma_H=GAMMA_H, mu_H=MU_H, 
                      a=PCT_ASYMPTOMATIC, h=PCT_HOSPITALIZED, f=PCT_FATALITY,              
                      alpha=ALPHA, beta_pairwise_mode=BETA_PAIRWISE_MODE, delta_pairwise_mode=DELTA_PAIRWISE_MODE,
                      initE=INIT_EXPOSED)
# Run model
t_steps = 200
node_states, simulation_results = run_simulation(model, t_steps, checkpoints=checkpoints)

# Model name for storage + store the model params in csv
fig_name = f"InterventionsBaseModel{param_combo_i}"
# add_model_name("experiments/model_names.csv", fig_name, household_weight, neighbor_weight, food_weight, transmission_rate, recovery_rate, progression_rate, hosp_rate, round(sum(crit_rate)/len(crit_rate), 3), death_rate, init_symp_cases, init_asymp_cases, t_steps, f"{q_start}-{q_end}", reduction_percentage, f"{q_start}-{m_end}")

# Construct results dataframe
output_df = results_to_df(simulation_results, store=True, store_name=f"experiments/results/{fig_name}.csv")

# Plot and store
fig, ax = model.figure_basic(show=False)
fig.savefig(f"experiments/plots/{fig_name}_basic.png")

fig1, ax1 = model.figure_infections(show=False)
fig1.savefig(f"experiments/plots/{fig_name}_infections.png")


