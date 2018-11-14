# -*- coding: utf-8 -*-

# load useful libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing,linear_model, metrics
import time
# %matplotlib inline

np.random.seed(1)

# we display the description of the features
with open('data/features.txt', 'r') as f:
    for line in f:
        print(line)
#!cat data/kaggle_data/features.txt
        
feature_data = pd.read_csv('data/features.txt', header=None, sep="  ", engine='python', names=['feature_names', 'feature_description'])
feature_data.head(5)

feature_data.shape

target_data = pd.read_csv('data/train-targets.csv', sep=",")
target_data.head(5)

y_tr = target_data['Prediction'].values
plt.hist(y_tr,bins=2000)
plt.xlim((0,10000))

list_feature_names = list(feature_data['feature_names'])

train_data = pd.read_csv('data/train.csv', header=None, sep=" ", names=list_feature_names)
train_data.head(10)

test_data = pd.read_csv('data/test-val.csv', header=None, sep=" ", names=list_feature_names)
test_data.head(5)

from pandas import scatter_matrix
figure1 = scatter_matrix(train_data.get(["nb_words_content", "pp_uniq_words"]), alpha=0.2,
               figsize=(6, 6), diagonal='kde')
plt.savefig(r"Pictures for report\figure_1.png")

import seaborn.apionly as sns
sns.set_style('whitegrid')
sns.jointplot("nb_words_content", "pp_uniq_words", data = train_data, 
              kind='reg', size=6, space=0, color='b')
plt.savefig(r"Pictures for report\figure_2.png")

# let's redefine the cross-validation procedure with standardization
from sklearn import preprocessing
def cross_validate_scaling(design_matrix, labels, regressor, cv_folds):
    """ Perform a cross-validation and returns the predictions. 
    Use a scaler to scale the features to mean 0, standard deviation 1.
    
    Parameters:
    -----------
    design_matrix: (n_samples, n_features) np.array
        Design matrix for the experiment.
    labels: (n_samples, ) np.array
        Vector of labels.
    classifier:  Regressor instance; must have the following methods:
        - fit(X, y) to train the regressor on the data X, y
        - predict_proba(X) to apply the trained regressor to the data X and return predicted values
    cv_folds: sklearn cross-validation object
        Cross-validation iterator.
        
    Return:
    -------
    pred: (n_samples, ) np.array
        Vectors of predictions (same order as labels).
    """

    pred = np.zeros(labels.shape)
    for tr, te in cv_folds:
        scaler = preprocessing.StandardScaler()
        Xtr = scaler.fit_transform(design_matrix[tr,:])
        ytr =  labels[tr]
        Xte = scaler.transform(design_matrix[te,:])
        regressor.fit(Xtr, ytr)
        pred[te] = regressor.predict(Xte)
    return pred

def cross_validate_optimize(design_matrix,labels,regressor,cv_folds):
    pred = np.zeros(labels.shape)
    for (tr,te) in cv_folds:
        scaler = preprocessing.StandardScaler()
        X_tr = scaler.fit_transform(design_matrix[tr,:])
        y_tr = labels[tr]
        X_te = scaler.transform(design_matrix[te,:])
        
        regressor.fit(X_tr, y_tr)
        print(regressor.best_params_)
        pred[te]=regressor.best_estimator_.predict(X_te)
    return pred

# Binarize weekday
weekday_or_weekend = (train_data['weekday'] > 4) * 1
weekday_or_weekend_data = pd.get_dummies(weekday_or_weekend, prefix='weekday_or_weekend', drop_first=True)

train_data = pd.concat([weekday_or_weekend_data, train_data], axis=1)
train_data.head()

weekday_or_weekend = (test_data['weekday'] > 4) * 1
weekday_or_weekend_data = pd.get_dummies(weekday_or_weekend, prefix='weekday_or_weekend', drop_first=True)
test_data = pd.concat([weekday_or_weekend_data, test_data], axis=1)
test_data.head()

# Get the weekday data and encode it using a dummy categorical encoding
weekday_data = pd.get_dummies(train_data['weekday'], prefix='weekday', drop_first=True)

