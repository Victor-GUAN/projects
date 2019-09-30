# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 15:46:00 2019

@author: Minghui GUAN
"""

import pandas as pd
import numpy as np

# create lag indicators without ema
def cal_indic_dynamic(filepath_indicator, indicator, lag_list):
    
    df = pd.read_csv(filepath_indicator, index_col = 0, header = 0, sep = ',').astype(np.float)
    df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    lag_list = sorted(lag_list)
    lag_max = max(lag_list)
    df = df.T
    time_set = list(df.columns)
    dict_indic = {}

    for lag in lag_list:
        arr_indic_1 = np.asarray(df.loc[indicator, time_set[lag_max] : time_set[-2]]
                                   .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
        arr_indic_2 = np.asarray(df.loc[indicator, time_set[lag_max - lag] : time_set[-2 - lag]]
                                   .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
        arr_indic = arr_indic_1 - arr_indic_2
        arr_indic[np.isnan(arr_indic)] = 0.0
        dict_indic['lag_' + str(lag)] =  list(arr_indic)
    
    arr_ret_1 = np.asarray(df.loc[indicator, time_set[lag_max + 1] : time_set[-1]]
                             .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
    arr_ret_2 = np.asarray(df.loc[indicator, time_set[lag_max] : time_set[-2]]
                             .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
    arr_ret = arr_ret_1 - arr_ret_2
    arr_ret[np.isnan(arr_ret)] = 0.0
    dict_indic['target'] = list(arr_ret)
    
    df_dynamic = pd.DataFrame(dict_indic, index = time_set[lag_max : -1]).astype(np.float)
    
    return df_dynamic

# create lag indicators with ema
def cal_indic_ema(filepath_indicator, indicator, lag_list):
    
    df = pd.read_csv(filepath_indicator, index_col = 0, header = 0, sep = ',').astype(np.float)
    df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    arr = df[indicator].tolist()
    
    lag_list = sorted(lag_list)
    lag_max = max(lag_list)
    time_set = list(df.index)
    dict_indic = {}
    
    for lag in lag_list:
        arr_ema = ema_trans(arr, lag).tolist()
        df_ema = pd.DataFrame({indicator: arr_ema}, index = time_set)
        df_ema = df_ema.T
        
        arr_indic_1 = np.asarray(df_ema.loc[indicator, time_set[lag_max] : time_set[-2]]
                                   .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
        arr_indic_2 = np.asarray(df_ema.loc[indicator, time_set[lag_max - 1] : time_set[-3]]
                                   .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
        arr_indic = arr_indic_1 - arr_indic_2
        arr_indic[np.isnan(arr_indic)] = 0.0
        dict_indic['ema_lag_' + str(lag)] =  list(arr_indic)
        
    df = df.T
    arr_ret_1 = np.asarray(df.loc[indicator, time_set[lag_max + 1] : time_set[-1]]
                             .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
    arr_ret_2 = np.asarray(df.loc[indicator, time_set[lag_max] : time_set[-2]]
                             .apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0))
    arr_ret = arr_ret_1 - arr_ret_2
    arr_ret[np.isnan(arr_ret)] = 0.0
    dict_indic['target'] = list(arr_ret)
    
    df_ema = pd.DataFrame(dict_indic, index = time_set[lag_max : -1]).astype(np.float)
    
    return df_ema
        
def ema_trans(arr, lag):
    """
    For exponential moving average, alpha =  2 / (lag + 1)
    This is because in this case, the weights of an simple moving average (SMA) and exponential moving average (EMA) have the same "center of mass"
    """
    alpha =  2 / (lag + 1)
    arr_ema = np.zeros(len(arr))
    arr_ema[0] = arr[0]
    for idx in range(1, len(arr)):
        arr_ema[idx] = alpha * arr[idx] + (1 - alpha) * arr_ema[idx - 1]
        
    return arr_ema
        








        

    
    
    
    