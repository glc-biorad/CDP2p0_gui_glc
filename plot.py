import matplotlib.pyplot as plt
import numpy as np

data = np.array([92,92, 55,55, 84,84])
#data = np.array([92,92,(92+55)/2., 55,55, (84+55)/2., 84,84])
plt.plot(data)
plt.show()
