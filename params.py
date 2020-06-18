import pandas as pd

class ModelParams():
    def __init__(self,param_file,pop_file):
        params=ModelParams.read_params(param_file)
        sample_pop=ModelParams.read_params(pop_file)
        self.household_weight = params[params['Name']=='Household weight']['Value'].values[0]  # Edge weight for connections within each structure
        self.neighbor_weight = params[params['Name']=='Neighbour weight']['Value'].values[0]
        self.food_weight = params[params['Name']=='Food weight']['Value'].values[0] # Edge weight for connections in the food queue 
        
        transmission_rates=params[params['Name']=='Transmission rate']
        self.transmission_rate = transmission_rates[transmission_rates['Notes']=='Medium']['Value'].values[0]
        self.progression_rate = round(1/params[params['Name']=='Progression period']['Value'].values[0], 3)
        self.recovery_rate = 1/params[params['Name']=='Recovery period']['Value'].values[0] # Approx 1/18 -> Recovery occurs after 18 days
        self.hosp_rate = round(1/params[params['Name']=='hosp period']['Value'].values[0], 3) #1/6.3 # From Tucker Model
        # crit_rate = 0.3 # From camp_params
        self.crit_rate = list((sample_pop["death_rate"] / sample_pop["prob_symptomatic"]) / sample_pop["prob_hospitalisation"])
        self.death_rate = params[params['Name']=='death rate']['Value'].values[0]


        self.prob_global_contact = params[params['Name']=='probability of global contact']['Value'].values[0]
        self.prob_detected_global_contact = params[params['Name']=='probability of detecting global contact']['Value'].values[0]

        # prob_hosp_to_critical = list(sample_pop["death_rate"]/sample_pop["prob_hospitalisation"])
        self.prob_death = list(sample_pop["death_rate"])
        self.prob_asymptomatic = list(1 - sample_pop["prob_symptomatic"])
        self.prob_symp_to_hosp = list(sample_pop["prob_hospitalisation"])

        self.init_symp_cases = params[params['Name']=='initial symptomatic cases']['Value'].values[0]
        self.init_asymp_cases = params[params['Name']=='initial asymptomatic cases']['Value'].values[0]
    @staticmethod
    def read_params(csv_file):
        return pd.read_csv(csv_file)