import torch
from operator import mul
from functools import reduce
from .torch_model import TorchModel


class DummyModel(TorchModel):

    def __init__(self, config, input_size, output_size):
        super(DummyModel, self).__init__(input_size, output_size)
        self.input_size = input_size
        self.output_size = output_size
        self.linear1 = torch.nn.Linear(reduce(mul, input_size, 1), 200)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(200, 10)
        self.softmax = torch.nn.Softmax(dim = output_size[0])

    def forward(self, x):
        x = (torch.flatten(x) if len(x.shape) == 2 else torch.flatten(x, 1))
        x = self.linear1(x)
        x = self.activation(x)
        x = self.linear2(x)
        x = self.softmax(x)
        
        return x