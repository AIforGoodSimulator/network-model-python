import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os


AVGS = ['AvgBase', 'AvgInt']


sns.set_style("darkgrid")


files = [file for file in os.listdir('results') if '.csv' in file]

networks = []
for fname in files:
    df = pd.read_csv('results/' + fname, index_col=0)
    df['Infected'] = df['Infected_Presymptomatic']\
                     + df['Infected_Symptomatic']\
                     + df['Infected_Asymptomatic']
    df['delta_Fatalities'] = df['Fatalities'].diff()
    df.fillna(value=0, inplace=True)

    networks.append(df)

infected_nums = pd.DataFrame()
hospitalized_nums = pd.DataFrame()
fatalities_nums = pd.DataFrame()
fatalities_rates = pd.DataFrame()
summary_df = pd.DataFrame(columns=['highest_infections_day',
                                   'highest_infections',
                                   'highest_hospitalizations_day',
                                   'highest_hospitalizations',
                                   'hospital_person_days',
                                   'highest_deaths_day',
                                   'highest_deaths'])
for i in range(len(files)):
    infected_nums[files[i].split('_')[0]] = networks[i]['Infected'].values
    hospitalized_nums[files[i].split('_')[0]] = networks[i]['Hospitalized'].values
    fatalities_nums[files[i].split('_')[0]] = networks[i]['Fatalities'].values
    fatalities_rates[files[i].split('_')[0]] = networks[i]['delta_Fatalities'].values

    summary_df.loc[i] = [np.argmax(networks[i]['Infected'].values),
                         max(networks[i]['Infected']),
                         np.argmax(networks[i]['Hospitalized'].values),
                         max(networks[i]['Hospitalized']),
                         sum(networks[i]['Hospitalized'].values),
                         np.argmax(networks[i]['delta_Fatalities'].values),
                         max(networks[i]['delta_Fatalities'])]

base_graphs = []
intervention_graphs = []
for col in infected_nums.columns:
    if 'Interventions' in col:
        intervention_graphs.append(col)
    else:
        base_graphs.append(col)

infected_nums['AvgBase'] = infected_nums[base_graphs].mean(axis=1)
infected_nums['AvgInt'] = infected_nums[intervention_graphs].mean(axis=1)

hospitalized_nums['AvgBase'] = hospitalized_nums[base_graphs].mean(axis=1)
hospitalized_nums['AvgInt'] = hospitalized_nums[intervention_graphs].mean(axis=1)

fatalities_nums['AvgBase'] = fatalities_nums[base_graphs].mean(axis=1)
fatalities_nums['AvgInt'] = fatalities_nums[intervention_graphs].mean(axis=1)

fatalities_rates['AvgBase'] = fatalities_rates[base_graphs].mean(axis=1)
fatalities_rates['AvgInt'] = fatalities_rates[intervention_graphs].mean(axis=1)

plt.figure()
plt.title('Total Infected per Day')
fig1 = sns.lineplot(data=infected_nums[AVGS])
fig1.figure.savefig('plotted_results/infected_totals.png')

plt.figure()
plt.title('Total Hospitalized per Day')
fig2 = sns.lineplot(data=hospitalized_nums[AVGS])
fig2.figure.savefig('plotted_results/hospitalized_totals.png')

plt.figure()
plt.title('Total Fatalities per Day')
fig3 = sns.lineplot(data=fatalities_nums[AVGS])
fig3.figure.savefig('plotted_results/fatalities_totals.png')

plt.figure()
plt.title('New Fatalities per Day')
fig4 = sns.lineplot(data=fatalities_rates[AVGS])
fig4.figure.savefig('plotted_results/fatalities_delta.png')

summary_df.to_csv('summary.csv', index=False)
