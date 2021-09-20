# -*- coding: utf-8 -*-
"""
@author: LiGorden

This Cart Tree contain post-pruming.
"""

from collections import Counter
import numpy as np
import random
import math
import re
import copy as copy

def load_data(path_of_data_file):
    X, Y = [], []
    file = open(path_of_data_file,'r') 
    for row in file:                   
        data = row.strip().split(',')  
        X.append(data[:-1])            
        Y.append(data[-1])             
    file.close()
    return data, X, Y, np.array(X), np.array(Y)   

def generate_train_test(X, Y, r):
    '''
    Function: Using stratified sampling to create Train & Test Dataset for a classification question
    Variable: r-% of train data
    '''
    index_list_train = []
    index_total_list = [j for j in range(len(Y))]
    #Use .reshape(-1, 1) to turn Y from(n, ) array to (n, 1) array for hstack. -1 means turn into whatever row as long as column number is 1
    array_XY = np.hstack([X[1:, :], Y[1:].reshape(-1,1)])
    
    array_XY = array_XY[np.lexsort(array_XY.T)]
    array_XY = np.vstack([np.hstack([X[0,:], Y[0]]), array_XY])
    
    for i in set(Y[1:]):
        targetindex_turple = np.where(array_XY == i)
        targetindex_array = targetindex_turple[0]
        indexchosen_list = random.sample(list(targetindex_array), math.ceil(len(targetindex_array)*r)) #random.sample(list,n)从list中随机选取n个, 是一个list
        index_list_train += indexchosen_list
     
    index_list_test = list(set(index_total_list) - set(index_list_train)) #以index_total_list为全集创造index_list_train的补集。减去{0},是因为需要random乱序选取
    index_list_train.insert(0, 0) #这里直接用.insert就好，不能index = index.insert()
    return array_XY[index_list_train,:-1], array_XY[index_list_train,-1], array_XY[index_list_test,:-1], array_XY[index_list_test,-1]
    
def Gini(Y):
    Sum = 0
    
    for key, value in Counter(Y).items():
        P = value / len(Y)
        Sum = Sum + P * (1-P)
    
    return Sum

def Continue_Process(X, Y):
    Continue_VariableList = []
    #利用Np的lexsort函数对数组进行排序。lexsort(a)默认对当前数组 最后一行 进行升序排序，因此如果要对列操作，则需要转置a.T。如果要逆序，则lexsort(-a)
    #lexsort操作返回index,是一个一维向量/数组
    #数组排序特性，数组a是一个2行*n列数组,a[括号内放一个array],该array对应行操作，如：a[array(1,0)]表示将a原来第一行放到新数组对应行index=1（第二行）处，a的第二行放到新数组对应行index=0（第一行）
    array_YX = np.hstack([Y, X])
    #直接输出np.array(Y) size 为(n,)不为1维数组(n,1),所以需要reshape(len(Y),1)转化为(n,1),才能进行hstack拼接
    Sortedarray_YX = array_YX[np.lexsort(array_YX.T)] #只有(n,1)才能lexsort, (n,)不能排序, 所以要先转为(n,1)
    for i in range(0,len(X)-1):
        if Sortedarray_YX[i,0] != Sortedarray_YX[i+1,0]:
            Continue_standard = (eval(Sortedarray_YX[i,1]) + eval(Sortedarray_YX[i+1,1])) / 2
            Continue_VariableList.append(Continue_standard)   
    return Continue_VariableList
                
