# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 00:58:05 2017

@author: Minghui GUAN
"""

import json
import numpy as np
from scipy.spatial.distance import pdist

X=np.zeros([3,3])
X[0]=[1,2,3]
X[1]=[2,3,4]
X[2]=[5,4,6]

n=pdist(X, 'sqeuclidean')

print n

n += 1.

print n, '\n',X[0]-X

print (243-(243%50))/50

Y=[[]]
Y[0]=X
Z=[[]]
Z[0]=[[1,2],[1,3]]

Y.extend(Z)
print Y

A=Y

print A

j = 20
Dict = {}
Dict[str(j)]="nihao"
print Dict
print 50/20

with open(r'E:/Dict_TSNE.json', 'r') as f:
     data = json.load(f)
step = float(data['step'])   

#for key in data :   
#    if (key != 'step'):
data1 = data["100"][1:-1]
data2 =  data1.split('\n')
#        for i in range(len(data2)):
#            data2[i]=data2[i].strip().lstrip('[').rstrip(']').strip().split()
#            data2[i][0]=float(data2[i][0])
#            data2[i][1]=float(data2[i][1])
         
#        data[str(key)] = np.array(data2)
    
print len(data)

Dict = {}
Dict["nihao"]=123
Dict["tamen"]=321
Dict["women"]=951
Dict["lkjkl"]=852
print Dict.keys()



'''def _tsne(self, P, degrees_of_freedom, n_samples, random_state,
              X_embedded=None, neighbors=None, skip_num_points=0):
        """Runs t-SNE."""
        # t-SNE minimizes the Kullback-Leiber divergence of the Gaussians P
        # and the Student's t-distributions Q. The optimization algorithm that
        # we use is batch gradient descent with three stages:
        # * early exaggeration with momentum 0.5
        # * early exaggeration with momentum 0.8
        # * final optimization with momentum 0.8
        # The embedding is initialized with iid samples from Gaussians with
        # standard deviation 1e-4.

        if X_embedded is None:
            # Initialize embedding randomly
            X_embedded = 1e-4 * random_state.randn(n_samples,
                                                   self.n_components)
        params = X_embedded.ravel()

        opt_args = {"n_iter": 50, "momentum": 0.5, "it": 0,
                    "learning_rate": self.learning_rate,
                    "n_iter_without_progress": self.n_iter_without_progress,
                    "verbose": self.verbose, "n_iter_check": 25,
                    "kwargs": dict(skip_num_points=skip_num_points)}
        if self.method == 'barnes_hut':
            m = "Must provide an array of neighbors to use Barnes-Hut"
            assert neighbors is not None, m
            obj_func = _kl_divergence_bh
            objective_error = _kl_divergence_error
            sP = squareform(P).astype(np.float32)
            neighbors = neighbors.astype(np.int64)
            args = [sP, neighbors, degrees_of_freedom, n_samples,
                    self.n_components]
            opt_args['args'] = args
            opt_args['min_grad_norm'] = 1e-3
            opt_args['n_iter_without_progress'] = 30
            # Don't always calculate the cost since that calculation
            # can be nearly as expensive as the gradient
            opt_args['objective_error'] = objective_error
            opt_args['kwargs']['angle'] = self.angle
            opt_args['kwargs']['verbose'] = self.verbose
        else:
            obj_func = _kl_divergence
            opt_args['args'] = [P, degrees_of_freedom, n_samples,
                                self.n_components]
            opt_args['min_error_diff'] = 0.0
            opt_args['min_grad_norm'] = self.min_grad_norm

        # Early exaggeration
        P *= self.early_exaggeration

        params, kl_divergence, it = _gradient_descent(obj_func, params,
                                                      **opt_args)
        opt_args['n_iter'] = 100
        opt_args['momentum'] = 0.8
        opt_args['it'] = it + 1
        params, kl_divergence, it = _gradient_descent(obj_func, params,
                                                      **opt_args)
        if self.verbose:
            print("[t-SNE] KL divergence after %d iterations with early "
                  "exaggeration: %f" % (it + 1, kl_divergence))
        # Save the final number of iterations
        self.n_iter_final = it

        # Final optimization
        P /= self.early_exaggeration
        opt_args['n_iter'] = self.n_iter
        opt_args['it'] = it + 1
        params, error, it = _gradient_descent(obj_func, params, **opt_args)

        if self.verbose:
            print("[t-SNE] Error after %d iterations: %f"
                  % (it + 1, kl_divergence))

        X_embedded = params.reshape(n_samples, self.n_components)
        self.kl_divergence_ = kl_divergence

        return X_embedded

    def fit_transform(self, X, y=None):
        """Fit X into an embedded space and return that transformed
        output.
        Parameters
        ----------
        X : array, shape (n_samples, n_features) or (n_samples, n_samples)
            If the metric is 'precomputed' X must be a square distance
            matrix. Otherwise it contains a sample per row.
        Returns
        -------
        X_new : array, shape (n_samples, n_components)
            Embedding of the training data in low-dimensional space.
        """
        embedding = self._fit(X)
        self.embedding_ = embedding
        return self.embedding_

    def fit(self, X, y=None):
        """Fit X into an embedded space.
        Parameters
        ----------
        X : array, shape (n_samples, n_features) or (n_samples, n_samples)
            If the metric is 'precomputed' X must be a square distance
            matrix. Otherwise it contains a sample per row. If the method
            is 'exact', X may be a sparse matrix of type 'csr', 'csc'
            or 'coo'.
        """
        self.fit_transform(X)
        return self'''