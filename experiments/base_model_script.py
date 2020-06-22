import sys 
sys.path.append("~/Projects/network_model_python/")

import matplotlib.pyplot as plt
from seirsplus.models import *
from network_utils import *
from stats_utils import *
from intervention_utils import *
from camp_params import *


# SEIRS+ Model parameters
transmission_rate = 1.28
progression_rate = round(1/5.1, 3)
recovery_rate = 0.056 # Approx 1/18 -> Recovery occurs after 18 days
hosp_rate = round(1/11.4, 3) #1/6.3 # From Tucker Model
# crit_rate = 0.3 # From camp_params
crit_rate = list((sample_pop["death_rate"] / sample_pop["prob_symptomatic"]) / sample_pop["prob_hospitalisation"])
death_rate = 0.75

prob_global_contact = 1
prob_detected_global_contact = 1

# prob_hosp_to_critical = list(sample_pop["death_rate"]/sample_pop["prob_hospitalisation"])
prob_death = list(sample_pop["death_rate"])
prob_asymptomatic = list(1 - sample_pop["prob_symptomatic"])
prob_symp_to_hosp = list(sample_pop["prob_hospitalisation"])

init_symp_cases = 1
init_asymp_cases = 1

t_steps = 200

# Crate n graphs and store all of them
new_graphs = int(sys.argv[1])
start_idx = int(sys.argv[2])
n_graphs = int(sys.argv[3])

# Only create new graphs ONCE
if new_graphs:
	for i in range(start_idx, start_idx + n_graphs):
		household_weight = 0.98  # Edge weight for connections within each structure
		graph, nodes_per_struct = create_graph(n_structs, 0, n_pop, max_pop_per_struct, 
		                                       edge_weight=household_weight, label="household",
		                                       age_list=list(sample_pop["age"]),
		                                       sex_list = list(sample_pop["sex"]),
		                                       n_ethnicities=n_ethnic_groups)

		save_graph(graph, nodes_per_struct, f"experiments/networks/Moria_wNeighbors_{i}")

# Load graphs and process
for i in range(start_idx, start_idx + n_graphs):
	graph, nodes_per_struct = load_graph(f"experiments/networks/Moria_wNeighbors_{i}")

	# Base model with 1 food queue
	food_weight = 0.407
	graph = connect_food_queue(graph, nodes_per_struct, food_weight, "food")

	# Model construction
	model = SymptomaticSEIRSNetworkModel(G=graph, beta=transmission_rate, sigma=progression_rate, gamma=recovery_rate, 
	                                         lamda=progression_rate, mu_H=crit_rate, eta=hosp_rate, p=prob_global_contact, a=prob_asymptomatic, f=death_rate, 
	                                         h=prob_symp_to_hosp, q=prob_detected_global_contact, initI_S=init_symp_cases, initI_A=init_asymp_cases, store_Xseries=True)

	# Run model
	node_states, simulation_results = run_simulation(model, t_steps)

	# Model name for storage
	fig_name = f"BaseSympModel{i}_HW={household_weight}_NW={neighbor_weight}_FW={food_weight}_TransR={transmission_rate}_RecR={recovery_rate}_ProgR={progression_rate}_HospR={hosp_rate}_CritR={sum(crit_rate)/len(crit_rate)}_DeathR={death_rate}_initI_S={init_symp_cases}_initI_A={init_asymp_cases}_T={t_steps}"

	# Construct results dataframe
	output_df = results_to_df(simulation_results, store=True, store_name=f"experiments/results/{fig_name}.csv")

	# Plot and store
	fig, ax = model.figure_basic(show=False)#vlines=interventions.get_checkpoints()['t'])
	fig.savefig(f"experiments/plots/{fig_name}_figBasic.png")



