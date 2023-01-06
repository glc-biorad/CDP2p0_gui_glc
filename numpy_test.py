import numpy as np

if __name__ == '__main__':
    n_chunks = 20
    np_array = np.array([i for i in range(100)])
    print(np.array_split(np_array, n_chunks))
