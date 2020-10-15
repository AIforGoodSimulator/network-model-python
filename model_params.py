from seirsplus.utilities import *
from network_utils import *
from camp_params import *

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# BASELINE PROFILE
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Distribution based parameters
latentPeriod_mean, latentPeriod_coeffvar = 4.0, 0.6
presymptomaticPeriod_mean, presymptomaticPeriod_coeffvar = 2.2, 0.5
symptomaticPeriod_mean, symptomaticPeriod_coeffvar = 4.0, 0.4
onsetToHospitalizationPeriod_mean, onsetToHospitalizationPeriod_coeffvar = 11.0, 0.45
hospitalizationToDischargePeriod_mean, hospitalizationToDischargePeriod_coeffvar = 8.0, 0.45
hospitalizationToDeathPeriod_mean, hospitalizationToDeathPeriod_coeffvar = 10.0, 0.45
R0_mean     = 2.5
R0_coeffvar = 0.2

SIGMA   = 1 / gamma_dist(latentPeriod_mean, latentPeriod_coeffvar, n_pop)
LAMDA   = 1 / gamma_dist(presymptomaticPeriod_mean, presymptomaticPeriod_coeffvar, n_pop)
GAMMA   = 1 / gamma_dist(symptomaticPeriod_mean, symptomaticPeriod_coeffvar, n_pop)
ETA     = 1 / gamma_dist(onsetToHospitalizationPeriod_mean, onsetToHospitalizationPeriod_coeffvar, n_pop)
GAMMA_H = 1 / gamma_dist(hospitalizationToDischargePeriod_mean, hospitalizationToDischargePeriod_coeffvar, n_pop)
MU_H    = 1 / gamma_dist(hospitalizationToDeathPeriod_mean, hospitalizationToDeathPeriod_coeffvar, n_pop)
R0 = gamma_dist(R0_mean, R0_coeffvar, n_pop)

infectiousPeriod = 1/LAMDA + 1/GAMMA
BETA = 1/infectiousPeriod * R0
BETA_PAIRWISE_MODE  = 'infected'
DELTA_PAIRWISE_MODE = 'mean'

# Constant parameters
P_GLOBALINTXN = 0.8
INIT_EXPOSED = int(n_pop / 100)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# REDUCED INTERACTIONS PROFILE ADDITIONS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
reduction_rate = 0.3
BETA_Q = BETA * (reduction_rate/R0_mean)
Q_GLOBALINTXN = 0.2


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# AGE BASED PARAMETERS
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ageGroup_pctAsymp = {'0-9':0.6,
                            '10-19':    0.75,
                            '20-29':    0.63,
                            '30-39':    0.58,
                            '40-49':    0.49,
                            '50-59':    0.41,
                            '60-69':    0.28,
                            '70+':    0.24}

ageGroup_pctHospitalized = {'0-9':      0.0076,
                            '10-19':    0.0081,
                            '20-29':    0.0099,
                            '30-39':    0.0185,
                            '40-49':    0.0543,
                            '50-59':    0.1505,
                            '60-69':    0.3329,
                            '70+':    0.6176}

ageGroup_hospitalFatalityRate = {'0-9':     0.0000,
                                 '10-19':   0.3627,
                                 '20-29':   0.0577,
                                 '30-39':   0.0426,
                                 '40-49':   0.0694,
                                 '50-59':   0.1532,
                                 '60-69':   0.3381,
                                 '70-79':   0.5187,
                                 '80+':     0.7283 }
ageGroup_susceptibility = {"0+": 1.0}








