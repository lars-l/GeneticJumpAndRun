#!python
#cython: language_level=3, boundscheck=False, wraparound=False, optimize.unpack_method_calls = True




import numpy as np
import system_settings as settings
from system_settings import INPUT_NEURONS, HIDDEN_NEURONS, OUTPUT_NEURONS, HIDDEN_NEURONS_2, SEGMENT_NEURONS, SEG_AMOUNT, META_NEURONS
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cdef class NeuralNetwork:

    cdef public np.ndarray biases0, biases1, biases2
    cdef public np.ndarray weights0, weights1, weights2


    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self.biases0 = 50 * np.random.randn(HIDDEN_NEURONS-META_NEURONS, 1)
        self.biases1 = 50 * np.random.randn(HIDDEN_NEURONS_2, 1)
        self.biases2 = 50 * np.random.randn(OUTPUT_NEURONS, 1)


        self.weights0 = 50 * np.random.randn(HIDDEN_NEURONS-META_NEURONS, SEGMENT_NEURONS)
        self.weights1 = 50 * np.random.randn(HIDDEN_NEURONS_2, HIDDEN_NEURONS)
        self.weights2 = 50 * np.random.randn(OUTPUT_NEURONS, HIDDEN_NEURONS_2)


    @cython.boundscheck(False) # turn off bounds-checking for entire function
    @cython.wraparound(False)  # turn off negative index wrapping for entire function
    cpdef bint calculate_output_neurons(self, segment_neurons, meta_neurons):
        cdef np.ndarray a = np.ndarray(shape=(SEGMENT_NEURONS, 1), dtype=float, buffer=np.array(segment_neurons))
        cdef np.ndarray b = np.ndarray(shape=(META_NEURONS, 1), dtype=float, buffer=np.array(meta_neurons))

        a = relu(np.dot(self.weights0, a) + self.biases0)
        a = np.append(a, b)
        a = relu(np.dot(self.weights1, a) + self.biases1)
        a = relu(np.dot(self.weights2, a) + self.biases2)
        return a[0][0] >= 3

def relu(x):
    return np.maximum(x, 0)