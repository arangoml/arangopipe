#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:58:20 2019

@author: Rajiv Sambasivan
"""
from arangopipe.arangopipe_analytics.regression_perf_analyzer import RegressionPerfAnalyzer
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error
from subprocess import check_call

class DT_RegressionPerfAnalyzer(RegressionPerfAnalyzer):
    def segment_regression_performance(self, ytrue, ypred, pred_data, output_dir = ".",\
         res_kde_plt_fname = "residual_fit_error_density.pdf", seg_dt_fname = "seg_perf_regions.png"):
        residual = ytrue - ypred
        dr = DummyRegressor()
        dr.fit(pred_data, residual)
        ypred_dr = dr.predict(pred_data)
        mse_dr = mean_squared_error(residual, ypred_dr)
        fnames = pred_data.columns.tolist()
        regr = DecisionTreeRegressor(random_state=0, max_depth = 3)
        regr = regr.fit(pred_data, residual)
        ypred = regr.predict(pred_data)
        mse_dtr = mean_squared_error(ypred, residual)
        rfresidual = residual - ypred
        print("Residual DTR MSE: %.2f " % (mse_dtr))
        print("Residual Baseline(Dummy Regressor) MSE: %.2f " % (mse_dr))
        fp1 = output_dir + "/" + res_kde_plt_fname
        ax = residual.plot.kde()
        fig = ax.get_figure()
        ax = rfresidual.plot.kde()
        ax.grid(which='both')
        fig = ax.get_figure()
        fig.savefig(fp1)
        fp2 = output_dir + "/" + seg_dt_fname
        tree.export_graphviz(regr, feature_names = fnames, out_file="seg_perf_regions.dot")
        check_call(['dot','-Tpng','seg_perf_regions.dot','-o', fp2])
        
        return

