# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os

def read_indicators_csv(filepath, filepath_output, filepath_pred_original, ticker, train_scale, validation_scale, holdout_scale, predict_scale, normalization):
    filepath_indict = filepath + '/' + str(ticker) + '/'
    df = pd.read_csv(filepath_indict + os.listdir(filepath_indict)[0], sep = ',', header = 0, index_col = 0)
    time_set = [str(d) for d in list(df.index)]
    indic_set = list(df.columns)
    total_scale = train_scale + validation_scale + holdout_scale
    last_predict_period = int(len(time_set) - total_scale) % int(predict_scale)
    for i in range(int((len(time_set) - total_scale - last_predict_period) / predict_scale) + 1):
        df_period = df.iloc[i * predict_scale : i * predict_scale + total_scale, : ].copy(deep = True)
        df_period_pred = df.iloc[i * predict_scale + total_scale : min((i + 1) * predict_scale + total_scale, len(time_set)), : -1].copy(deep = True)
        df_period.columns = ["indic_" + str(j) for j in range(len(indic_set) - 1)] + ["target"]
        df_period_pred.colums = ["indic_" + str(j) for j in range(len(indic_set) - 1)]
        # df_period = df.iloc[i * predict_scale : min((i + 1) * predict_scale + total_scale, len(time_set)), : ].copy(deep = True)
         
        if normalization:
            for c in range(len(indic_set) - 1):
                mean_value = df_period.iloc[ : , c].mean()
                std_value = df_period.iloc[ : , c].std()
                df_period_pred.iloc[ : , c] = df_period_pred.iloc[ : , c].apply(lambda x: np.float64(x - mean_value) / std_value)
            df_period.iloc[ : , : -1] = df_period.iloc[ : , : -1].apply(lambda x: (x - x.mean()) / x.std(), axis = 0)
             
        df_period[np.isinf(df_period)] = 0.0
        df_period = df_period.fillna(0)
        df_period_pred[np.isinf(df_period_pred)] = 0.0
        df_period_pred = df_period_pred.fillna(0)
         
        # if not df_period[df_period == 0].isnull().values.any() or not df_period_pred[df_period_pred == 0].isnull().values.any() or len(np.where(np.asarray(df_period.iloc[ : , -1]) == 0)[0]) == total_scale:
        if not df_period[df_period == 0].isnull().values.any() or len(np.where(np.asarray(df_period.iloc[ : , -1]) == 0)[0]) == total_scale:
            continue
         
        df_period['partition'] = pd.Series(train_scale * [0] + validation_scale * [1] + holdout_scale * [2], index = df_period.index)
        if not os.path.exists(filepath_output + '/instru_' + str(ticker)):
            os.makedirs(filepath_output + '/instru_' + str(ticker))
        if not os.path.exists(filepath_pred_original + '/instru_' + str(ticker)):
            os.makedirs(filepath_pred_original + '/instru_' + str(ticker))
            
        df_period.to_csv(filepath_output + '/instru_' + str(ticker) + '/period_' + str(i) + '.csv', index = False)
        df_period_pred.to_csv(filepath_pred_original + '/instru_' + str(ticker) + '/period_' + str(i) + '.csv', index = False)
        
if __name__ == '__main__':
    train_scale = 1250
    validation_scale = 375
    holdout_scale = 1
    predict_scale = 375
    normalization = True
    filepath = './data/indicators_reverson'
    filepath_output = './data/gererated'
    filepath_pred_original = './data/original'
    tickers = os.listdir(filepath)

    if not os.path.exists(filepath_output):
        os.makedirs(filepath_output)
    else:
        for root, dirs, files in os.walk(filepath_output):
            for file in files:
                os.remove(os.path.join(root, file))
                
    if not os.path.exists(filepath_pred_original):
        os.makedirs(filepath_pred_original)
    else:
        for root, dirs, files in os.walk(filepath_pred_original):
            for file in files:
                os.remove(os.path.join(root, file))
                
    for ticker in tickers:
        read_indicators_csv(filepath, filepath_output, filepath_pred_original, ticker, train_scale, validation_scale, holdout_scale, predict_scale, normalization)
            
            