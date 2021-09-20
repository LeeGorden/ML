# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
贪心算法
https://www.bilibili.com/video/BV1uA411N7c5?p=80
本质：是当前最优解, 不保证全局最优解, 保证局部最优解。但很多时候局部最优=全局最优
'''
'''------------------------------------------------------------------------'''

#找零问题
'''
n元钱, 有100元, 50元, 20元, 5元, 1元; 怎么找钱所需要的钱币的量最小？
'''
a = [100, 50, 20, 5, 1]
def change(t, n):
    '''
    t需要倒叙排好
    '''
    m = [0 for _ in range(len(t))]
    for i, money in enumerate(t):
        m[i] = n // money
        n = n % money
    return m, n #返回每种钱币张书和剩下的没找开的钱

print(change(a, 376))
'''------------------------------------------------------------------------'''

##背包问题
'''
eg: 有若干个物品, 第i个物品价值vi元, 重wi千克。背包能装W_Total千克。要尽量让装的东西价值最高，
    应该怎么装？
分为：0-1背包问题（要么装-1, 要么不装-0), 采用单价最高得不到全局最优
     分数背包问题(可以带走物品的一部分), 采用单价最高的贪心算法, 此时局部最优=全局最优
解法:
'''

#分数背包
print('分数背包')
def fractional_backpack(goods, W_Total):
    m = [0 for _ in range(len(goods))]
    V_Total = 0
    for i, (price, weight) in enumerate(goods):
        if W_Total >= weight:
            m[i] = 1
            W_Total -= weight
            V_Total += price
        else:
            m[i] = W_Total / weight
            V_Total += m[i] * price
            W_Total = 0
            break
    return m, V_Total

goods = [(60, 10),(100, 20),(120,30)] #元组(价值,重量)
goods.sort(key = lambda x: x[0]/x[1], reverse = True) #按照单位价值对goods进行排序    
print(fractional_backpack(goods, 50))
'''------------------------------------------------------------------------'''

#数字拼接问题
print('数字拼接问题')
'''
有n个非负整数, 将其按照字符串拼接为一个整数, 如何拼接使拼接出来的字最大。
最大问题: 128和1286如何设计贪心算法进行拼接
贪心原则: 当a+b > b+a时,进行换位而不是只比较a, b大小
'''
l = [123, 234, 23]
l = list(map(lambda x: str(x), l))

from functools import cmp_to_key

def xy_cmp(x, y): #x,y为字符
    if x+y < y+x:
        return 1 #此时字符串y大于字符串x, 返回1, 表示将x, y换位
    elif x+y > y+x:
        return -1
    else:
        return 0

def number_join(li):
    li = list(map(str, li))
    li.sort(key = cmp_to_key(xy_cmp)) #这一步实现的是类似排序, 按照函数xy_cmp里面的进行换位
    return ''.join(li)

print(number_join(l))
'''------------------------------------------------------------------------'''

#活动选择问题
print('活动选择问题')
'''
假设有n个活动，这些活动都需要占用同一片场地，而场地在某时刻只能供一个活动使用。
每个活动都有一个开始时间si和结束时间fi(题目中以整数表示), 表示活动在[si, fi)区间占场地。
问安排哪些活动能够使场地举办活动个数最多
贪心原则：最先结束的活动一定是最优解的一部分
'''
activities = [(1,4),(3,5),(0,6),(5,7),(3,9),(5,9),(6,10),(8,11),(8,12),(2,14),(12,16)]
#这是各个活动开始结束时间
#保证活动是按照结束时间排好序的
activities.sort(key = lambda x: x[1])

def activity_selection(a):
    res = [a[0]] #最先结束的活动a[0]一定在最优解中, 可以用反证法证明：假设b是最优解中最早结束的活动且a != b， 此时因为ab不相等,所以b至少要比a晚结束。若b比a晚结束, 则a也一定能替换b, 所以a一定在最优解中
    #由于a[0]确定在最优解中，基于a[0]的结束时间进行之后活动的安插
    for i in range(1, len(a)): #0号位的最早结束的活动a[0]已经被选入全局最优解中了
        if a[i][0] >= res [-1][1]:
            #若当前备选的活动开始时间晚于最后一个被选入最优解集合中的活动, 表示不冲突
            res.append(a[i])
    #因为备选列表a已经按照结束时间排好序,每个循环选完一次后, a中的子集剩下一定是不冲突的最早结束的活动。
    return res

print(activity_selection(activities))
            