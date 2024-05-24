import torch
from operator import mul
from functools import reduce


class FeedForwardModel(torch.nn.Module):

    def __init__(self, config, input_size, output_size):
        super(FeedForwardModel, self).__init__()
        self.is_torch_model = True
        self.input_size = input_size
        self.output_size = output_size
        self.nb_hidden_layers = config["nb_hidden_layers"]
        self.hidden_layer_size = config["hidden_layer_size"]
        self.activation_name = config["activation"]
        self.dropout = (config["dropout"] if config["dropout"] != 0 else None)

        # Define the model
        self.input_layer = torch.nn.Linear(reduce(mul, input_size, 1), self.hidden_layer_size)
        self.activation = eval(f"torch.nn.{self.activation_name}()")
        self.output_layer = torch.nn.Linear(self.hidden_layer_size, output_size[1])
        self.hidden_layer = torch.nn.Linear(self.hidden_layer_size, self.hidden_layer_size)
        self.dropout_layer = torch.nn.Dropout(self.dropout)

    def forward(self, x):
        x = (torch.flatten(x) if len(x.shape) == 2 else torch.flatten(x, 1))
        x = self.input_layer(x)
        for _ in range(self.nb_hidden_layers):
            x = self.activation(x)
            if(self.dropout):
                x = self.dropout_layer(x)
            x = self.hidden_layer(x)
        x = self.activation(x)
        x = self.output_layer(x)
        return x