# Get the rest of the data
other_data = train_data.drop(['weekday'], axis=1)

# Create a new data set by concatenation of the new weekday data and the old rest of the data
training_data = pd.concat([weekday_data, other_data], axis=1)

# Print the created training data.
training_data.head(5)

# Get the catogary data and encode it using a dummy categorical encoding
category_data = pd.get_dummies(training_data['category'], prefix='category', drop_first=True)

# Get the rest of the data
other_data = training_data.drop(['category'], axis=1)

# Create a new data set by concatenation of the new weekday data and the old rest of the data
training_data = pd.concat([category_data, other_data], axis=1)

# Do the same things to the test data
# Weekday
weekday_data = pd.get_dummies(test_data['weekday'], prefix='weekday', drop_first=True)
other_data = test_data.drop(['weekday'], axis=1)
testing_data = pd.concat([weekday_data, other_data], axis=1)

# Category
category_data = pd.get_dummies(testing_data['category'], prefix='category', drop_first=True)
other_data = testing_data.drop(['category'], axis=1)
testing_data = pd.concat([category_data, other_data], axis=1)

training_data.head()

testing_data.head()

X_tr = training_data.values
X_te = testing_data.values
y_tr = target_data['Prediction'].values

target_data['Prediction'].values

# set up folds for cross_validation
from sklearn import model_selection
kf = model_selection.KFold(n_splits=5)
kf.get_n_splits(X_tr)
folds = [(tr, te) for (tr, te) in kf.split(X_tr)]

from sklearn import preprocessing

std_scale = preprocessing.StandardScaler().fit(X_tr)
X_scaled = std_scale.transform(X_tr)

from sklearn.feature_selection import RFECV
from sklearn.svm import SVR
estimator = SVR(kernel="linear")
selector = RFECV(estimator, step=1, cv=5, scoring= 'neg_mean_squared_error')
selector = selector.fit(X_scaled, y_tr)
selector.support_
selector.ranking_

X_tr_rfe = selector.transform(X_scaled)
X_tr_rfe.shape

from sklearn.svm import SVR
from sklearn.metrics import mean_squared_log_error

kf.get_n_splits(X_tr_rfe)
folds_svr_rfe = [(tr, te) for (tr, te) in kf.split(X_tr_rfe)]
svr = SVR(C = 1000)
ypred_svr_rfe = cross_validate_scaling(X_tr_rfe, y_tr, svr, folds_svr_rfe)
print(metrics.mean_squared_error(y_tr, ypred_svr_rfe))
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(ypred_svr_rfe)))))

svr = SVR(C = 1000)
svr.fit(X_tr_rfe, y_tr)
X_te_scaled = std_scale.transform(X_te)
X_te_rfe = selector.transform(X_te_scaled)
pred_te = svr.predict(X_te_rfe)

raw_data = {'Id': [i for i in range(2000)], 'Prediction': abs(pred_te) }
df = pd.DataFrame(raw_data, columns = ['Id', 'Prediction'])
df.to_csv("test.csv", sep=",", index=False,float_format='%.f')

features = [i for i in range(X_tr.shape[1])]

def processSubset(regr, feature_set = [0,1]):
    # Fit model on feature_set and calculate RSS
    X_tr_sub = X_tr[:, feature_set]
    ypred = cross_validate_scaling(X_tr_sub, y_tr_log, regr, folds)
    RMLSE = np.sqrt(metrics.mean_squared_error(np.log(y_tr), ypred))
    dict_test = {"model": feature_set, "RMLSE":RMLSE}
    return dict_test

def forward(predictors, regr = linear_model.LinearRegression()):
    # Pull out predictors we still need to process
    remaining_predictors = [p for p in features if p not in predictors]
    tic = time.time()
    results = []
    for p in remaining_predictors:
        predictors.append(p)
        results.append(processSubset(regr, predictors))
        predictors = predictors[:-1]
                       
    # Wrap everything up in a nice dataframe
    models = pd.DataFrame(results)
    # Choose the model with the highest RSS
    best_model = models.loc[models['RMLSE'].argmin()]
    toc = time.time()
    print("Processed ", models.shape[0], "models on", len(predictors)+1, "predictors in", (toc-tic), "seconds.", "RMSLE",models['RMLSE'].min() )
    # Return the best model, along with some other useful information about the model
    return best_model

