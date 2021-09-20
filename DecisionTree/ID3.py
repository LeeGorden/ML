# -*- coding: utf-8 -*-
"""
DecisionTree-ID3
Nature: Use ΔEntropy(Gain) to judge which feature to use first when split the tree.
        In ID3, each Feature can only be used ONCE when splitting the tree.
Note: In this algorithm, RECURSION is used to build the tree

@author: LiGorden
"""
from collections import Counter
import numpy as np

def load_data(path_of_data_file):
    '''
    Function: Load CSV data into python. The Last row of CSV should be dependent Y.
              Return array X, Y
    '''
    X, Y = [], []
    file=open(path_of_data_file,'r') 
    for row in file:                 
        data = row.strip().split(',')  
        X.append(data[:-1])         
        Y.append(data[-1])          
    file.close()
    return np.array(X), np.array(Y) 

def H(Y):
    '''
    Function: Calculate the Entropy of the imput Y
    '''
    sum = 0
    for key,value in Counter(Y).items():
        '''
        Counter will return a dict:
        dict_items[{key: num_of_corresponding_value, ...}]
        '''
        p = value/len(Y)
        sum -= p * np.log2(p)
    return sum

def Condition_H(X, Y):
    '''
    Function: Calculate the Entropy of Y after apply feature X as a split of Y
    '''
    sum = 0
    for key, value in Counter(X).items():
        sum += (value / len(X)) * H(Y[X == key])
    return sum

class Tree():
    def __init__(self, feature, default):
        '''
        feature: name of variable chosen to split the tree
        default: the default return when current samples to be predicted do not
                 have proper route
        '''
        self.feature = feature
        self.node = {}
        self.default = default
        
    def __repr__(self):
        '''
        Rewrite Print function
        '''             
        return self.feature + '->'+str(self.node)
        
    def addNode(self, key, values):
        self.node[key] = values
    
    def getTree(self, key):     
        return self.node[key] if key in self.node else self.default
        
class DecisionTreeClassifier():
    def __init__(self, min_node_sample):
        '''
        Variable: min_node_sample-Minimum munber of samples on each node
        '''
        self.min_node_sample = min_node_sample
    
    def fit(self, X, Y):
        self.node = self.constructTree(X, Y)
        
    def predict(self, X):
        '''
        Function: Predict the classification of the samples
        Variable: X-Features of samples to be predicted, Including feature name
                  in the first row
        '''
        pass
    
    def constructTree(self, X, Y):
        '''
        Function: Construct a ID3 Tree using RECURSION
        Variables: X-Features with Features' name in the first row
                   Y-Dependent with Dependent's name in the first row
        '''
        #When the set to be classified only has one sample, no need to classify further, the node is pure
        if len(set(Y[1:])) == 1:
            return Y[1]
        #Pre-Cutting, set the threshold as >= min_node_sample each node
        elif len(Y) < self.min_node_sample:         
            #Return the most common result in Y as the result of classification
            return Counter(Y[1:]).most_common(1)[0][0]
            #Counter(np.array).most_common(n) is a list, return the n most common (value, number): [('No', 9), ('Yes', 8)]
        #Since in Method ID3, each Feature can only be used once. When all the Feature is used, stop constructing tree
        elif X.shape[1] == 0:
            return Counter(Y[1:]).most_common(1)[0][0]
        
        #Calculating Gain = H_BeforeSplit - H_AfterSplit = H_Total - H_judge
        H_Total = H(Y[1:])
        Gain_Max = 0
        i_Max = 0
        
        #Judging which Feature brings most Gain, Pick out the chosen Feature
        for i in range(X.shape[1]):
            H_judge = Condition_H(X[1:,i], Y[1:])
            Gain = H_Total-H_judge
            if Gain >= Gain_Max:
                Gain_Max = Gain
                i_Max = i
             
        #Put the chosen Feature name into the Tree, use the most common type as defult
        tree = Tree(X[0,i_Max], Counter(Y[1:]).most_common(1)[0][0])
        #Use set() function to list the unique data in the chosen Feature
        for key in set(X[1:,i_Max]): 
            #index = the unique data of the chosen Feature
            index = X[:,i_Max] == key
            #Feature name needed to be put in tree too. Thus set index[0] = True
            index[0] = True 
            #Remove the chosen feature, and use the picked samples according to the feature to do the recursion
            value = self.constructTree(np.hstack([X[index,:i_Max],X[index,i_Max+1:]]), Y[index])
            tree.addNode(key, value)
        return tree
            

if __name__ == '__main__':
    X, Y = load_data('../Data/Iris Data/iris.csv')
    model = DecisionTreeClassifier(5)
    model.fit(X, Y)
    print(model.node)
    
    

        
        
        

    