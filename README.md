# Network Model for COVID-19 in Moria
By Marcelo Sandoval-Castaneda and Daniel Firebanks-Quevedo. Built using NetworkX and SEIRS+ in Python.

## The Network
A network is designed using NetworkX to represent social and day-to-day interactions in the Moria refugee camp in Lesbos, Greece. Isoboxes to represent houses inside the camp are constructed in a grid of 29 * 28, to which each of the camp inhabitants is assigned to at random, where each isobox contains a maximum of **Poisson(λ=10)** inhabitants. Each inhabitant is represented by a node, that contains the data for the isobox they live in, their ethnicity, thier age, and their gender.

Connections are built using the following rules (from Tucker's paper):
- Connections between inhabitants in the same isobox are assigned with an edge weight of 0.98.
- Connections between inhabitants that live near one another, and are of the same ethnicity, are assigned with an edge weight of 0.017, what we like to call *friendship edges*.
- Lastly, connections regarding the food queue are assigned simulating a FCFS queue, where an individual comes in contact with the five people directly in front of them and the five people directly behind them. These edges are given a weight of 0.407.

Most intervention representations deal with manipulating these edges, whether it is by reducing their weights or by deleting them altogether.

## The Epidemic
As for the simulation of the epidemic, this is done using the SEIRS+ model. Our initial network is assigned to the model, after which arbitrarily many different graphs can be assigned to it, allowing us to perform different food queues everyday, or different interventions depending on the time.

Our key parameters are the following:

Variable | Symbol | Value | Source
:---:|:---:|:---:|:---:
Rate of Transmission | β | 1.28 | [López and Rodó](https://www.medrxiv.org/content/10.1101/2020.03.27.20045005v3.full.pdf)
Mean Incubation Period | 1/σ | 5.1 | [Lauer et al.](https://www.acpjournals.org/doi/10.7326/M20-0504)
Mean Infectious Period | 1/γ | 17.85 | [Citation Needed]
Initial Infected Population | I₀ | 10 | 

## Preliminary Results
Running this simulation with only the people that live in the houses (around 8100 people), the results we have found from the SEIRS+ model are the following:

![Image not found.](plots/Infections_IsoWeight=1_NeighWeight=0.5_FoodWeight=0.2_Beta=1.28_Gamma=0.056_Sigma=0.87_initI=10_figBasic.png)

## Todo List
- Get as specific as possible with the interventions that are possible to model.
- Convert our notebooks into executable Python files.
- Restructure the repo for organization's sake.

## Launch Jupyter Notebooks for Data Science in Docker
```
docker run -p 8888:8888 -p 4040:4040 -v $(PWD):/home/jovyan/work --name seirs-covid jupyter/datascience-notebook
```
