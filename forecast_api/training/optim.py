# coding: utf-8

# External imports
import torch
import torch.nn as nn


def get_loss(lossname):
    return eval(f"nn.{lossname}()")


def get_optimizer(cfg, params):
    params_dict = cfg["params"]
    optim = eval(f"torch.optim.{cfg['algo']}(params, **params_dict)")
    return optim