import numpy as np
import pandas as pd


# Death rate per age calculation - parameters found by fitting a sigmoid curve
A_MALES = -9.58814632
B_MALES = 0.61453804
A_FEMALES = -9.91023535
B_FEMALES = 0.47451181


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def deathrate_male(x):
    return sigmoid(np.sqrt(x) + A_MALES) * B_MALES


def deathrate_female(x):
    return sigmoid(np.sqrt(x) + A_FEMALES) * B_FEMALES


def get_deathrate(row):
    if row["sex"] == 0:
        return deathrate_male(row["age"])

    else:
        return deathrate_female(row["age"])


def sympt_prob(x):
    return 0.41731169 + -1.38217963e-02*x**1 + 5.19931131e-04*x**2 + -3.66388844e-06*x**3


def get_prob_symptomatic(row):
    if row["age"] > 79:
        return sympt_prob(79)
    return sympt_prob(row["age"])


def sample_population(n_sample):
    # Dataframe including age (V1) and sex (V2)
    pop_df = pd.read_csv('data/age_and_sex.csv')
    pop_df = pop_df[["V1", "V2"]].rename(columns={"V1": "age", "V2": "sex"})

    # Sample only the number of people in isoboxes (n_samples)
    pop_df['death_rate'] = pop_df.apply(lambda row: get_deathrate(row), axis=1)
    pop_df['prob_symptomatic'] = pop_df.apply(lambda row: get_prob_symptomatic(row), axis=1)
    sample = pop_df.sample(n=n_sample, random_state=69420)
    # print(sample['death_rate'].values.shape)

    return sample