import copy
def backward(predictors, regr = linear_model.LinearRegression()):
    # Pull out predictors we still need to process
    remaining_predictors = copy.deepcopy(predictors)
    tic = time.time()
    results = []
    for p in remaining_predictors:
        predictors.remove(p)
        results.append(processSubset(regr, copy.deepcopy(predictors)))
        predictors.append(p)
                       
    # Wrap everything up in a nice dataframe
    models = pd.DataFrame(results)
    # Choose the model with the highest RSS
    best_model = models.loc[models['RMLSE'].argmin()]
    toc = time.time()
    print("Processed ", models.shape[0], "models on", len(predictors), "predictors in", (toc-tic), "seconds.", "RMSLE",models['RMLSE'].min())
    # Return the best model, along with some other useful information about the model
    return best_model

import copy
#predictors = [i for i in range(X_tr.shape[1])]
#models3 = pd.DataFrame(columns=["model", "RMLSE"])
predictors = [31, 34]
models3 = pd.DataFrame(columns=["model", "RMLSE"])
for i in range(1,2):
    models3.loc[i] = backward(predictors, regr = SVR(C = 1.8))
    predictors = models3.loc[i].model
    
from sklearn import decomposition, preprocessing

std_scale = preprocessing.StandardScaler().fit(X_tr)
X_tr_scaled = std_scale.transform(X_tr)

pca = decomposition.PCA(n_components=10)
pca.fit(X_tr_scaled)

X_tr_projected = pca.transform(X_tr_scaled)

plt.bar(np.arange(10), pca.explained_variance_ratio_, color='blue')
plt.xlim([-1, 9])
plt.xlabel("Number of PCs", fontsize=16)
plt.ylabel("Fraction of variance explained", fontsize=16)
plt.savefig(r"Pictures for report\figure_3.png")

# create figure and axis objects
fig, ax = plt.subplots(figsize=(6, 5))
# create scatterplot on axis N.B. we record the return value to feed to the colorbar
cax = ax.scatter(X_tr_projected[:, 0], X_tr_projected[:, 1], c=y_tr_log,
                 cmap=plt.get_cmap('plasma'))
# Set axis limits
#ax.set_xlim([-5.5, 5.5])
#ax.set_ylim([-4, 4])
# Create color bar
plt.colorbar(cax, label='Rank')
#plt.savefig(r"Pictures for report\figure_4.png")

from sklearn.svm import SVR
from sklearn import decomposition, preprocessing
from sklearn.ensemble import RandomForestRegressor
class PCA_Regr():
    """ Class for PCA + regression:
    
    Attributes:
    -----------
    
    """
    def __init__(self, n_components = 10, regr = linear_model.LinearRegression()):
        self.coef_ = None
        self.n_components = n_components
        self.std = None
        self.pca = None
        self.regr = regr
        
    def fit(self, X, y):
        """ Fit the data (X, y).        
        """
        std_scale = preprocessing.StandardScaler().fit(X)
        self.std = std_scale
        X_scaled = self.std.transform(X)

        pca = decomposition.PCA(n_components=self.n_components)
        pca.fit(X_scaled)
        self.pca = pca
        
        X_projected = pca.transform(X_scaled)
        self.regr.fit(X_projected, y)
        
    def predict(self, X):
        """ Make predictions for data X.
    
        Parameters:
        -----------
        X: (num_samples, num_features) np.array
            Design matrix
        
        Returns:
        -----
        y_pred: (num_samples, ) np.array
            Predictions
        """
        X_scaled = self.std.transform(X)
        X_projected = self.pca.transform(X_scaled)
        pred = self.regr.predict(X_projected)
        
        return pred
    
