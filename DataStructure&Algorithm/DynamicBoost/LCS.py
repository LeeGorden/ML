# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
#最长公共子序列LCS
https://www.bilibili.com/video/BV1uA411N7c5?p=93
给定两个序列X, Y，求X和Y长度最大的公共子序列。
eg: X = 'ABBCBDE' Y = 'DBBCDB' LCS(X, Y) = 'BBCD'
应用场景: 字符串相似度比对(模糊查询)

定理1-LCS的最优子结构: 令X = (x1, x2,..., xm) 和 y = (y1, y2,...yn)为两个序列,
                      Z = （z1, z2,...zk)为X和Y的任意LCS
                      1)如果 xm = yn, 则zk = xm = yn, 且Zk-1是Xm-1 和 Yn-1的一个LCS
                        ABDC 和 ABC的LCS是ABC，则ABD和AB的LCS是AB
                      2)如果 xm ！= yn，那么zk ！= xm意味着Z是Xm-1和Y的一个LCS
                      3)2)如果 xm ！= yn，那么zk ！= yn意味着Z是X和Yn-1的一个LCS
★由定理1得出递推式: c[i, j] = 0                          若i = 0, 或j = 1
                             c[i-1, j-1] + 1            若i,j > 0, 且xi = yj
                             max(c[i, j-1]), c[i-1, j]) 若i,j < 0， 且xi != yj
                             其中c表示X和Y的LCS的长度, i是X序列下标, j是y序列下标
可以参考下图:
C:\Personal\MachineLearning\Python\Algorithm Material\Leetcode\Data Structure & Algorithm of Python\动态规划\LCS.JPG
'''
def LCS_DP(X, Y):
    '''
    X,Y可以是str也可以是list
    '''
    m = len(X)
    n = len(Y)
    c = [[0 for _ in range(n+1)] for _ in range(m+1)] #创建一个m+1行, n+1列的二维列表, 因为要算上空集, 即index 0
    route = [[0 for _ in range(n+1)] for _ in range(m+1)] #创建一个路径, 记录该格子的数是从哪个方向传来的
    for i in range(1, m+1):
        #第一行是0, 所以i从1开始
        for j in range(1, n+1):
            #第一列是0, 所以j从1开始
            #参考C:\Personal\MachineLearning\Python\Algorithm Material\Leetcode\Data Structure & Algorithm of Python\动态规划\LCS.JPG
            if X[i-1] == Y[j-1]: #X, Y的第一位的index是0, 所以是i-1, j-1
                c[i][j] = c[i-1][j-1] + 1
                route[i][j] = 1 #1表示当前格子的数字来自于左上方
            else:
                if c[i-1][j] >= c[i][j-1]:
                    c[i][j] = c[i-1][j]
                    route[i][j] = 2 #2表示当前格子的数字来自于上边
                else:
                    c[i][j] = c[i][j-1]
                    route[i][j] = 3 #3表示当前格子的数字来自于左边      
    for _ in c:
        print(_)
    print('Route is:')
    for _ in route:
        print(_)        
        
    return c[m][n], route


def LCS_DP_Solution(X, Y):
    '''
    回溯求解
    只计算一个LCS，改变上面最后一组if else等于号归属可能会有不同答案
    '''
    c, route = LCS_DP(X, Y)
    i = len(X)
    j = len(Y)
    ans = [0 for _ in range(c)]
    ans_ind = -1
    while i > 0 and j > 0:
        if route[i][j] == 1: #来自左上方, 为位置匹配, 将对应元素放入LCS
            ans[ans_ind] = X[i-1]
            ans_ind -= 1
            i -= 1
            j -= 1
        elif route[i][j] == 2: #来自上方, 往上移动
            i -= 1
        else:
            j -= 1 #来自左方, 往左移动
    return ''.join(ans)
    '''
    #下面这个方法return对list用了reverse(O(n)), 时间复杂度升高
    ans = []
    while i > 0 and j > 0:
        if route[i][j] == 1: #来自左上方, 为位置匹配, 将对应元素放入LCS
            ans.append(X[i-1])
            i -= 1
            j -= 1
        elif route[i][j] == 2: #来自上方, 往上移动
            i -= 1
        else:
            j -= 1 #来自左方, 往左移动   
    return ''.join(reversed(ans))
    '''
            
print(LCS_DP_Solution('AZBYCIDOEPFIG', 'ABCDFG'))



