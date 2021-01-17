import numpy as np

AREA_UPPER_LIMIT = 0.675
AREA_LOWER_LIMIT = 0.005

A_LR = [np.array([0, 75, 70]), np.array([160, 75, 70])]
A_UR = [np.array([20, 255, 200]), np.array([180, 255, 200])]

B_LR = [np.array([0, 95, 30]), np.array([150, 95, 30])]
B_UR = [np.array([30, 255, 197]), np.array([180, 255, 197])]

C_LR = [np.array([0, 100, 20]), np.array([150, 100, 20])]
C_UR = [np.array([30, 255, 177]), np.array([180, 255, 177])]

D_LR = [np.array([0, 105, 20]), np.array([150, 105, 20])]
D_UR = [np.array([30, 255, 167]), np.array([180, 255, 167])]

E_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
E_UR = [np.array([30, 255, 153]), np.array([180, 255, 153])]

F_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
F_UR = [np.array([30, 255, 140]), np.array([180, 255, 140])]

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