#计算一个特征的最小基尼系数及其判断标准
def Gini_DA(X, Y):
    Gini_Max = 0.5   #Gini系数最大值
    Standard, Max_index_1, Max_index_0 = None, None, None  #初始化采取的标准,每一次重新进入Gini_DA都需要重置参数，否则会报错---UnboundLocalError: local variable 'Max_1' referenced before assignment
    
    #当为连续型变量时
    try:
        if isinstance(eval(X[0]),(int,float)): #eval将所有文本型数字转化为数值型(int/float...)数字
            Converted_X = X.reshape(-1,1).astype(dtype = np.float) #因为X为字符型数值数组，该方法转化为浮点型数值数组。原来是1维转化完就是1维，原来没有维度(n,),转化完就没有维度
            Converted_Y = Y.reshape(-1,1)
            #当两个没有维度的array(n,)使用np.hstack就不会横向拼接，而是直接将两个array前后相连(2n,),所以这里对XY都需要reshape成(2n,1)的array
            Continue_Variable = Continue_Process(Converted_X, Converted_Y)
            for i in Continue_Variable:
                index_1 = Converted_X >= i
                Weight_1 = np.sum(Converted_X >= i) / len(Converted_X) #np.sum(array>=1)统计数组中大于等于1的数的个数
                Gini_DA_1 = Weight_1 * Gini(Converted_Y[index_1])
        
                #将bool数组index_1取反:1-index生成取反的0 & 1；.astype(np.bool)将0,1转换为T/F---BOOL类型可以直接作为0/1做数的运算
                index_0 = (1-index_1).astype(np.bool)
                Weight_0 = np.sum(Converted_X < i) / len(Converted_X)
                Gini_DA_0 = Weight_0 * Gini(Converted_Y[index_0])
        
                Gini_DA_TTL = Gini_DA_1 + Gini_DA_0
        
                if Gini_DA_TTL <= Gini_Max:
                    Gini_Max = Gini_DA_TTL
                    Standard = '>=' + str(i)
                    Max_index_1 = index_1
                    Max_index_0 = index_0   
                
    #当为离散型变量时             
    except:  
        for key, value in Counter(X).items():
            index_1 = X == key
            Weight_1 = value / len(X)
            Gini_DA_1 = Weight_1 * Gini(Y[index_1])
        
            #将bool数组index_1取反:1-index生成取反的0 & 1；.astype(np.bool)将0,1转换为T/F---BOOL类型可以直接作为0/1做数的运算
            index_0 = (1-index_1).astype(np.bool)
            Weight_0 = value / len(X)
            Gini_DA_0 = Weight_0 * Gini(Y[index_0])
        
            Gini_DA_TTL = Gini_DA_1 + Gini_DA_0
        
            if Gini_DA_TTL <= Gini_Max:
                Gini_Max = Gini_DA_TTL
                Standard = key
                Max_index_1 = index_1
                Max_index_0 = index_0
    
    return Gini_Max, Standard, Max_index_1, Max_index_0

#返回依照当前样本Gini系数选取的自变量
def Max_Gini_DA(X, Y):
    Gini_of_X = 0.5
    Standard_of_X = None
    i_of_X = 0
    
    for i in range(X.shape[1]):
        Gini_judge, Standard_judge, index_1, index_0 = Gini_DA(X[:,i], Y)
        if Gini_judge <= Gini_of_X:
            Gini_of_X = Gini_judge
            Standard_of_X = Standard_judge    
            Max_index_1_of_X, Max_index_0_of_X = np.insert(index_1,0,True), np.insert(index_0,0,True) #在index_0和index_1的index=0号位置插入一个True
            i_of_X = i #返回X的列号
    return Standard_of_X, Max_index_1_of_X, Max_index_0_of_X, i_of_X

def statistic_cal(Y):   #样本内字段个数统计, 这里Y为array
    assert len(Y.shape) == 1      #当len()==1时继续运行，否则断点。Y.shape返回一个turple记录Y的size, (这里Y需要为(n,)此时这个turple的shape的len == 1, 否则下面的统计Counter会报错)
    items_dict = {}
    for i in range(0, len(Counter(Y))):
        items_dict[Counter(Y).most_common()[i][0]] = Counter(Y).most_common()[i][1]
    return items_dict

def abnormal(dictionary, default): #统计字典中的异常值(占少数的内容的个数)
    abnormal_Num = 0
    for key, value in dictionary.items():
        if key != default:
            abnormal_Num += value
    return abnormal_Num
            

def C_WithoutSubtree(t): #记录剪枝后的C(t)
    assert isinstance(t, Tree)
    return abnormal(t.sample, t.default)