from sklearn import ensemble
error_pca = []
for k in range(1, 50):
    regr_pca = PCA_Regr(k, linear_model.LinearRegression())
    pred = cross_validate_scaling(X_tr, np.log(y_tr), regr_pca, folds)
    print("pca", k, "Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred)))))
    error_pca.append(metrics.mean_squared_error(y_tr, np.exp(pred)))
    
pred = cross_validate_scaling(X_tr, y_tr, linear_model.LinearRegression(), folds)
print("pca", k, "Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred)))))

from sklearn import linear_model
regr_linear = linear_model.LinearRegression()
ypred_linear = cross_validate_scaling(X_tr, y_tr, regr_linear, folds)
print(metrics.mean_squared_error(y_tr, ypred_linear))
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(y_tr_log, np.log(abs(ypred_linear)))))

from sklearn import linear_model

parameters = {'alpha': np.logspace(-4, 1, 10)}

regr_lasso = linear_model.Lasso()
regr_lasso_opt = model_selection.GridSearchCV(regr_lasso, parameters, cv=3)
regr_lasso_opt.fit(X_tr, y_tr_log)
ypred_lasso = cross_validate_scaling(X_tr, y_tr_log, regr_lasso_opt.best_estimator_, folds)
#ypred_lasso = cross_validate_scaling(X_tr, y_tr, regr_lasso, folds)
print(metrics.mean_squared_error(y_tr, ypred_lasso))
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), ypred_lasso)))

num_features = X_tr.shape[1]
plt.scatter(range(num_features), regr_lasso_opt.best_estimator_.coef_,#TODO, 
            color='orange', marker='+', label='L1-regularized linear regression')


plt.xlabel('Features', fontsize=16)
plt.ylabel('Weights', fontsize=16)
plt.title('Linear regression weights', fontsize=16)
plt.legend(fontsize=14, loc=(1.05, 0))
plt.xlim([0, num_features])

print("The L1-regularized logistic regression uses %d features" %len(np.where(regr_lasso_opt.best_estimator_.coef_ != 0)[0]))
plt.savefig(r"Pictures for report\figure_5.png")


parameters = {'alpha': np.logspace(-4, 1, 10)}

regr_ridge = linear_model.Ridge()
regr_ridge_opt = model_selection.GridSearchCV(regr_ridge, parameters, cv=3)
regr_ridge_opt.fit(X_tr, y_tr_log)
ypred_ridge = cross_validate_scaling(X_tr, y_tr_log, regr_ridge_opt.best_estimator_, folds)
#ypred_lasso = cross_validate_scaling(X_tr, y_tr, regr_lasso, folds)
print(metrics.mean_squared_error(y_tr, ypred_ridge))
print("Root mean squared logarithmic error: %.5f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), ypred_ridge)))

X_tr_lasso = X_tr[:,np.where(regr_lasso_opt.best_estimator_.coef_ != 0)[0]]
y_tr_lasso = y_tr

from sklearn.neighbors import KNeighborsRegressor

parameters = {'n_neighbors': [55,56,57,58,59]}

neigh = KNeighborsRegressor()
neigh_opt = model_selection.GridSearchCV(neigh, parameters, cv=3)
neigh_opt.fit(X_tr, y_tr_log)
print(neigh_opt.best_estimator_)
ypred_neigh = cross_validate_scaling(X_tr, y_tr_log, neigh_opt.best_estimator_, folds)

print(metrics.mean_squared_error(y_tr, ypred_neigh))
print("Root mean squared logarithmic error: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, ypred_neigh)))

error_pca = []
for k in range(1, 50):
    regr_pca = PCA_Regr(k, neigh_opt.best_estimator_)
    pred = cross_validate_scaling(X_tr, y_tr_log, regr_pca, folds)
    print("pca", k, "Root mean squared logarithmic error: %.5f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), pred)))
    error_pca.append(metrics.mean_squared_error(y_tr, pred))
    
svr = SVR(C=1.8, kernel='rbf')
ypred_svr = cross_validate_scaling(X_tr, y_tr_log, svr, folds)
print("Root mean squared logarithmic error: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, ypred_svr)))

from sklearn.svm import SVR

parameters = {'C': [1.8], 'kernel':['rbf', 'linear']}
svr = SVR()
svr_opt = model_selection.GridSearchCV(svr, parameters, cv=3)
svr_opt.fit(X_tr, y_tr_log)
print(svr_opt.best_estimator_)
ypred_svr = cross_validate_scaling(X_tr, y_tr_log, svr_opt.best_estimator_, folds)
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(y_tr_log, ypred_svr)))

svr_opt.best_estimator_

from sklearn.svm import SVR
kf.get_n_splits(X_tr_lasso)
folds_svr_lasso = [(tr, te) for (tr, te) in kf.split(X_tr_lasso)]
svr = SVR(C = 1000)
ypred_svr_lasso = cross_validate_scaling(X_tr_lasso, y_tr_lasso, svr, folds_svr_lasso)
print(metrics.mean_squared_error(y_tr_lasso, ypred_svr_lasso))
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr_lasso), np.log(abs(ypred_svr_lasso)))))

