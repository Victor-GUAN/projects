# -*- coding: utf-8 -*-

inp = "./data/gererated/dataset.csv"
TMP = "./data"
RES = "./res"
out = "./res/output.csv"
sep = ","
MAX_WAIT = 600 # min allowed to fit the model
PROCESS = 20 # number of upload allowed in parallel
WORKERS = 80 # number of process of the pool used

ENDPOINT = "http://XXXXXXXXXXXXXXXXXXXXXXXXX"

ACCOUNTS = [
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        {"api_token" : "XXXXXXXXXXXXXXXXXXXXXXXXX"},
        ]

MODEL_NAMES = [
                'Auto-tuned Stochastic Gradient Descent Regression', 'Decision Tree Regressor', 'Dropout Additive Regression Trees Regressor', 
                'Elastic-Net Regressor', 'ExtraTrees Regressor', 'eXtreme Gradient Boosted Trees Regressor', 'Generalized Additive Model',
                'Linear Regression', 'RandomForest Regressor', 'Gradient Boosted Greedy Trees Regressor', 'K-Nearest Neighbors Regressor'
                'Lasso Regressor', 'Light Gradient Boosted Trees Regressor with Early Stopping', 'Light Gradient Boosting on Elastic-Net Predictions',
                'Mean Response Regressor', 'Rigde Regression', 'Ridge Regressor', 'Support Vector Regressor', 'TensorFlow Deep Learning Regressor'
            ]

import csv
import os
import time
import datarobot
import glob
import logging
import pandas as pd
import itertools
from multiprocessing import Semaphore, Pool
from datarobot.models.modeljob import wait_for_async_model_creation
from datetime import timedelta
from collections import defaultdict
from time import sleep

logging.basicConfig(level = logging.INFO, format = '%(relativeCreated)6d %(threadName)s %(message)s')

class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret
        
def newCSV(key, fieldnames):
    f = open(os.path.join(TMP, key.replace(" ", "_").replace(":", "") + ".csv"), "wb")
    csvwriter = csv.DictWriter(f, fieldnames = fieldnames)
    csvwriter.close = lambda: f.close()
    csvwriter.writeheader()
    return csvwriter

start = time.time()

newfiles = None

with open(inp, 'rb') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter = sep)
    fieldnames = ['index'] + csvreader.fieldnames
    newfiles = keydefaultdict(lambda key: newCSV(key, fieldnames))
    i = 0
    for row in csvreader:
        csvwriter = newfiles[row["stock"]]
        row['index'] = i
        csvwriter.writerow(row)
        i += 1

for csvwriter in newfiles.values():
    csvwriter.close()
    
endREWRITEDATA = time.time()
print(timedelta(seconds = endREWRITEDATA - start))

# Global dataframe used for merge
globalDF = os.path.join(RES, 'result.csv')
with open(globalDF, 'w') as W:
    W.write("row_id, partition_id, prediction\r\n")
    
# Semaphore of upload
semUP = Semaphore(PROCESS)

#Semaphore of joint
semJOIN = Semaphore()

def code(pathtoken, globalDF, OUT, endpoint, model_name_to_use):
    global RES
    
    path = pathtoken["path"]
    logging.info(">>>>" + path + "<<<< (" + pathtoken["token"] + ")")
    
    # launching of the client DR
    datarobot.Client(
            token = pathtoken["token"],
            endpoint = endpoint,
            )
    
    # creation of the project
    ## point of the synchronization
    with semUP:
        created = False
        while not created:
            try:
                pj = datarobot.Project.start(
                        path,
                        project_name = os.path.splitext(os.path.basename(path))[-2],
                        target = 'target',
                        metric = 'RMSE',
                        autoplot_on = False,
                        partitioning_method = datarobot.partitioning_methods.UserTVH(
                                "partition",
                                "train",
                                "validation",
                                None
                                )
                        )
                created = True
            except datarobot.errors.ClientError as e:
                logging.error(e.message)
                return None
            except Exception as e:
                logging.info(path + ">UPLOAD RESTART")
                logging.warning(e.message)
                created = False
                
    logging.info(pj.project_name + ">SETUP")
    
    # search and training of the Blueprints
    bp = filter(lambda bp: bp.model_type == model_name_to_use, pj.get_blueprints())[0]
    mid = pj.train(bp, sample_pct = pj.max_train_pct)
    mod = wait_for_async_model_creation(project_id = pj.id, model_job_id = mid, max_wait = MAX_WAIT)
    logging.info(pj.project_name + ">TRAINED")
    
    # prediction on the validation set
    pid = mod.request_training_prediction(datarobot.enums.DATA_SUBSET.VALIDATION_AND_HOLDOUT)
    pred = pid.get_result_when_complete()
    logging.info(pj.project_name + ">PREDICTION ENDED")
    
    # download of the predictions
    output = os.path.join(OUT, "result_" + pj.project_name + ".csv")
    download = False
    while not download:
        try:
            pred.download(output)
            download = True
        except:
            sleep(0.5)
            logging.info(pj.project_name + ">PREDICTION DOWNLOAD RESTART")
            download = False
            
    logging.info(pj.project_name + ">DOWNLOAD ENDED")
    
    # concatenation of the content in globalDF
    with semJOIN:
        with open(globalDF, 'a') as gdf:
            with open(output, 'rb') as new:
                new.readline()
                gdf.write(new.read())
                
    os.remove(output)
    logging.info(pj.project_name + ">PREDICTION MERGED")

    download_jar = False
    while not download_jar:
        try:
            mod.download_scoring_code(os.path.join(OUT, pj.project_name + "_" + mod.id + ".jar"))
            download_jar = True
        except:
            sleep(0.5)
            logging.info(pj.project_name + ">JAR DOWNLOAD RESTART")
            download_jar = False
    logging.info(pj.project_name + ">JAR DOWNLOAD ENDED")

    logging.info(pj.project_name + ">END")

def code_2(pathtoken, model_name_to_use):
    return code(pathtoken, globalDF, RES, ENDPOINT, model_name_to_use)     

p = Pool(WORKERS)
paths = glob.glob(os.path.abspath(os.path.join(TMP, "*.csv")))
N = len(ACCOUNTS)
dispatch = [
        {
           "path": path,
           "token": ACCOUNTS[i % N]["api_token"]
        }
        for i, path in enumerate(paths)
    ]

params = list(itertools.product(dispatch, MODEL_NAMES))
    
for r in p.imap_unordered(code_2, params):
    r

logging.info(">>>>GLOBAL ALL RUN")

df = pd.read_csv(os.path.join(RES, "result.csv"))
del df['partition_id']
df = df.set_index('row_id')
df.sort_index(inplace = True)

inpDF = pd.read_csv(inp, sep = sep)

final = pd.concat([inpDF, df], axis = 1, sort = False, join = 'inner')
final.to_csv(out, index = False)

endPROJECTS = time.time()
print(timedelta(seconds = endPROJECTS - endREWRITEDATA))

