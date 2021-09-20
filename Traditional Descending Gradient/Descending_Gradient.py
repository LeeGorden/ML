# -*- coding: utf-8 -*-
"""
Descending Gradient
@author: LiGorden
"""
import numpy as np

def loss_function(y,y_hat):
    '''
    Function: Design Loss_Function, here is (y_hat - y_real)^2
    '''
    return np.mean((y_hat-y)**2)

def partial_deritive(x, y, y_hat):
    '''
    Function: Calculate the Partial derivative of β in LINEAR REGRESSION for 
              Gradient Decent
    '''
    return (y_hat - y).dot(x)/len(x)

def add_bias(x):
    '''
    Function: Adding Intercept to x array, Default Intercept as 1
    '''
    return np.hstack([np.ones([x.shape[0],1]),x])

class LinearRegression():
    def __init__(self, learning_rate):
        self.α = learning_rate
        self.coef = None
        self.loss_history = []
    
    def fit(self, x, y, max_iterations):
        x = add_bias(x)
        self.coef = np.zeros(x.shape[1])
        for i in range(max_iterations):
            y_hat=self._forward(x)
            self._backward(x, y, y_hat)
            self.loss_history.append(loss_function(y, y_hat))
            print(i, self.coef)
            
    def predict(self, x):
        x=add_bias(x)
        return self._forward(x)
    
    def _forward(self, x):
        '''
        Function: Calculating the result matrix of X·b  = x·b + b_0
        '''
        return x.dot(self.coef)
    
    def _backward(self, x, y, y_hat):
        '''
        Function: Calculating movement of each β according to the partial deritives 
                  calculated for each parameter, and out put a coef vector
        '''
        delta = partial_deritive(x, y, y_hat)
        self.coef -= self.α*delta
    
if __name__ == '__main__':
    import pandas as pd
    data = pd.read_csv('linear_regression_data.csv')
    X = data.iloc[:, :-1]
    Y = data.iloc[:, -1]
    
    model = LinearRegression(learning_rate=0.01)
    model.fit(X, Y, 1000)
    pred_y = model.predict(X)
    print(model.coef)
    model.loss_history

