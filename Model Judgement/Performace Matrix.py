# -*- coding: utf-8 -*-
"""
Author: LiGorden

Peformance Matrix
"""
import numpy as np
import matplotlib.pyplot as plt

class PerformanceMatrix:
    def __init__(self, y_pred, y_real, Positive_std=0.5):
        '''
        Function: Create the performance matrix according to the method input
        Variable: y_pred is the predicted labels
                  y_pred should be array posibililty
                  y_real is the real labels
                  y_real should be array True/False(1/0)
        '''
        self.y_pred = y_pred
        self.y_real = y_real
        self.Positive_std = Positive_std
        self.TP, self.FP, self.TN, self.FN = self._indicator(self.y_pred, self.y_real, self.Positive_std)
    
    def _indicator(self, y_pred, y_real, Positive_std):
        '''
        Function: Calculate TP, FP, FN, TN
        '''
        y_pred = y_pred > Positive_std
        #True Positive
        ind = y_pred == 1
        TP = sum(y_pred[ind] == y_real[ind])
        #False Positive(Type I error)
        FP = sum(y_pred[ind] != y_real[ind])
        
        #True Negative
        ind = y_pred != 1
        TN = sum(y_pred[ind] == y_real[ind])
        #False Negative(Type II error)
        FN = sum(y_pred[ind] !=  y_real[ind])
        return TP, FP, TN, FN
    
    def TPR(self):
        '''
        Sensitivity
        '''
        return self.TP / (self.TP + self.FN)
    
    def FPR(self):
        return self.FP / (self.FP + self.TN)    
    
    def TNR(self):
        '''
        Specifity
        '''
        return self.TN / (self.TN + self.FP)
    
    def FNR(self):
        return self.FN / (self.FN + self.TP)
    
    def Recall(self):
        return self.TP / (self.TP + self.FN)  
    
    def Precision(self):
        return self.TP/ (self.TP + self.FP)
    
    def Accuracy(self):
        return (self.TP + self.TN)/ (self.TP + self.TN + self.FP + self.FN)
    
    def F_score(self):
        return 2/((1/self.Recall())+(1/self.Precision()))
    
    def plot(self, method='ROC'):
        TPR_Recall = []
        FPR = []
        Precision = []
        
        for std in np.linspace(max(self.y_pred)-0.01, min(self.y_pred)-0.01, 100):
            TP, FP, TN, FN = self._indicator(self.y_pred, self.y_real, std)
            TPR_Recall.append(TP / (TP + FN))
            FPR.append(FP / (FP + TN))
            Precision.append(TP/ (TP + FP))
        print(TPR_Recall)
        print(FPR)
        print(Precision)
        if method == 'ROC':
            plt.title('ROC Curve')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.plot(FPR, TPR_Recall)
            plt.show()
        elif method == 'RC':
            plt.title('RC Curve')
            plt.xlabel('Recall Rate')
            plt.ylabel('Precision Rate')
            plt.plot(TPR_Recall, Precision)
            plt.show()
    
if __name__ == '__main__':
    y_real = np.array([1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0])
    y_pred = np.array([0.95, 0.85, 0.80, 0.67, 0.65, 0.60, 0.58, 0.54, 0.52, 0.51, \
                        0.45, 0.40, 0.38, 0.35, 0.33, 0.30, 0.28, 0.27, 0.26, 0.18])
    
    PM = PerformanceMatrix(y_pred, y_real)
    print('Answer:--------------------')
    print(PM.FPR())
    print(PM.TPR())
    print(PM.FP)
    print(PM.FN)
    print(PM.Precision())
    print(PM.Recall())
    print(PM.TPR())
    print(PM.TNR())
    print(PM.Accuracy())
    print(PM.F_score())
    PM.plot(method='ROC')
    PM.plot(method='RC')
    
