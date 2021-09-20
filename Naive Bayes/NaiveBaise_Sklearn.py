# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd
from sklearn import datasets
from utils import train_test_split, normalize, accuracy_score, Plot

data = pd.read_csv('..\Data\Iris Data\iris.csv')

class NaiveBayes():
    #NB_Type: 朴素贝叶斯的类型：多项式(离散变量)、高斯(连续变量)、伯努利(布尔变量)
    def __init__(self, NB_Type):
        self.type = NB_Type

    def fit(self, X, y):
        self.X = X
        self.y = y
        #读取独特的变量作为array输出，这里是作为类别输出。
        self.classes = np.unique(y)
        self.parameters = {}
        
        #enumerate()起到的是遍历作用
        #seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        #beta = list(enumerate(seasons, start=1))       
        # 下标从 1 开始[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
        for i, c in enumerate(self.classes):
            # 计算每个种类的平均值，方差，先验概率
            X_Index_c = X[np.where(y == c)] #np.where只对array生效
            X_index_c_mean = np.mean(X_Index_c, axis=0, keepdims=True)
            X_index_c_var = np.var(X_Index_c, axis=0, keepdims=True)
            parameters = {"mean": X_index_c_mean, "var": X_index_c_var, "prior": X_Index_c.shape[0] / X.shape[0]}
            self.parameters["class" + str(c)] = parameters

    def _pdf(self, X, classes):
        # 一维高斯分布的概率密度函数
        # eps为防止分母为0
        eps = 1e-4
        mean = self.parameters["class" + str(classes)]["mean"]
        var = self.parameters["class" + str(classes)]["var"]

        # 取对数防止数值溢出
        # numerator.shape = [m_sample,feature]
        numerator = np.exp(-(X - mean) ** 2 / (2 * var + eps))
        denominator = np.sqrt(2 * np.pi * var + eps)

        # 朴素贝叶斯假设(每个特征之间相互独立)
        # P(x1,x2,x3|Y) = P(x1|Y)*P(x2|Y)*P(x3|Y),取对数相乘变为相加
        # result.shape = [m_sample,1]
        result = np.sum(np.log(numerator / denominator), axis=1, keepdims=True)

        return result.T

    def _predict(self, X):
        # 计算每个种类的概率P(Y|x1,x2,x3) =  P(Y)*P(x1|Y)*P(x2|Y)*P(x3|Y)
        output = []
        for y in range(self.classes.shape[0]):
            prior = np.log(self.parameters["class" + str(y)]["prior"])
            posterior = self._pdf(X, y)
            prediction = prior + posterior
            output.append(prediction)
        return output

    def predict(self, X):
        # 取概率最大的类别返回预测值
        output = self._predict(X)
        output = np.reshape(output, (self.classes.shape[0], X.shape[0]))
        prediction = np.argmax(output, axis=0)
        return prediction



#主函数
def main():
    data = datasets.load_digits()
    X = normalize(data.data)
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4)
    print("X_train",X_train.shape)
    clf = NaiveBayes()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)

    print ("Accuracy:", accuracy)

    # Reduce dimension to two using PCA and plot the results
    Plot().plot_in_2d(X_test, y_pred, title="Naive Bayes", accuracy=accuracy, legend_labels=data.target_names)

if __name__ == "__main__":
    main()

