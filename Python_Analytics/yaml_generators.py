# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:52:47 2019

@author: Minghui GUAN
"""
import yaml
import itertools
import copy
import os

# generate multiple personalized yaml files for parallel simulations

if __name__ == '__main__':
    
    use_emas = [True, False]
    kmeans = [[1], [1,2]]
    pvalues = [0, -1]
    
    quan_percentage_simple = [0.5, 1, 2, 4, 7, 10]
    kurt_simple = [-0.2, -0.5, 0, 0.2, 0.5]
    quan_min_max = [[30, 70], [40, 60], [45, 55], [20, 80]]

    nonskew_transform = ['standard', 'normal', 'uniform', 'robust']
    skew_size = [0.8, 0.4, 0.2]
    quan = [0.5, 1, 2, 4, 7, 10]
    kurt_complex = [-0.2, -0.5, 0, 0.2, 0.5]
    
    params_common = list(itertools.product(use_emas, kmeans, pvalues))
    params_simple = list(itertools.product(quan_percentage_simple, kurt_simple))
    params_complex = list(itertools.product(nonskew_transform, skew_size, quan, kurt_complex))
    params_tot_complex = []
    params_tot_simple = []
    
    t1 = (True,)
    t2 = (False,)
    for p in params_common:
        for pp in params_simple:
            for q in quan_min_max:    
                params_tot_simple.append(t1 + p + pp + (q[0], q[-1],))
                
        for pp in params_complex:
            params_tot_complex.append(t2 + p + pp)
    
    data_init = yaml.load(open(os.getcwd() + '/config.yaml'))
    
    def generate_complex_yaml(params):
        data = copy.deepcopy(data_init)
        data['experiment_params']['choose_normalization_simple_or_complex'] = str(params[0])
        data['use_ema'] = str(params[1])
        data['experiment_params']['kmeans_n_clusters'] = [str(i) for i in params[2]]
        data['experiment_params']['pvalue_threshold'] = str(params[3])
        data['experiment_params']['normalization_complex']['normalization_type_for_nonskewed_part'] = str(params[4])
        data['experiment_params']['normalization_complex']['skew_size'] = str(params[5])
        data['experiment_params']['normalization_complex']['quantile_percentage_for_outliers'] = str(params[6])
        data['experiment_params']['normalization_complex']['kurt_threshold'] = str(params[7])
        
        name_prefix = 'simple_or_complex_{}_ema_{}_kmeans_{}_pvalue_{}_nonskew_{}_skewsize_{}_quan_{}_kurt_{}'.format(params[0],
                                                                                                                      params[1],
                                                                                                                      ''.join([str(i) for i in params[2]]),
                                                                                                                      params[3],
                                                                                                                      params[4],
                                                                                                                      params[5],
                                                                                                                      params[6],
                                                                                                                      params[7])
        data['fig_outpath'] = name_prefix
        yaml.dump(data, open(os.getcwd() + '/YAML_complex/{}.yaml'.format(name_prefix), 'w'))
        
        
    def generate_simple_yaml(params):
        data = copy.deepcopy(data_init)
        data['experiment_params']['choose_normalization_simple_or_complex'] = str(params[0])
        data['use_ema'] = str(params[1])
        data['experiment_params']['kmeans_n_clusters'] = [str(i) for i in params[2]]
        data['experiment_params']['pvalue_threshold'] = str(params[3])
        data['experiment_params']['normalization_simple']['quantile_percentage_for_outliers_simple'] = str(params[4])
        data['experiment_params']['normalization_simple']['kurt_threshold_simple'] = str(params[5])
        data['experiment_params']['normalization_simple']['quantile_min_robust_transform'] = str(params[6])
        data['experiment_params']['normalization_simple']['quantile_max_robust_transform'] = str(params[7])
        
        name_prefix = 'simple_or_complex_{}_ema_{}_kmeans_{}_pvalue_{}_quansimple_{}_kurtsimple_{}_inf_{}_sup_{}'.format(params[0],
                                                                                                                         params[1],
                                                                                                                         ''.join([str(i) for i in params[2]]),
                                                                                                                         params[3],
                                                                                                                         params[4],
                                                                                                                         params[5],
                                                                                                                         params[6],
                                                                                                                         params[7])
        data['fig_outpath'] = name_prefix
        yaml.dump(data, open(os.getcwd() + '/YAML_simple/{}.yaml'.format(name_prefix), 'w'))
        
    for params in params_tot_simple:
        print(params)
        generate_simple_yaml(params)
    for params in params_tot_complex:
        generate_complex_yaml(params)
        
        
        
        
        
        
        
        
        
        
