import torch
from operator import mul
from functools import reduce
from scipy import stats
import numpy as np
import math

class LinearReg():

    def __init__(self, config, input_size, output_size):
        self.is_torch_model = False
        self.input_size = input_size
        self.output_size = output_size

    def __call__(self, inputs):
        y = np.array(inputs).flatten()
        slope, intercept, r, p, se = stats.linregress([k for k in range(len(y))], y)
        res = []
        for i in range(self.output_size[0]):
            predict = intercept + slope * (len(y) + i)
            predict = round(predict, 5)
            res.append(predict)


        
        return np.array(res)