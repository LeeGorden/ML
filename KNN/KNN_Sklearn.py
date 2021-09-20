# -*- coding: utf-8 -*-
"""
@author: LiGorden

KNN-Using Sklearn
"""
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

#Import Data
data = pd.read_csv('../Data/Iris Data/iris.csv')
X, y = np.array(data)[:, :-1], np.array(data)[:, -1]
X_train, X_test, y_train, y_test = \
     train_test_split(X, y, test_size=0.33, shuffle=True, stratify=y, random_state=0)

#Building KNN model with kdTree
clf_sk = KNeighborsClassifier(n_neighbors=3, p=2, algorithm='kd_tree')
clf_sk.fit(X_train, y_train)

#Prediction
prediction = clf_sk.predict(X_test)

#Recall Rate
clf_sk.score(X_test, y_test) 
