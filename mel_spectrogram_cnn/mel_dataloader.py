import os
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from mel_config import MelConfig

config = MelConfig()


class MelDataset(Dataset):
    def __init__(self, spectrogram_csv):
        self.spectrogram_csv = spectrogram_csv
        self.len = len(spectrogram_csv)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        # Function that returns a spectrogram and its label
        # __getitem__ is called by the DataLoader object that subsumes this Dataset in batches of batch_size
        spectrogram_path = self.spectrogram_csv.iloc[idx, 0]
        label = self.spectrogram_csv.iloc[idx, 1]
        spectrogram = np.load(spectrogram_path)
        spectrogram = torch.from_numpy(spectrogram).float()
        # print(spectrogram.float())
        return spectrogram.unsqueeze(0), label


class MelTestDataset(Dataset):
    def __init__(self, spectrogram_csv):
        self.spectrogram_csv = spectrogram_csv
        self.len = len(spectrogram_csv)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        # Function that returns a spectrogram and its label
        # __getitem__ is called by the DataLoader object that subsumes this Dataset in batches of batch_size
        spectrogram_path = self.spectrogram_csv.iloc[idx, 0]
        file = self.spectrogram_csv.iloc[idx, 1]
        spectrogram = np.load(spectrogram_path)
        spectrogram = torch.from_numpy(spectrogram).float()

        return spectrogram.unsqueeze(0), file


def data_generator(spectrogram_csv_path, test_csv_path=None):
    spectrogram_csv = pd.read_csv(spectrogram_csv_path)

    # Partition samples into training and validation sets
    train_csv, val_csv = train_test_split(spectrogram_csv, test_size=config.val_size, random_state=config.seed)

    # Read test csv
    test_csv = pd.read_csv(test_csv_path)

    # Create custom Dataset objects that are then fed to the DataLoader
    train_data = MelDataset(train_csv)
    val_data = MelDataset(val_csv)
    test_data = MelTestDataset(test_csv)

    train_dataloader = DataLoader(train_data, batch_size=config.batch_size, shuffle=True,
                                  drop_last=config.drop_last)
    val_dataloader = DataLoader(val_data, batch_size=config.batch_size, shuffle=False, drop_last=config.drop_last)
    test_dataloader = DataLoader(test_data, batch_size=config.batch_size, shuffle=False)
    return train_dataloader, val_dataloader, test_dataloader