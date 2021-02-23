#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:10:33 2019

@author: Rajiv Sambasivan
"""
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from arangopipe.arangopipe_analytics.dataset_shift_detector import DatasetShiftDetector


class RF_DatasetShiftDetector(DatasetShiftDetector):
    def detect_dataset_shift(self, dataframe1, dataframe2):
        pd.options.mode.chained_assignment = None
        dataframe1.loc[:, "DS"] = 0
        dataframe2.loc[:, "DS"] = 1
        dfc = pd.concat([dataframe1, dataframe2])
        preds = dfc.columns.tolist()
        preds.remove("DS")
        X = dfc.loc[:, preds]
        Y = dfc.loc[:, "DS"]
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            Y,
                                                            test_size=0.33,
                                                            random_state=42)
        clf = RandomForestClassifier(n_estimators=100,
                                     max_depth=3,
                                     random_state=0)
        clf.fit(X_train, y_train)
        acc_score = clf.score(X_test, y_test)

        return acc_score
