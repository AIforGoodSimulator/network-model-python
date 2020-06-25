import sys 
sys.path.append("/Users/dafirebanks/Projects/network_model_python/")

import matplotlib.pyplot as plt
from seirsplus.models import *
from network_utils import *
from stats_utils import *
from intervention_utils import *
from camp_params import *

if not sys.argv[1]:
	print("Must enter start_idx and number of graphs to load")
	sys.exit(1)

# Crate n graphs and store all of them
start_idx = int(sys.argv[1])
n_graphs = int(sys.argv[2])

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

# Load graphs and process
for i in range(start_idx, start_idx + n_graphs):
	base_graph, nodes_per_struct = load_graph(f"experiments/networks/Moria_wNeighbors_{i}")

	for food_queue_number in [1, 2, 4]:
		
		# Base model with 1 food queue
		food_weight = 0.407
		graph = create_multiple_food_queues(base_graph, food_queue_number, food_weight, nodes_per_struct, [grid_isoboxes, grid_block1, grid_block2, grid_block3])

		# Create quarantine graph - This also includes neighbor/friendship edges
		quarantine_graph = remove_edges_from_graph(graph, scale=2, edge_label_list=["food", "friendship"], min_num_edges=2)

		# Create interventions
		interventions = Interventions()

		# Amount by which wearing masks reduces the transmission rate
		reduction_percentage = 0.3

		# Simulate quarantine + masks
		q_start = 0
		interventions.add(quarantine_graph, q_start, beta=transmission_rate*reduction_percentage)

		# Simulate HALT of quarantine but people still have to wear masks
		q_end = 150
		interventions.add(graph, q_end, beta=transmission_rate*reduction_percentage)

		# Simulate HALT of wearing masks
		m_end = 200
		interventions.add(graph, m_end, beta=transmission_rate)

		checkpoints = interventions.get_checkpoints()

		# Model construction
		model = SymptomaticSEIRSNetworkModel(G=graph, Q=quarantine_graph, beta=transmission_rate, sigma=progression_rate, gamma=recovery_rate, 
		                                         lamda=progression_rate, mu_H=crit_rate, eta=hosp_rate, p=prob_global_contact, a=prob_asymptomatic, f=death_rate, 
		                                         h=prob_symp_to_hosp, q=prob_detected_global_contact, initI_S=init_symp_cases, initI_A=init_asymp_cases, store_Xseries=True)

		# Run model
		node_states, simulation_results = run_simulation(model, t_steps, checkpoints)

		# Model name for storage
		fig_name = f"InterventionsMultFQ{food_queue_number}_Model{i}_HW={household_weight}_NW={neighbor_weight}_FW={food_weight}_TransR={transmission_rate}_RecR={recovery_rate}_ProgR={progression_rate}_HospR={hosp_rate}_CritR={round(sum(crit_rate)/len(crit_rate), 3)}_DeathR={death_rate}_initI_S={init_symp_cases}_initI_A={init_asymp_cases}_T={t_steps}"
		intervention_deets = f"Qtime={q_start}-{q_end}_Qred={reduction_percentage}_Htime={q_start}-{m_end}"

		# Construct results dataframe
		output_df = results_to_df(simulation_results, store=True, store_name=f"experiments/results/{fig_name}_{intervention_deets}.csv")

		# Plot and store
		fig, ax = model.figure_basic(show=False)#vlines=interventions.get_checkpoints()['t'])
		fig.savefig(f"experiments/plots/{fig_name}_{intervention_deets}_fig.png")



