# coding: utf-8

# Standard imports
import logging
import random

# External imports
import torch
import torch.nn as nn
import torch.utils.data
import torchvision
from torchvision import transforms

import matplotlib.pyplot as plt
from src.datasets.mt5_dataset import CloseDataset



def get_dataloaders(data_config, use_cuda):
    valid_ratio = data_config["valid_ratio"]
    batch_size = data_config["batch_size"]
    num_workers = data_config["num_workers"]

    logging.info("  - Dataset creation")

    base_dataset = eval(f"{data_config['dataset']['name']}(data_config['dataset'])")

    logging.info(f"  - I loaded {len(base_dataset)} samples")

    indices = list(range(len(base_dataset)))
    random.shuffle(indices)
    num_valid = int(valid_ratio * len(base_dataset))
    train_indices = indices[num_valid:]
    valid_indices = indices[:num_valid]

    train_dataset = torch.utils.data.Subset(base_dataset, train_indices)
    valid_dataset = torch.utils.data.Subset(base_dataset, valid_indices)

    # Build the dataloaders
    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=use_cuda,
    )

    valid_loader = torch.utils.data.DataLoader(
        valid_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=use_cuda,
    )

    input_size = tuple(base_dataset[0]["past_ticks"].shape)
    output_size = tuple(base_dataset[0]["next_ticks"].shape)

    return train_loader, valid_loader, input_size, output_size