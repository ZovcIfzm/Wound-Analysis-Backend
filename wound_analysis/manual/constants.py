import numpy as np

AREA_UPPER_LIMIT = 0.475
AREA_LOWER_LIMIT = 0.025

A_LR = [np.array([0, 45, 20]), np.array([140, 45, 20])]
A_UR = [np.array([40, 255, 185]), np.array([180, 255, 185])]

B_LR = [np.array([0, 75, 20]), np.array([150, 75, 20])]
B_UR = [np.array([30, 255, 177]), np.array([180, 255, 177])]

C_LR = [np.array([0, 100, 20]), np.array([150, 100, 20])]
C_UR = [np.array([30, 255, 177]), np.array([180, 255, 177])]

D_LR = [np.array([0, 105, 20]), np.array([150, 105, 20])]
D_UR = [np.array([30, 255, 155]), np.array([180, 255, 155])]

E_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
E_UR = [np.array([30, 255, 150]), np.array([180, 255, 150])]

F_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
F_UR = [np.array([30, 255, 120]), np.array([180, 255, 120])]

ORIG_LOWER_RANGE = [np.array([0, 30, 30]), np.array([130, 30, 30])]
ORIG_UPPER_RANGE = [np.array([40, 255, 255]), np.array([180, 255, 255])]


DEF_LOWER_RANGE = B_LR
DEF_UPPER_RANGE = B_UR