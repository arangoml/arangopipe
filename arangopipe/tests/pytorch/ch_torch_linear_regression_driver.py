#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 09:19:36 2019

@author: Rajiv Sambasivan
"""
import torch
from ch_data_loader import CH_Dataset
from ch_linear_regression_model import CH_LinearRegression
import torch.nn as nn
from torch.utils import data
from torch.autograd import Variable
import numpy as np
from math import sqrt
import jsonpickle
from arangopipe.arangopipe_storage.arangopipe_api import ArangoPipe
from arangopipe.arangopipe_storage.arangopipe_admin_api import ArangoPipeAdmin
from arangopipe.arangopipe_storage.arangopipe_config import ArangoPipeConfig
import uuid
import datetime
from arangopipe.arangopipe_storage.managed_service_conn_parameters import (
    ManagedServiceConnParam, )
import yaml
import os

# from torch.utils.data.sampler import SubsetRandomSampler


def get_test_config():
    file_name = os.path.join(os.path.dirname(__file__),
                             "../test_config/test_datagen_config.yaml")
    with open(file_name, "r") as file_descriptor:
        test_cfg = yaml.load(file_descriptor, Loader=yaml.FullLoader)

    return test_cfg


def run_driver():

    params = {"batch_size": 128, "shuffle": True, "num_workers": 6}
    trng_dataset = CH_Dataset()
    test_dataset = CH_Dataset(train=False)
    training_generator = data.DataLoader(trng_dataset, **params)
    test_generator = data.DataLoader(test_dataset, **params)
    input_size = trng_dataset.input_size
    output_size = trng_dataset.output_size

    m = CH_LinearRegression(inputSize=input_size, outputSize=output_size)
    cost_func = nn.MSELoss()
    learning_rate = 0.1
    optimizer = torch.optim.Adam(m.parameters(), lr=learning_rate)
    all_losses = []
    test_pred_list = []
    test_acts_list = []
    num_epochs = 100
    loss_sched = {}
    for e in range(num_epochs):
        batch_losses = []
        for ix, (Xb, yb) in enumerate(training_generator):
            _X = Variable(Xb).float()

            _y = Variable(yb).float()
            # ==========Forward pass===============
            preds = m(_X)
            preds = torch.flatten(preds)
            loss = cost_func(preds, _y)

            # ==========backward pass==============

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_losses.append(loss.item())
            all_losses.append(loss.item())

        mbl = sqrt(np.mean(batch_losses))

        if e % 5 == 0:
            print("training loss: " + str(mbl))
            loss_sched[e] = mbl

    # prepares model for inference when trained with a dropout layer

    #    print(m.training)
    #    m.eval()
    #    print(m.training)

    test_batch_losses = []
    test_pred_list = []
    test_acts_list = []
    for _X, _y in test_generator:

        _X = Variable(_X).float()
        _y = Variable(_y).float()

        # apply model
        test_preds = m(_X)
        test_preds = torch.flatten(test_preds)
        test_loss = cost_func(test_preds, _y)
        test_pred_list.extend(test_preds.detach().numpy().ravel())
        test_acts_list.extend(_y.numpy().ravel())

        test_batch_losses.append(test_loss.item())
    # print("Batch loss: {}".format(test_loss.item()))

    tmbl = sqrt(np.mean(test_batch_losses))
    print("test loss: " + str(tmbl))

    # Store experiment results in Arangopipe
    conn_config = ArangoPipeConfig()
    msc = ManagedServiceConnParam()
    test_cfg = get_test_config()
    conn_params = {
        msc.DB_SERVICE_HOST: test_cfg["arangodb"][msc.DB_SERVICE_HOST],
        msc.DB_SERVICE_END_POINT:
        test_cfg["arangodb"][msc.DB_SERVICE_END_POINT],
        msc.DB_SERVICE_NAME: test_cfg["arangodb"][msc.DB_SERVICE_NAME],
        msc.DB_SERVICE_PORT: test_cfg["arangodb"][msc.DB_SERVICE_PORT],
        msc.DB_CONN_PROTOCOL: test_cfg["arangodb"][msc.DB_CONN_PROTOCOL],
    }
    #    conn_params = { msc.DB_SERVICE_HOST : "localhost", \
    #                        msc.DB_SERVICE_END_POINT : "apmdb",\
    #                        msc.DB_SERVICE_NAME : "createDB",\
    #                        msc.DB_SERVICE_PORT : 8529,\
    #                        msc.DB_CONN_PROTOCOL : 'http',\
    #                        msc.DB_NOTIFICATION_EMAIL : 'somebody@some_company.com'}

    conn_config = conn_config.create_connection_config(conn_params)
    proj_info = {"name": "Housing_Price_Estimation_Project"}
    admin = ArangoPipeAdmin(reuse_connection=False, config=conn_config)
    proj_reg = admin.register_project(proj_info)
    ap_config = admin.get_config()
    ap = ArangoPipe(config=ap_config)
    ruuid = str(uuid.uuid4().int)
    model_name = "pytorch-linear-reg" + "_dev_run_" + ruuid
    model_info = {"name": model_name, "type": "model-development"}
    model_reg = ap.register_model(model_info,
                                  project="Housing_Price_Estimation_Project")
    ds_info = trng_dataset.get_dataset()
    ds_reg = ap.register_dataset(ds_info)
    fs = trng_dataset.get_featureset()
    fs_reg = ap.register_featureset(fs, ds_reg["_key"])

    model_params = {
        "optimizer": "Adam",
        "training_epochs": 100,
        "batch_size": 128,
        "learning_rate": learning_rate,
        "run_id": ruuid,
    }
    model_perf = {
        "training_loss_schedule": jsonpickle.encode(loss_sched),
        "run_id": ruuid,
        "timestamp": str(datetime.datetime.now()),
    }
    run_tag = "Housing-Price-Pytorch-Experiment" + "_dev_run_" + ruuid
    run_info = {
        "dataset": ds_reg["_key"],
        "featureset": fs_reg["_key"],
        "run_id": ruuid,
        "model": model_reg["_key"],
        "model-params": model_params,
        "model-perf": model_perf,
        "tag": run_tag,
        "project": "Housing Price Estimation Project",
    }
    ap.log_run(run_info)
    mp = ap.lookup_modelperf(run_tag)
    print(
        "A look up of the loss schedule for this experiment in Arangopipe yields:"
    )
    print(str(mp["training_loss_schedule"]))

    return
