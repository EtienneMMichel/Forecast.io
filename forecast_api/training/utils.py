import torch
from operator import mul
from functools import reduce
# coding: utf-8

# Standard imports
import os

# External imports
import torch
import torch.nn
import tqdm


def generate_unique_logpath(logdir, raw_run_name):
    """
    Generate a unique directory name
    Argument:
        logdir: the prefix directory
        raw_run_name(str): the base name
    Returns:
        log_path: a non-existent path like logdir/raw_run_name_xxxx
                  where xxxx is an int
    """
    i = 0
    while True:
        run_name = raw_run_name + "_" + str(i)
        log_path = os.path.join(logdir, run_name)
        if not os.path.isdir(log_path):
            return log_path
        i = i + 1


class ModelCheckpoint(object):
    """
    Early stopping callback
    """

    def __init__(
        self,
        model: torch.nn.Module,
        savepath,
        min_is_best: bool = True,
    ) -> None:
        self.model = model
        self.savepath = savepath
        self.best_score = None
        if min_is_best:
            self.is_better = self.lower_is_better
        else:
            self.is_better = self.higher_is_better

    def lower_is_better(self, score):
        return self.best_score is None or score < self.best_score

    def higher_is_better(self, score):
        return self.best_score is None or score > self.best_score

    def update(self, score, save):
        if self.is_better(score):
            if save:
                torch.save(self.model.state_dict(), self.savepath)
            self.best_score = score
            return True
        return False
    
def train_torch_model(model, loader, f_loss, optimizer, device, dynamic_display=True):
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
    model.train()

    total_loss = 0
    num_samples = 0
    for (inputs_, targets_) in (pbar := tqdm.tqdm(enumerate(loader))):
        inputs = targets_["past_ticks"]
        targets = targets_["next_ticks"]
        
        inputs = inputs.type(torch.float32).detach().clone()
        targets = targets.type(torch.float32).detach().clone()
        
        inputs, targets = inputs.to(device), targets.to(device)
        # Compute the forward propagation
        
        outputs = model(inputs)
        # print("outputs leaf: ", outputs.is_leaf)

        outputs = torch.reshape(outputs, (outputs.shape[0],1, outputs.shape[1]))
        loss = f_loss(outputs, targets)
        # loss.requires_grad = True
 

        # Backward and optimize
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        # Update the metrics
        # We here consider the loss is batch normalized
        total_loss += inputs.shape[0] * loss.item()
        num_samples += inputs.shape[0]
        pbar.set_description(f"Train loss : {total_loss/num_samples:.2f}")

    return total_loss / num_samples




def test_torch_model(model, loader, f_loss, device):
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
    model.eval()

    total_loss = 0
    num_samples = 0
    for (inputs_, targets_) in (pbar := tqdm.tqdm(enumerate(loader))):
        inputs = targets_["past_ticks"]
        targets = targets_["next_ticks"]
        inputs =inputs.type(torch.float32).detach().clone()
        targets = targets.type(torch.float32).detach().clone()
        inputs, targets = inputs.to(device), targets.to(device)

        # Compute the forward propagation
        with torch.no_grad():
            outputs = model(inputs)
            outputs = torch.reshape(outputs, (outputs.shape[0],1, outputs.shape[1]))
            loss = f_loss(outputs, targets)

        # Update the metrics
        # We here consider the loss is batch normalized
        total_loss += inputs.shape[0] * loss.item()
        num_samples += inputs.shape[0]

    return total_loss / num_samples