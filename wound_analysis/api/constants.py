import numpy as np

AREA_UPPER_LIMIT = 0.675
AREA_LOWER_LIMIT = 0.005

A_LR = [np.array([0, 75, 180]), np.array([168, 75, 180])]
A_UR = [np.array([12, 255, 200]), np.array([180, 255, 200])]

B_LR = [np.array([0, 95, 140]), np.array([168, 95, 140])]
B_UR = [np.array([12, 255, 197]), np.array([180, 255, 197])]

C_LR = [np.array([0, 100, 140]), np.array([168, 100, 140])]
C_UR = [np.array([12, 255, 177]), np.array([180, 255, 177])]

D_LR = [np.array([0, 105, 140]), np.array([168, 105, 140])]
D_UR = [np.array([12, 255, 167]), np.array([180, 255, 167])]

E_LR = [np.array([0, 110, 50]), np.array([168, 110, 50])]
E_UR = [np.array([12, 255, 153]), np.array([180, 255, 153])]

F_LR = [np.array([0, 110, 50]), np.array([168, 110, 50])]
F_UR = [np.array([12, 255, 140]), np.array([180, 255, 140])]

ORIG_LOWER_RANGE = [np.array([0, 30, 30]), np.array([130, 30, 30])]
ORIG_UPPER_RANGE = [np.array([40, 255, 255]), np.array([180, 255, 255])]


DEF_LOWER_RANGE = C_LR
DEF_UPPER_RANGE = C_UR

SAT_STEP_1 = 1
SAT_STEP_2 = 4
SAT_STEP_3 = 9

VAL_STEP_1 = 1
VAL_STEP_2 = 4
VAL_STEP_3 = 9

