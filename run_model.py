from seirsplus.models import SymptomaticSEIRSNetworkModel
from network_utils import load_graph,create_node_groups,run_simulation_group,results_to_df_group,connect_food_queue
from params import ModelParams
import pickle as pkl
import pandas as pd
import dask
from dask.diagnostics import ProgressBar
import os

#TODO: run the same baseline experiment with the same parameters 10+ times to average out
def run_baseline(num_iterations=10,n_processes=os.cpu_count()):
    #load the base graph
    lazy_sols=[]
    graph, nodes_per_struct = load_graph("Moria_wNeighbors")
    food_weight = 0.407
    graph_1fq = connect_food_queue(graph, nodes_per_struct, food_weight, "food")
    node_groups=create_node_groups(graph_1fq)
    Params=ModelParams('model_params.csv','population_moria.csv')
    # Model construction
    for i in range(num_iterations):
        model = SymptomaticSEIRSNetworkModel(G=graph_1fq, beta=Params.transmission_rate, sigma=Params.progression_rate, gamma=Params.recovery_rate, 
                                               lamda=Params.progression_rate, mu_H=Params.crit_rate, eta=Params.hosp_rate, p=Params.prob_global_contact,a=Params.prob_asymptomatic, f=0.75, 
                                               h=Params.prob_symp_to_hosp, q=Params.prob_detected_global_contact, initI_S=Params.init_symp_cases, initI_A=Params.init_asymp_cases, store_Xseries=True,node_groups=node_groups)
        lazy_result = dask.delayed(run_simulation_group)(model,20)
        lazy_sols.append(lazy_result)
    with dask.config.set(scheduler='processes', n_processes=n_processes):
        with ProgressBar():
            sols = dask.compute(*lazy_sols)
    for i in range(num_iterations):
        simulation_results=sols[i]
        simulation_results['Run']=[i]*len(simulation_results)
        output_df = results_to_df_group(simulation_results,store=True,store_name=f"baseline_{i}.csv")
    return None

if __name__ == '__main__':
    run_baseline()

