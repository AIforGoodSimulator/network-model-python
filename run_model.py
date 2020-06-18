from seirsplus.models import SymptomaticSEIRSNetworkModel
from network_utils import create_node_groups,run_simulation_group
from params import ModelParams
import pickle as pkl
import pandas as pd


sample_pop = pd.read_csv('population_moria.csv')
#load the base graph
with open("Moria_graph.pkl", "rb") as f:
    graph = pkl.load(f)
node_groups=create_node_groups(graph)
Params=ModelParams('model_params.csv','population_moria.csv')
# Model construction
model = SymptomaticSEIRSNetworkModel(G=graph, beta=Params.transmission_rate, sigma=Params.progression_rate, gamma=Params.recovery_rate, 
                                         lamda=Params.progression_rate, mu_H=Params.crit_rate, eta=Params.hosp_rate, p=Params.prob_global_contact, a=Params.prob_asymptomatic, f=0.75, 
                                         h=Params.prob_symp_to_hosp, q=Params.prob_detected_global_contact, initI_S=Params.init_symp_cases, initI_A=Params.init_asymp_cases, store_Xseries=True,node_groups=node_groups)
t_steps = 200
node_states,simulation_results,timed_group_data = run_simulation_group(model, t_steps)