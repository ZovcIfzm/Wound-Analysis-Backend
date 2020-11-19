import numpy as np

AREA_UPPER_LIMIT = 0.375
AREA_LOWER_LIMIT = 0.025

A_LR = [np.array([0, 45, 40]), np.array([140, 45, 40])]
A_UR = [np.array([40, 255, 185]), np.array([180, 255, 185])]

B_LR = [np.array([0, 75, 40]), np.array([150, 75, 40])]
B_UR = [np.array([30, 240, 177]), np.array([180, 240, 177])]

C_LR = [np.array([0, 100, 40]), np.array([150, 100, 40])]
C_UR = [np.array([30, 240, 177]), np.array([180, 240, 177])]

D_LR = [np.array([0, 105, 40]), np.array([150, 105, 40])]
D_UR = [np.array([30, 240, 155]), np.array([180, 240, 155])]

E_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
E_UR = [np.array([30, 255, 150]), np.array([180, 255, 150])]

F_LR = [np.array([0, 110, 0]), np.array([150, 110, 0])]
F_UR = [np.array([30, 255, 120]), np.array([180, 255, 120])]

ORIG_LOWER_RANGE = [np.array([0, 30, 30]), np.array([130, 30, 30])]
ORIG_UPPER_RANGE = [np.array([40, 255, 255]), np.array([180, 255, 255])]


DEF_LOWER_RANGE = B_LR
DEF_UPPER_RANGE = B_UR