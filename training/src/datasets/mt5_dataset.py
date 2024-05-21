from torch.utils.data import Dataset
import pandas as pd
import os



class CloseDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, config):
        self.data = None
        self.nb_past_ticks = config["nb_past_ticks"]
        self.nb_next_ticks = config["nb_next_ticks"]
        self.symbols_metadata = config["symbols_metadata"]
        for file_name in config["symbols_metadata"]:
            close = pd.read_csv(os.path.join(config["DATA_DIR_PATH"], f"{file_name}.csv"))["close"]
            close.rename(file_name[:-3], inplace=True)
            if(self.data is None):
                self.data = close.to_frame()
            else:
                self.data = pd.concat([self.data, close], axis=1)

    def __len__(self):
        return self.data.shape[0] - (self.nb_past_ticks + self.nb_next_ticks)

    def __getitem__(self, idx):
        sample = {
            "past_ticks": self.data.iloc[idx: idx + self.nb_past_ticks].to_numpy(),
            "next_ticks": self.data.iloc[idx + self.nb_past_ticks:idx + self.nb_past_ticks + self.nb_next_ticks].to_numpy(),
            "metadatas": self.symbols_metadata
        }
        return sample