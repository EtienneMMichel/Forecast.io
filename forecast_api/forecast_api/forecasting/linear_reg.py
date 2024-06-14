from scipy import stats, odr
import numpy as np

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
    

class PolyReg():

    def __init__(self, config, input_size, output_size):
        self.is_torch_model = False
        self.input_size = input_size
        self.output_size = output_size
        self.order = 3

    def __call__(self, inputs):
        y = np.array(inputs).flatten()
        x = [k for k in range(len(y))]
        poly_model = odr.polynomial(self.order)  # using third order polynomial model
        data = odr.Data(x, y)
        odr_obj = odr.ODR(data, poly_model)
        output = odr_obj.run()  # running ODR fitting
        poly = np.poly1d(output.beta[::-1])
        res = poly([k for k in range(len(y), len(y) + self.output_size[0])])
        return np.array(res)