def C_WithSubtree(T):    #记录剪枝前的C(T)
    WithSubtree_missNum = 0  
    for key, value in T.node.items():
        if isinstance(value, Tree) == False:
            WithSubtree_missNum += abnormal(T.sample_distribution[key], 
                                            Counter(T.sample_distribution[key]).most_common(1)[0][0])
        else:
            sub_T = value
            WithSubtree_missNum += C_WithSubtree(sub_T)
    return WithSubtree_missNum

def leavesNumCount(tree):   #读取主树(可以是 树/子树)下有多少个叶节点。
    leavescount = 0
    for key, value in tree.node.items():
        if isinstance(value, Tree) == False:
            leavescount += 1
        else:
            sub_tree = value   #此处需要用value赋值不能用tree.node[key],因为万一 循环内 对tree重新赋值了，会导致 tree.node[key]读取下一个层级的node 
            leavescount += leavesNumCount(sub_tree)
        tree.leavesNum = leavescount
    return leavescount

def node_loss_cal(tree, sampleNum):   #为tree每个node计算node_loss
    if isinstance(tree, Tree):
        tree.node_loss = (C_WithoutSubtree(tree) - C_WithSubtree(tree)) / (tree.leavesNum - 1) / sampleNum
        for key, value in tree.node.items():
            if isinstance(value, Tree):
                sub_tree = value
                node_loss_cal(sub_tree, sampleNum)
            
def set_treeNo(tree, StartNo):   #为构建完的tree, 每个节点编号, 目的: 剪枝读取loss最小的节点时用该编号定位
    if isinstance(tree, Tree):
        tree.node_No = StartNo
        for key, value in tree.node.items():
            if isinstance(value, Tree):
                StartNo += 1
                set_treeNo(value, StartNo)

def get_minLossNode(tree, node_No,  min_node_loss):      #找到最小node_loss的node, 为剪枝做准备
    '''get_min_LossNode(tree, default node_No = 1, default min_node_loss = ttl_tree.node_loss)'''
    if isinstance(tree, Tree):
        for key, value in tree.node.items():
            if isinstance(value, Tree):
                if value.node_loss < min_node_loss:
                    node_No = value.node_No
                    min_node_loss = value.node_loss
                subtree = value
                node_No, min_node_loss = get_minLossNode(subtree, node_No, min_node_loss) 
                #这里一定要赋值, 因为node_No, min_node_loss都是函数内部变量, 
                #不会带出下一个循环返回到上一个循环的node_No, min_node_loss中, 除非return node_No, min_node_loss    
    return node_No, min_node_loss

def cut_node(tree_to_cut, node_No):
    if isinstance(tree_to_cut, Tree):       
        for key, value in tree_to_cut.node.items():   #★这里直接从tree.node开始剪枝, 就注定不会把node_No = 1的树(母树)剪枝
            if isinstance(value, Tree):
                if value.node_No == node_No:
                    tree_to_cut.node[key] = value.default 
                    #★value = tree.node[], 所以在循环内对sub_tree value的修改会直接影响到最外层的tree_to_cut
                    return tree_to_cut
                else:
                    subtree_to_cut = value
                    cut_node(subtree_to_cut, node_No)

def accuracy(Y_real, Y_hat):
    accuracy_BoolArray = Y_real == Y_hat
    accuracy_RateNum = (sum(accuracy_BoolArray)-1)/(len(accuracy_BoolArray)-1)
    return accuracy_RateNum
            
class Tree():
    def __init__(self, feature, default):
        self.feature = feature #feature为X_name
        self.default = default
        self.node_No = 0
        self.node = {}
        self.sample = {}
        self.sample_distribution = {}
        self.node_loss = 0
        self.leavesNum = 0
        self.missrate = 0 #训练样本对训练集的误差
        
    def __repr__(self):
        return self.feature + '->'+str(self.node) 
        
    def addNode(self, key, value):
        self.node[key] = value
        
    def addSample(self, key, value):
        self.sample_distribution[key] = value
   
    def get(self, key):
        if key not in self.node:
            return self.default
        return self.node[key]

