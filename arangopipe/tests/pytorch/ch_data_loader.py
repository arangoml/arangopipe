#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 08:59:42 2019

@author: Rajiv Sambasivan
"""
import pandas as pd
from torch.utils import data
import numpy as np
from math import ceil
import torch
from sklearn.preprocessing import StandardScaler


class CH_Dataset(data.Dataset):
    "Characterizes a dataset for PyTorch"

    def __init__(self, fp="cal_housing.csv", train=True, trng_prop=0.667):
        "Initialization"
        self.file_path = fp
        df = pd.read_csv(self.file_path)
        preds = df.columns.tolist()
        preds.remove("medianHouseValue")
        df["medianHouseValue"] = np.log(df["medianHouseValue"])
        featureset = df.dtypes.to_dict()
        featureset = {k: str(featureset[k]) for k in featureset}
        featureset["name"] = "log_transformed_median_house_value"
        self.featureset = featureset
        self.ds_info = {
            "name": "california-housing-dataset",
            "description":
            "This dataset lists median house prices in Califoria. Various house features are provided",
            "source": "UCI ML Repository",
        }
        df[preds] = StandardScaler().fit_transform(df[preds].values)
        num_rows = df.shape[0] - 1
        trng_end = ceil(num_rows * trng_prop)
        if train:
            self.X = torch.from_numpy(df.loc[:trng_end, preds].values)
            self.Y = torch.from_numpy(df.loc[:trng_end,
                                             "medianHouseValue"].values)
        else:
            self.X = torch.from_numpy(df.loc[(trng_end + 1):, preds].values)
            self.Y = torch.from_numpy(df.loc[(trng_end + 1):,
                                             "medianHouseValue"].values)
        self.input_size = len(preds)
        self.output_size = 1

    def __len__(self):
        "Denotes the total number of samples"
        return len(self.X)

    def __getitem__(self, index):
        "Generates one sample of data"
        # Load data and get label
        return self.X[index], self.Y[index]

    def get_featureset(self):
        return self.featureset

    def get_dataset(self):
        return self.ds_info
