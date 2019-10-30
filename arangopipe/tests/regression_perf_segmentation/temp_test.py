#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:53:35 2019

@author: admin2
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from arangopipe.arangopipe_analytics.dt_regression_perf_analyzer import DT_RegressionPerfAnalyzer
from sklearn.metrics import mean_squared_error

def load_data(trng_prop = 0.667):
    fp = "cal_housing.csv"
    df = pd.read_csv(fp)
    preds = df.columns.tolist()
    preds.remove("medianHouseValue")
    df["medianHouseValue"] = np.log(df["medianHouseValue"])
    df[preds] = StandardScaler().fit_transform(df[preds].values)
    msk = np.random.rand(len(df)) < trng_prop
    df_train = df[msk]
    df_test = df[~msk]
    X_train = df_train[preds]
    Y_train = df_train["medianHouseValue"]
    X_test = df_test[preds]
    Y_test = df_test["medianHouseValue"]
    return X_train, Y_train, X_test, Y_test

def fit_regression():
    X_train,Y_train, X_test, Y_test = load_data()
    dtr = DecisionTreeRegressor(random_state=0, max_depth = 3)
    dtr.fit(X_train,Y_train)
    ypred = dtr.predict(X_test)
    mse = mean_squared_error(Y_test, ypred)
    print("Mean Squared Error for Model: %.2f" % (mse))
    return ypred, Y_test, X_test

def run_test():
    ypred, Y, X = fit_regression()
    dtra = DT_RegressionPerfAnalyzer()
    regr = dtra.segment_regression_performance(Y, ypred, X, output_dir = "./plots")
    return regr     