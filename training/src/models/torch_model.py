import torch
from operator import mul
from functools import reduce
import tqdm

class TorchModel(torch.nn.Module):
    def __init__(self, input_size, output_size):
        super(TorchModel, self).__init__()
        self.input_size = input_size
        self.output_size = output_size


    def forward(self, x):
        raise NotImplementedError("forward method must be implemented in the child class")
    
    def train_(self, loader, f_loss, optimizer, device, dynamic_display=True):
        """
        Train a model for one epoch, iterating over the loader
        using the f_loss to compute the loss and the optimizer
        to update the parameters of the model.
        Arguments :
        model     -- A torch.nn.Module object
        loader    -- A torch.utils.data.DataLoader
        f_loss    -- The loss function, i.e. a loss Module
        optimizer -- A torch.optim.Optimzer object
        device    -- A torch.device
        Returns :
        The averaged train metrics computed over a sliding window
        """

        # We enter train mode.
        # This is important for layers such as dropout, batchnorm, ...
        self.train()

        total_loss = 0
        num_samples = 0
        for (inputs_, targets_) in (pbar := tqdm.tqdm(enumerate(loader))):
            inputs = targets_["past_ticks"]
            targets = targets_["next_ticks"]
            inputs =inputs.type(torch.float32).detach().clone().requires_grad_(True)
            targets = targets.type(torch.float32).detach().clone().requires_grad_(True)
            inputs, targets = inputs.to(device), targets.to(device)

            # Compute the forward propagation
            
            outputs = self.forward(inputs)
            outputs = torch.reshape(outputs, (outputs.shape[0],1, outputs.shape[1]))
            loss = f_loss(outputs, targets)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # Update the metrics
            # We here consider the loss is batch normalized
            total_loss += inputs.shape[0] * loss.item()
            num_samples += inputs.shape[0]
            pbar.set_description(f"Train loss : {total_loss/num_samples:.2f}")

        return total_loss / num_samples

    


    def test_(self, loader, f_loss, device):
        """
        Test a model over the loader
        using the f_loss as metrics
        Arguments :
        model     -- A torch.nn.Module object
        loader    -- A torch.utils.data.DataLoader
        f_loss    -- The loss function, i.e. a loss Module
        device    -- A torch.device
        Returns :
        """

        # We enter eval mode.
        # This is important for layers such as dropout, batchnorm, ...
        self.eval()

        total_loss = 0
        num_samples = 0
        for (inputs_, targets_) in (pbar := tqdm.tqdm(enumerate(loader))):
            inputs = targets_["past_ticks"]
            targets = targets_["next_ticks"]
            inputs =inputs.type(torch.float32).detach().clone()
            targets = targets.type(torch.float32).detach().clone()
            inputs, targets = inputs.to(device), targets.to(device)

            # Compute the forward propagation
            outputs = self.forward(inputs)
            outputs = torch.reshape(outputs, (outputs.shape[0],1, outputs.shape[1]))
            loss = f_loss(outputs, targets)

            # Update the metrics
            # We here consider the loss is batch normalized
            total_loss += inputs.shape[0] * loss.item()
            num_samples += inputs.shape[0]

        return total_loss / num_samples