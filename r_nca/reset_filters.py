import numpy as np

np.save("weights.npy", np.zeros((5, 5, 3, 3, 3), dtype=np.float64))
np.save("intercepts.npy", np.zeros((5, 5, 3), dtype=np.float64))
