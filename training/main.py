# coding: utf-8

# Standard imports
import logging
import sys
import os
import pathlib

# External imports
import yaml
import wandb
import torch
from torchinfo import summary

# Local imports
import data
import src.models as models
import optim
import utils


def train(config):

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda") if use_cuda else torch.device("cpu")

    # Build the dataloaders
    logging.info("= Building the dataloaders")
    data_config = config["data"]

    train_loader, valid_loader, input_size, output_size = data.get_dataloaders(
        data_config, use_cuda
    )

    # Build the model
    logging.info("= Model")
    model_config = config["model"]
    model = eval(f"models.{model_config['name']}(model_config, input_size, output_size)")
    model.to(device)

    # Build the loss
    logging.info("= Loss")
    loss = optim.get_loss(config["loss"])

    # Build the optimizer
    logging.info("= Optimizer")
    optim_config = config["optim"]
    optimizer = optim.get_optimizer(optim_config, model.parameters())

    
    # Make a summary script of the experiment
    logdir = ""
    if config["save_model_summary"]:
        # Build the callbacks
        logging_config = config["logging"]
        # Let us use as base logname the class name of the model
        logname = model_config["name"]
        logdir = utils.generate_unique_logpath(logging_config["logdir"], logname)
        if not os.path.isdir(logdir):
            os.makedirs(logdir)
        logging.info(f"Will be logging into {logdir}")

        # Copy the config file into the logdir
        logdir = pathlib.Path(logdir)
        with open(logdir / "config.yaml", "w") as file:
            yaml.dump(config, file)
        summary_text = (
            f"Logdir : {logdir}\n"
            + "## Command \n"
            + " ".join(sys.argv)
            + "\n\n"
            + f" Config : {config} \n\n"
            + "## Summary of the model architecture\n"
            + f"{summary(model, input_size=input_size)}\n\n"
            + "## Loss\n\n"
            + f"{loss}\n\n"
            + "## Datasets : \n"
            + f"Train : {train_loader.dataset.dataset}\n"
            + f"Validation : {valid_loader.dataset.dataset}"
        )
        with open(os.path.join(logdir, "summary.txt"), "w", encoding="utf-8") as f:
            f.write(summary_text)
        logging.info(summary_text)

    # Define the early stopping callback
    model_checkpoint = utils.ModelCheckpoint(
        model, os.path.join(logdir, "best_model.pt"), min_is_best=True
    )

    for e in range(config["nepochs"]):
        # Train 1 epoch
        train_loss = model.train_(train_loader, loss, optimizer, device)

        # Test
        test_loss = model.test_(valid_loader, loss, device)

        updated = model_checkpoint.update(test_loss, config["save_model_summary"])
        logging.info(
            "[%d/%d] Test loss : %.3f %s"
            % (
                e,
                config["nepochs"],
                test_loss,
                "[>> BETTER <<]" if updated else "",
            )
        )

        # Update the dashboard
        metrics = {"train_CE": train_loss, "test_CE": test_loss}


def test(config):
    raise NotImplementedError


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    if len(sys.argv) != 3:
        logging.error(f"Usage : {sys.argv[0]} config.yaml <train|test>")
        sys.exit(-1)

    logging.info("Loading {}".format(sys.argv[1]))
    config = yaml.safe_load(open(sys.argv[1], "r"))

    command = sys.argv[2]
    eval(f"{command}(config)")