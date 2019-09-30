# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 12:24:49 2019

@author: Minghui GUAN
"""

import pandas as pd
import numpy as np
import copy
import os
import scipy.stats as stats
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import scipy

def df_trim(df):
    
    inds = df.columns
    df = df.loc[(df != 0).any(axis = 1)]
    
    return df, inds

def df_dist_partition_equal_num(df, col, nb_bins):
    
    index_count_dict = {}
    index = []
    arr = np.array(df[col])
    arr_nonzero = arr[arr != 0]
    partition = []
    
    if len(arr[arr == 0]) / len(arr) > 0.8:
        return None
    
    num = int(len(arr_nonzero) / nb_bins)
    num_partition = int(len(arr_nonzero) / num) + 1
    arr_sort = np.sort(arr_nonzero)
    hole_sub_boundry = 0.0
    
    if arr_nonzero.max() * arr_nonzero.min() >= 0:
        
        for idx_num_part in range(1, num_partition):
            partition.append((arr_sort[idx_num_part * num] + arr_sort[idx_num_part * num - 1]) / 2.0)
        
        partition = [arr_nonzero.min()] + partition + [arr_nonzero.max()]
    
    else:

        arr_pos = arr_sort[arr_sort > 0]
        arr_neg = arr_sort[arr_sort < 0][::-1]
        
        n_pos, n_neg = int(len(arr_pos) / num) + 1, int(len(arr_neg) / num) + 1
        
        pos_boundry = [(arr_pos[count_point * num] + arr_pos[count_point * num - 1]) / 2.0 for count_point in range(1, n_pos)] if n_pos > 1 else []
        neg_boundry = [(arr_neg[count_point * num] + arr_neg[count_point * num - 1]) / 2.0 for count_point in range(1, n_neg)][::-1] if n_neg > 1 else []
        
        part_pos = [arr_pos.min()] + pos_boundry + [arr_pos.max()]
        part_neg = [arr_neg.min()] + neg_boundry + [arr_neg.max()]
        
        hole_sub_boundry = arr_neg.max()
        partition = part_neg + part_pos
        
    for idx_num_part in arr:
        
        if idx_num_part == 0:
            interval_name = '0'
            index.append('0')
            index_count_dict[interval_name] = index_count_dict.get(interval_name, 0) + 1
            continue
        
        elif idx_num_part >= partition[-2]:
            interval_name = '[{}, {}]'.format(partition[-2], partition[-1])
            index.append(interval_name)
            index_count_dict[interval_name] = index_count_dict.get(interval_name, 0) + 1
            continue
        
        for idx_partition in range(len(partition) - 1):
            if partition[idx_partition] <= idx_num_part < partition[idx_partition + 1] or (idx_num_part == partition[idx_partition + 1] and idx_num_part == hole_sub_boundry):
                interval_name = '[{}, {}]'.format(partition[idx_partition], partition[idx_partition + 1])
                index.append(interval_name)
                index_count_dict[interval_name] = index_count_dict.get(interval_name, 0) + 1
                break
            
    df.loc[ : , '{}_partition'.format(col)] = index
    
    return df, index_count_dict


def dist_partition_analysis(df_tot, cols, nb_bins_list):
    df_tot = copy.deepcopy(df_tot)
    df_tot, indicators_columns = df_trim(df_tot)
    
    part_list = []
    part_dict_order = {}
    index_dicts = {}
    
    part_func = df_dist_partition_equal_num
    
    for (col, nb_bins) in zip(cols, nb_bins_list):
        
        col_partition = '{}_partition'.format(col)
        df_tot, ind_index_count_dict = part_func(df_tot, col, nb_bins)
        order_tmp = pd.unique(df_tot.sort_values(by = [col])[col_partition].tolist())
        part_list.append(col_partition)
        part_dict_order[col_partition] = order_tmp
        index_dicts[col_partition] = ind_index_count_dict
        
    return df_tot, part_list, part_dict_order, index_dicts

def dist_partition_out(df_tot,
                       part_list,
                       part_dict_order,
                       index_dicts,
                       graph_outpath,
                       true_col):
    #boxplot
    #violin plot
    
    for pred_col_partition in part_list:
        pred_col = pred_col_partition.replace('_partition', '')
        ymedians = df_tot.groupby(pred_col_partition, as_index = True)[true_col].median().loc[list(part_dict_order[pred_col_partition])].values
        ymeans = df_tot.groupby(pred_col_partition, as_index = True)[true_col].mean().loc[list(part_dict_order[pred_col_partition])].values
        xmedians = df_tot.groupby(pred_col_partition, as_index = True)[pred_col].median().loc[list(part_dict_order[pred_col_partition])].values
        xmeans = df_tot.groupby(pred_col_partition, as_index = True)[pred_col].mean().loc[list(part_dict_order[pred_col_partition])].values
        ypos = range(len(part_dict_order[pred_col_partition]))
        
        # ------------boxplot-----------------
        fig1, ax1 = plt.subplots(figsize = (5 * len(part_dict_order[pred_col_partition]), 50))
        ax1.set_ylim([-2, +2])
        sns.boxplot(ax = ax1,
                    x = df_tot[pred_col_partition],
                    y = df_tot[true_col],
                    order = part_dict_order[pred_col_partition],
                    showfliers = True,
                    showmeans = True,
                    meanline = True)
        
        for tick, label in zip(ypos, ax1.get_xticklabels()):
            ax1.text(ypos[tick], 
                     ymedians[tick] + 0.0001, 
                     index_dicts[pred_col_partition][part_dict_order[pred_col_partition][tick]],
                     horizontalalignment = 'center',
                     size = 'xx-large',
                     color = 'w',
                     weight = 'semibold')
            
        sns.pointplot(ax = ax1,
                      x = pred_col_partition,
                      y = true_col,
                      data = df_tot.groupby(pred_col_partition, as_index = False).mean(),
                      order = part_dict_order[pred_col_partition],
                      linestyle = '-',
                      color = 'b')
        
        sns.pointplot(ax = ax1,
                      x = pred_col_partition,
                      y = true_col,
                      data = df_tot.groupby(pred_col_partition, as_index = False).median(),
                      order = part_dict_order[pred_col_partition],
                      linestyle = '--',
                      color = 'k')
        
        plt.savefig(graph_outpath + '/{}_boxplot.png'.format(pred_col))
        plt.close()
        
        # ------------violin plot-----------------
        fig2, ax2 = plt.subplots(figsize = (5 * len(part_dict_order[pred_col_partition]), 50))
        ax2.set_ylim([-2, +2])
        sns.violinplot(ax = ax2,
                    x = df_tot[pred_col_partition],
                    y = df_tot[true_col],
                    order = part_dict_order[pred_col_partition],
                    showfliers = True,
                    showmeans = True,
                    meanline = True)
        
        for tick, label in zip(ypos, ax2.get_xticklabels()):
            ax2.text(ypos[tick], 
                     ymedians[tick] + 0.0001, 
                     index_dicts[pred_col_partition][part_dict_order[pred_col_partition][tick]],
                     horizontalalignment = 'center',
                     size = 'xx-large',
                     color = 'w',
                     weight = 'semibold')
            
        sns.pointplot(ax = ax2,
                      x = pred_col_partition,
                      y = true_col,
                      data = df_tot.groupby(pred_col_partition, as_index = False).mean(),
                      order = part_dict_order[pred_col_partition],
                      linestyle = '-',
                      color = 'b')
        
        sns.pointplot(ax = ax2,
                      x = pred_col_partition,
                      y = true_col,
                      data = df_tot.groupby(pred_col_partition, as_index = False).median(),
                      order = part_dict_order[pred_col_partition],
                      linestyle = '--',
                      color = 'k')
        
        plt.savefig(graph_outpath + '/{}_violin_plot.png'.format(pred_col))
        plt.close()
        
        # ------------regression plot-----------------
        figs, ax3 = plt.subplots(figsize = (20, 10))
        ax3.set_ylim([-5, +5])
        ax3.set_xlim([-5, +5])
        
        sns.regplot(ax = ax3,
                    x = xmedians,
                    y = ymedians,
                    color = 'k')
        sns.regplot(ax = ax3,
                    x = xmeans,
                    y = ymeans,
                    color = 'b')
        
        slope_median, intercept_median, r_value_median, p_value_median, std_err_median = scipy.stats.linregress(x = xmedians, y = ymedians)
        slope_mean, intercept_mean, r_value_mean, p_value_mean, std_err_mean = scipy.stats.linregress(x = xmeans, y = ymeans)
        
        textstr = '\n'.join((
                r"MEAN is BLUE",
                r"MEDIAN is BLACK",
                r"median slope = %.5f" % (slope_median, ),
                r"mean slope = %.5f" % (slope_mean, ),
                r"median intercept = %.5f" % (intercept_median, ),
                r"mean intercept = %.5f" % (intercept_mean, )
                ))
        # these are matplotlib.patch.Patch.properties
        props = dict(boxstyle = 'round', facecolor = 'wheat', alpha = 0.5)
        ax3.text(0.05, 0.95, 
                 textstr, 
                 transform = ax3.transAxes, 
                 fontsize = 10, 
                 verticalalignment = 'top',
                 bbox = props)
        
        plt.savefig(graph_outpath + '/{}_regplot.png'.format(pred_col))
        plt.close()
        
def stats_analysis(df, period_length, pred_col, true_col):
    
    df, inds = df_trim(df)
    out_dict = {}
    
    if len(df) == 0:
        return None
    else:
        index_base = list(df.index)
        for period in range(0, len(index_base), period_length):
            df_period = df.iloc[period : min(period + period_length, len(index_base))]
            corr, pvalue = stats.pearsonr(x = df_period[pred_col], y = df_period[true_col])
            out_dict['{}'.format(int(period / period_length))] =  [corr * 5, pvalue]
            
        df_stats_out = pd.DataFrame(out_dict, index = ['corr * 5', 'p-value'])
        
    return df_stats_out

def beta_analysis(df, period_length, pred_col, true_col):
    
    ridge_params_grid = {'alpha': [0.1, 0.3, 0.5, 1.0, 5.0, 10.0]}
    simple_linear_params_grid = {'n_jobs': [1]}
    
    ridge_model = linear_model.Ridge(fit_intercept = True,
                                     max_iter = None,
                                     tol = 0.0001,
                                     random_state = 1234)
    
    simple_linear_model = linear_model.LinearRegression(fit_intercept = True,
                                                        normalize = False)
    
    ridge_coef_dict = {}
    simple_linear_coef_dict = {}
    
    out_dict = {}
    
    index_base = list(df.index)
    
    for period in range(0, len(index_base), period_length):
        
        period_idx = int(period / period_length)
        ridge_coef_dict[str(period_idx)] = {}
        simple_linear_coef_dict[str(period_idx)] = {}
        
        df_period = df.iloc[period : min(period + period_length, len(index_base))]
        df_period, indicators_columns = df_trim(df_period)
        
        X = df_period[pred_col].values.reshape(-1, 1)
        y = df_period[true_col].ravel().tolist()
        
        ridge_model_grid = model_selection.GridSearchCV(ridge_model, ridge_params_grid, cv = 5, iid = True)
        simple_linear_model_grid = model_selection.GridSearchCV(simple_linear_model, simple_linear_params_grid, cv = 5, iid = True)
        ridge_model_grid.fit(X, y)
        simple_linear_model_grid.fit(X, y)
        
        ridge_coef = list(ridge_model_grid.best_estimator_.coef_.ravel() * 5)[0]
        simple_linear_coef = list(simple_linear_model_grid.best_estimator_.coef_.ravel())[0]
        
        out_dict['{}'.format(period_idx)] = [ridge_coef, simple_linear_coef]
        
    df_beta_out = pd.DataFrame(out_dict, index = ['ridge_coef * 5', 'simple_linear_coef'])
    
    return df_beta_out

def beta_stats_analysis_out(df, period_length, pred_col, true_col, graph_outpath):
    
    df_beta_out = beta_analysis(df, period_length, pred_col, true_col)
    df_stats_out = stats_analysis(df, period_length, pred_col, true_col)
    
    df_out_tot = pd.concat([df_beta_out, df_stats_out], axis = 0, sort = False)
    df_out_tot_transpose = df_out_tot.transpose()
    
    matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
    df_out_tot_transpose.plot(table = False, title = 'BETA/STAS')
    plt.savefig(graph_outpath + '/beta_stats.png')
    plt.close()
    
def confusion_matrix_out(df_init, pred_col, true_col, graph_outpath):
    df = copy.deepcopy(df_init)
    
    true_col_name = '{}_sign'.format(true_col)
    pred_col_name = '{}_sign'.format(pred_col)
    
    df[true_col_name] = ['sign'] * len(df.index)
    df[pred_col_name] = ['sign'] * len(df.index)
    
    df.loc[df[true_col] > 0, true_col_name] = '+'
    df.loc[df[true_col] < 0, true_col_name] = '-'
    df.loc[df[pred_col] > 0, pred_col_name] = '+'
    df.loc[df[pred_col] < 0, pred_col_name] = '-'
    
    y_true_sign = df.loc[(df[true_col_name] != 'sign') & (df[pred_col_name] != 'sign'), true_col_name].tolist()
    y_pred_sign = df.loc[(df[true_col_name] != 'sign') & (df[pred_col_name] != 'sign'), pred_col_name].tolist()
    
    con_matrix = confusion_matrix(y_pred_sign, y_true_sign, labels = sorted(['+', '-']))
    line_sum = np.sum(con_matrix, axis = 1)
    
    con_matrix_normalized = con_matrix.astype('float') / line_sum[:, None]
    
    matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
    fig, ax = plt.subplots()
    im = ax.imshow(con_matrix_normalized,
                   interpolation = 'nearest',
                   cmap = plt.cm.Blues)
    ax.figure.colorbar(im, ax = ax)
    
    ax.set(xticks = np.arange(con_matrix_normalized.shape[1]),
           yticks = np.arange(con_matrix_normalized.shape[0]),
           xticklabels = sorted(['+', '-']),
           yticklabels = sorted(['+', '-']),
           title = 'Normalized Confusion Matrix',
           xlabel = 'True Label',
           ylabel = 'Prediction Label')
    
    plt.setp(ax.get_xticklabels(),
             rotation = 0,
             ha = 'right',
             rotation_mode = 'anchor')
    
    fmt = '.4f'
    thresh = 0.5
    #thresh = con_matrix_normalized.max() / 2.0
    for idx in range(con_matrix_normalized.shape[0]):
        for col in range(con_matrix_normalized.shape[-1]):
            ax.text(col, idx, 
                    format(con_matrix_normalized[idx, col], fmt) + ' / {}'.format(con_matrix[idx, col]),
                    ha = 'center',
                    va = 'center',
                    color = 'white' if con_matrix_normalized[idx, col] > thresh else 'black')
            
    fig.tight_layout()
    
    plt.savefig(graph_outpath + '/confusion_matrix.png')
    plt.close()
    
def cal_statistcs(real_returns,
                  predict_returns,
                  create_analytics_params,
                  fig_outpath):
    
    period_length_for_beta_stats = int(float(create_analytics_params['period_length_for_beta_stats']))
    quantile_partition_nb_bins = float(create_analytics_params['quantile_partition_nb_bins'])
    
    graph_outpath = fig_outpath
    
    if not os.path.exists(graph_outpath):
        os.makedirs(graph_outpath)
        
    df_y = pd.DataFrame([])
    df_y['Y_true'] = list(real_returns)
    df_y['Y_pred'] = list(predict_returns)
    #print(df_y.head(20))
    df_y = df_y.loc[(df_y != 0).all(axis = 1)]
    
    period_length = period_length_for_beta_stats
    df_tot, part_list, part_dict_order, index_dicts = dist_partition_analysis(df_y, 
                                                                              ['Y_pred'],
                                                                              [quantile_partition_nb_bins])
    
    dist_partition_out(df_tot,
                       part_list,
                       part_dict_order,
                       index_dicts,
                       graph_outpath,
                       'Y_true')
    
    confusion_matrix_out(df_tot,
                         'Y_pred',
                         'Y_true',
                         graph_outpath)

    beta_stats_analysis_out(df_y, 
                            period_length,
                            'Y_pred',
                            'Y_true',
                            graph_outpath)    
    
    
    
    
    
    
    
    
    
    
    
    