import torch
from operator import mul
from functools import reduce


class DummyModel(torch.nn.Module):

    def __init__(self, config, input_size, output_size):
        super(DummyModel, self).__init__()
        self.is_torch_model = True
        self.input_size = input_size
        self.output_size = output_size

        # Define the model
        self.input_layer = torch.nn.Linear(reduce(mul, input_size, 1), 200)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(200, output_size[1])

        self.model = torch.nn.Sequential(
            self.input_layer,
            self.activation,
            self.linear2,
        )

    def forward(self, x):
        x = (torch.flatten(x) if len(x.shape) == 2 else torch.flatten(x, 1))
        x = self.model(x)


        
        return x