error_pca_svr_lasso = []
svr = SVR(C=1000)
for k in range(1, 2):
    regr_pca = PCA_Regr(k, svr)
    pred_pca_svr_lasso = cross_validate_scaling(X_tr_lasso, y_tr_lasso, regr_pca, folds_svr_lasso)# TODO
    print("pca", k, "Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr_lasso), np.log(abs(pred_pca_svr_lasso)))))
    
from sklearn import ensemble, model_selection
rf = ensemble.RandomForestRegressor()
ypred_rf_lasso = cross_validate_scaling(X_tr_lasso, y_tr_lasso, rf, folds_svr_lasso)
print(metrics.mean_squared_error(y_tr_lasso, ypred_rf_lasso))
print("Root mean squared logarithmic error: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr_lasso), np.log(abs(ypred_rf_lasso)))))


parameters = {'n_estimators':[i for i in range(1,20)]}
classifier = ensemble.RandomForestRegressor()

RF_opt = model_selection.GridSearchCV(classifier, parameters, cv=3)

rf = ensemble.RandomForestRegressor()
pred = cross_validate(X_tr, y_tr, rf, folds)
print("RMSLE: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred)))))

from sklearn.svm import SVR
parameters = {'C': np.logspace(3, 4, 20), 'kernel': ['rbf']}
svr = SVR()
svr_opt = model_selection.GridSearchCV(svr, parameters, cv=folds)  
svr_opt.fit(X_tr_scaled, y_tr)
pred_te = svr_opt.best_estimator_.predict(X_te_scaled)

pred_tr = svr_opt.best_estimator_.predict(X_scaled)
print("RMSLE: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(pred_tr))))

svr_opt.best_estimator_

from sklearn.svm import SVR
error_svr = {}
for e in np.linspace(0.01, 1, 20):
    svr = SVR(C = 1000, epsilon= e)
    pred = cross_validate(X_tr, y_tr, svr, folds)
    print("RMSLE: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred)))))
    error_svr[str(e)] = np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred))))
    
from sklearn import neighbors
knn = neighbors.KNeighborsRegressor(n_neighbors=30)
pred = cross_validate(X_tr, y_tr, knn, folds)
print("RMSLE: %.3f" % np.sqrt(metrics.mean_squared_error(np.log(y_tr), np.log(abs(pred)))))

from sklearn.svm import SVR
svr = SVR(C = 300, kernel = 'rbf')

std_scale = preprocessing.StandardScaler().fit(X_tr)
X_scaled = std_scale.transform(X_tr)
X_te_scaled = std_scale.transform(X_te)
    
svr.fit(X_scaled, y_tr)
pred_te = svr.predict(X_te_scaled)

from sklearn import model_selection, ensemble
# Define the grid of parameters to test
param_grid = {'max_features':['sqrt','log2'],'min_samples_leaf':[4,5,6], 'n_estimators':[200,250,350,400]}# TODO
y_tr_log = np.log(y_tr)

# Initialize a GridSearchCV object that will be used to cross-validate
# a random forest with these parameters.
rf = model_selection.GridSearchCV(ensemble.RandomForestRegressor(), param_grid, scoring='neg_mean_squared_error')
rf.fit(X_tr, y_tr_log)
print(rf.best_estimator_)

pred_rf_log = cross_validate_scaling(X_tr, y_tr_log, rf.best_estimator_, folds)
print("RMSLE: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, pred_rf_log)))

rf.best_estimator_.feature_importances_

print("RMSLE: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, pred_rf_log)))

rf_best = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='sqrt', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=7, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=500, n_jobs=1,
           oob_score=False, random_state=None, verbose=0, warm_start=False)
#RMSLE: 0.84806
pred_rf_best_log = cross_validate_scaling(X_tr, y_tr_log, rf_best, folds)
print("RMSLE: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, pred_rf_best_log)))

select = rf_best.feature_importances_.argsort()
select = select[::-1]

tree_based_feature_selection = SelectFromModel(estimator=rf.best_estimator_, 
                                               threshold='mean')
tree_based_feature_selection.fit(X, y)
print('number of selected features by random forest:', len(tree_based_feature_selection.get_support(indices=True)))


neigh = KNeighborsRegressor(n_neighbors= 57)
subset = select[:6]
X_tr_sub = X_tr[:, subset]
X_te_sub = X_te[:, subset]

pred_neigh_sub = cross_validate_scaling(X_tr_sub, y_tr_log, neigh, folds)
print("RMSLE: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, pred_neigh_sub)))


rf_sub = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=None,
           max_features='log2', max_leaf_nodes=None,
           min_impurity_decrease=0.0, min_impurity_split=None,
           min_samples_leaf=5, min_samples_split=2,
           min_weight_fraction_leaf=0.0, n_estimators=400, n_jobs=1,
           oob_score=False, random_state=None, verbose=0, warm_start=False)

subset = select[:40]
X_tr_sub = X_tr[:, subset]
X_te_sub = X_te[:, subset]

pred_rf_sub = cross_validate_scaling(X_tr_sub, y_tr_log, rf_sub, folds)
print("RMSLE: %.5f" % np.sqrt(metrics.mean_squared_error(y_tr_log, pred_rf_sub)))

data_fig_6=pd.read_csv('CSV_for_report/model_forward(SVR(C=1.8)).csv',sep=',')
data_fig_6.head(5)
fig_6_y=np.array(data_fig_6['RMLSE'])
plt.plot(range(len(fig_6_y))+np.ones(len(fig_6_y)),fig_6_y,'x-')
#plt.title('figure 6',fontsize=14)
plt.ylabel('RMLSE',fontsize=14)
plt.xlabel('number of features',fontsize=14)
plt.savefig(r"Pictures for report\figure_6.png")

std_scale = preprocessing.StandardScaler().fit(X_tr)
X_tr_scaled = std_scale.transform(X_tr)
X_te_scaled = std_scale.transform(X_te)

rf_best.fit(X_tr_scaled, y_tr_log)
pred_te_log = rf.predict(X_te_scaled)
pred_te = np.exp(pred_te_log)

rf.best_estimator_

subset = [31, 34, 23, 29, 11, 0]
X_tr_sub = X_tr[:, subset]
X_te_sub = X_te[:, subset]

std_scale = preprocessing.StandardScaler().fit(X_tr_sub)
X_tr_sub_scaled = std_scale.transform(X_tr_sub)
X_te_sub_scaled = std_scale.transform(X_te_sub)

neigh_sub = KNeighborsRegressor(n_neighbors=57)
neigh_sub.fit(X_tr_sub_scaled, y_tr_log)
pred_te_log = neigh_sub.predict(X_te_sub_scaled)
pred_te = np.exp(pred_te_log)

svr = SVR(C = 950)
svr.fit(X_tr_sub_scaled, y_tr)
pred_te = svr.predict(X_te_sub_scaled)

raw_data = {'Id': [i for i in range(2000)], 'Prediction': np.absolute(pred_te) }
df = pd.DataFrame(raw_data, columns = ['Id', 'Prediction'])
df.to_csv("test.csv", sep=",", index=False,float_format='%.f')
    











