# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 08:00:32 2019

@author: Minghui GUAN
"""
import indicators_generator
import experiment
import create_analytics
import os
import sys
import yaml
import numpy as np
import warnings
from sklearn import metrics
import pandas as pd

def run_simple():
    config_yaml_path = os.path.normpath(sys.argv[1])
    
    #------Load yaml configuration file----------------
    with open(config_yaml_path, 'r') as stream:
        try:
            config_params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()
            
    #-------Get parameters-----------------
    filepath_indicator = config_params['filepath_indicator']
    fig_outpath = config_params['fig_outpath']
    file_name = fig_outpath
    fig_outpath = os.getcwd() + '/{}'.format(file_name)
    
    experiment_params = config_params['experiment_params']
    create_analytics_params = config_params['create_analytics_params']
    
    indicator = config_params['indicator']
    use_ema = config_params['use_ema']
    lag_list = np.array(config_params['lag_list']).astype(np.float).astype(np.int).tolist()
    
    if experiment.parse_yaml_bool(use_ema):
        df = indicators_generator.cal_indic_ema(filepath_indicator, indicator, lag_list)
    else:
        df = indicators_generator.cal_indic_dynamic(filepath_indicator, indicator, lag_list)
    
    df.to_csv(os.getcwd() + '/indictaors.csv', index = True, header = True)
    
    predictions, real_returns = experiment.get_predictions(df, experiment_params)

    r2_score = metrics.r2_score(real_returns, predictions)
    variance_score = metrics.explained_variance_score(real_returns, predictions)
    mean_squared_error = metrics.mean_squared_error(real_returns, predictions)
    
    df_score = pd.DataFrame({'r2_score': [r2_score], 
                             'variance_score': [variance_score],
                             'mean_squared_error': [mean_squared_error]})
    df_score.to_csv(os.getcwd() + '/results/{}.csv'.format(file_name), index = True, header = True)
    
    print("R2 SCORE: {}".format(r2_score))
    print("VARIANCE SCORE: {}".format(variance_score))
    print("MSE: {}".format(mean_squared_error))
    
    create_analytics.cal_statistcs(real_returns,
                                   predictions,
                                   create_analytics_params,
                                   fig_outpath)

def run(config_yaml_path):
    #------Load yaml configuration file----------------
    with open(config_yaml_path, 'r') as stream:
        try:
            config_params = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit()
            
    #-------Get parameters-----------------
    filepath_indicator = config_params['filepath_indicator']
    fig_outpath = config_params['fig_outpath']
    file_name = fig_outpath
    fig_outpath = os.getcwd() + '/{}'.format(file_name)
    
    experiment_params = config_params['experiment_params']
    create_analytics_params = config_params['create_analytics_params']
    
    indicator = config_params['indicator']
    use_ema = config_params['use_ema']
    lag_list = np.array(config_params['lag_list']).astype(np.float).astype(np.int).tolist()
    
    if experiment.parse_yaml_bool(use_ema):
        df = indicators_generator.cal_indic_ema(filepath_indicator, indicator, lag_list)
    else:
        df = indicators_generator.cal_indic_dynamic(filepath_indicator, indicator, lag_list)
    
    df.to_csv(os.getcwd() + '/indictaors.csv', index = True, header = True)
    
    predictions, real_returns = experiment.get_predictions(df, experiment_params)

    r2_score = metrics.r2_score(real_returns, predictions)
    variance_score = metrics.explained_variance_score(real_returns, predictions)
    mean_squared_error = metrics.mean_squared_error(real_returns, predictions)
    
    df_score = pd.DataFrame({'r2_score': [r2_score], 
                             'variance_score': [variance_score],
                             'mean_squared_error': [mean_squared_error]})
    df_score.to_csv(os.getcwd() + '/results/{}.csv'.format(file_name), index = True, header = True)
    
    print("R2 SCORE: {}".format(r2_score))
    print("VARIANCE SCORE: {}".format(variance_score))
    print("MSE: {}".format(mean_squared_error))
    
    create_analytics.cal_statistcs(real_returns,
                                   predictions,
                                   create_analytics_params,
                                   fig_outpath)

warnings.filterwarnings('error')

if __name__ == '__main__':
    #run_simple()
    
    for f in os.listdir(os.getcwd() + '/YAML_simple/'):
        config_path = os.getcwd() + '/YAML_simple/' + f
        try:
            run(config_path)
        except:
            pass
    for f in os.listdir(os.getcwd() + '/YAML_complex/'):
        config_path = os.getcwd() + '/YAML_complex/' + f
        try:
            run(config_path)
        except:
            pass
    """
    df1 = pd.read_csv(os.getcwd() + '/indictaors.csv', header = 0, index_col = 0)
    df2 = pd.read_csv(os.getcwd() + '/data10000.csv', header = 0, index_col = 0)
    l2 = df2['gasUsed'].tolist()
    l1 = df1['target'].tolist()
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams['figure.figsize'] = (20.0, 3.0)
    plt.plot(l1)
    plt.show()
    """
    