class DecisionTreeClassifier():
    def __init__(self):
        self.tree = Tree(None, None)
        self.cutted_tree = Tree(None, None)
        self.cutted_tree_dict = {}
        self.final_tree = Tree(None, None)
    
    def fit(self, X, Y):       
        self.tree = self.constructTree(X, Y)
        set_treeNo(self.tree, 1)    #为建立完的总树每个节点标号, 便于下面找到最小损失度节点
        self.tree.leavesNum = leavesNumCount(self.tree)  #统计树下(包括子树)有多少叶节点
        node_loss_cal(self.tree, len(Y) - 1)
        
        #初始化待剪枝树
        self.cutted_tree = copy.deepcopy(self.tree)
        #这里不能cutted_tree = tree进行赋值, 因为会建立cutted_tree和tree的联系, 后面对cutted_tree进行的修改操作会映射到tree上        
        set_treeNo(self.cutted_tree, 1) #树节点号
        self.cutted_tree.leavesNum = leavesNumCount(self.cutted_tree) #计算树叶节点数
        node_loss_cal(self.cutted_tree, len(Y) - 1) #计算并赋值节点g(t)
        
        #创建自变量名称与index对应关系, 方便forward函数运行
        self.X_name2ind = dict((name, ind) for ind, name in enumerate(X[0,:]))
        
    def constructTree(self, X, Y):
        #在新的数据进入 熵的计算 前置条件
        #当归类后的子集为单一元素集，即没有必要再去分类，纯度已经100%
        if len(set(Y[1:])) == 1:  #set(array)表示统计括号内一维数组出现过什么内容，返回到一个集合里
            return Y[1]          #面有什么，因为Y从第二行Y[1:]开始已经只有一个元素，所以当len==1
        #当归类后的子集不满足预剪枝
        elif len(Y[1:]) < 5:          #预剪枝---设定最小叶节点样本不能小于5，避免过拟合
            return Counter(Y[1:]).most_common(1)[0][0] #将Y中最大概率的结果返回
            #Counter(np.array).most_common(n)是一个list,返回前n个最多的key以及个数value:[('否', 9), ('是', 8)]
            #Counter(np.array).most_common(n)[0]返回list中第0个index的内容，此处是一个turple('否', 9)
            #Counter(np.array).most_common(n)[0][0]返回turple中第一个值，'否'
        #当X已经没有被待选入的特征了（ID3每个变量在 一条路径 中只能使用一次）
        
        #选出纯度最高的第一层特征变量以及判断标准
        Standard, Index_1, Index_0, i = Max_Gini_DA(X[1:], Y[1:])
        tree = Tree(X[0,i], Counter(Y[1:]).most_common(1)[0][0])    
        tree.sample = statistic_cal(Y[1:])
        
        #建立每条子树下的路径---True一条，False一条，在内部 重复constructTree。因为Cart能重复使用已经用过的X，所以不用拼接
        value_1 = self.constructTree(X[Index_1,:], Y[Index_1])
        value_0 = self.constructTree(X[Index_0,:], Y[Index_0])
        tree.addNode(Standard, value_1)
        tree.addNode('Not '+str(Standard), value_0)
        #在每一个route添加样本
        tree.addSample(Standard, statistic_cal(Y[Index_1][1:])) #Index_1带Y_Name, 所以要再加上[1:]
        tree.addSample('Not '+str(Standard), statistic_cal(Y[Index_0][1:]))
        
        #计算每个节点的 误差率missrate
        tree.missrate = C_WithSubtree(tree) / len(Y[1:]) #训练样本对训练集的误差
         
        return tree        
    
    def forward(self, X, tree):
        if tree.feature in X:
            return Y[0]
        forward_tree = tree
        while isinstance(forward_tree, Tree):
            inputkey_of_node = X[self.X_name2ind[forward_tree.feature]]
            compare_standard = list(forward_tree.node.keys())[0] #以list形式存储node这个dict的key, list(...)[0]表输出index = 0的对应内容
            try:
                inputkey_of_node = eval(inputkey_of_node) #如果X为离散型变量就会报错进入except操作,如果X为连续变量就会继续运行try
                compare_standard = re.findall(r'\d+\.?\d*',compare_standard) #读取文本内数字,这里返回的是一个list到compare_standard
                compare_standard = eval(compare_standard[0])
                
                if inputkey_of_node >= compare_standard:
                    inputkey_of_node = '>='+str(compare_standard)
                else:
                    inputkey_of_node = 'Not >='+str(compare_standard)
            except:
                if inputkey_of_node in list(forward_tree.node.keys()):
                    pass
                else:
                    inputkey_of_node = 'Not '+ inputkey_of_node   
            
            forward_tree = forward_tree.get(inputkey_of_node)
        return forward_tree
    
    def predict_process(self, X_real, Y_real, tree):
        Y_hat = np.array([self.forward(row, tree) for row in X_real])
        return Y_hat, accuracy(Y_real, Y_hat)
    
    def predict(self, X_real, Y_real):
        Y_hat = np.array([self.forward(row, self.final_tree) for row in X_real])
        return Y_hat, accuracy(Y_real, Y_hat)
    
    def cut(self, X_real, Y_real):
        #进行剪枝操作
        nodeNo_tobecut, _ = get_minLossNode(self.cutted_tree, 1, self.cutted_tree.node_loss)
        
        i = 0
        _, accuracy = self.predict_process(X_real, Y_real, self.cutted_tree)
        temporary_tree_list = [copy.deepcopy(self.cutted_tree), copy.deepcopy(accuracy)]
        self.cutted_tree_dict['T' + str(i)] = temporary_tree_list
        
        #创建剪枝树的dict
        while True:            
            if nodeNo_tobecut != 1:    #当nodeNo_tobecut = 1时, nodeNo对应母树, 表示没有可以剪枝的东西了
            
                self.cut_tree_process(self.cutted_tree) #剪枝操作
                i += 1
                set_treeNo(self.cutted_tree, 1) #为一次剪枝后的树重新编节点号
                self.cutted_tree.leavesNum = leavesNumCount(self.cutted_tree) #计算一次剪枝后的树重新编叶节点数
                node_loss_cal(self.cutted_tree, len(Y) - 1) #为每次剪枝的树计算节点g(t)
                
                _, accuracy = self.predict_process(X_real, Y_real, self.cutted_tree)
                temporary_tree_list = [copy.deepcopy(self.cutted_tree), copy.deepcopy(accuracy)]
                self.cutted_tree_dict['T' + str(i)] = temporary_tree_list #后面的cutnode会对前面放到字典里的tree产生影响, 所以字典内要用copy而不是直接把self.cutted_tree放到dict里
                #这里只有深拷贝deepcopy才能拷贝module 
                
                nodeNo_tobecut, b = get_minLossNode(self.cutted_tree, 1, self.cutted_tree.node_loss)
            else:
                i += 1
                break
        
        #选择最高准确率中最简单的树
        tree_to_choose = Tree(None, None)
        tree_accuracy = 0
        for value in self.cutted_tree_dict.values():
            if value[1] >= tree_accuracy:
                tree_to_choose = value[0]
                tree_accuracy = value[1]
        self.final_tree = tree_to_choose                   
    
    def cut_tree_process(self, tree_to_cut):
        node_to_cut, min_node_loss = get_minLossNode(tree_to_cut, 1, tree_to_cut.node_loss)
        cut_node(tree_to_cut, node_to_cut)
                
if __name__ == '__main__':
    data, X_raw, Y_raw, X, Y = load_data('../Data/Iris Data/iris.csv')
    model = DecisionTreeClassifier()
    X_train, Y_train, X_test, Y_test = generate_train_test(X, Y, 0.4)
    model.fit(X_train, Y_train)
    #读取树model.node
    
    #进行剪枝操作
    model.cut(X_test, Y_test)
    
    #数据预测
    Y_hat, final_tree_accuracy = model.predict(X_test, Y_test) 
    tree = model.tree
    final_tree = model.final_tree
    n = leavesNumCount(tree)
    n_cutted = leavesNumCount(final_tree)
    print(model.final_tree)
    
    
    
        