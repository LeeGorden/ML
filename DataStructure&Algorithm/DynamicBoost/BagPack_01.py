# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
动态规划
https://www.bilibili.com/video/BV1uA411N7c5?p=88本质：是当前最优解, 不保证全局最优
解, 保证局部最优解。但很多时候局部最优=全局最优
'''
'''------------------------------------------------------------------------'''
#斐波那契数角度看动态规划：
def fibnacci(n):
    '''
    递归版本    
    '''
    if n == 1 or n == 2:
        return 1
    else:
        return fibnacci(n-1) + fibnacci(n-1)

print(fibnacci(10))

def fibnacci_no_recurision(n):
    '''
    非递归版本    
    '''
    f = [0, 1, 1]   #加0是为了实现下标1对应第一项
    if n > 2:
        for i in range(n-2): #求第n项循环n-2次, 即相加list f的后两项共n-2次
            num = f[-1] + f[-2]
            f.append(num)
    return f[n]

print(fibnacci(10))
'''
我们发现再求斐波那契数的时候，递归效率远远不如非递归版本。因为递归执行效率底下，原因之一
是子问题的重复计算与扩张，因为每个斐波那契数=2个子问题=4个子问题的子问题=8个子子子问题...
最后运算了2^(n-3)次。
而非递归的版本中，我们将已经算完的子问题存入了内存, 只需要调用就可以了。

而这个斐波那契数问题中非递归的思维就是我们动态规划的思维:
    1）最优子结构: 要解决当前问题, 只需要解决其子问题就行, 换个角度说只要能够写出子问题
       代码，然后用递推式就能搞定主问题。 难点在于总结递推式
    2）重复子问题：取代递归结构，用循环的方式，存储子问题，减少运算量
    总结：DP问题是一个个存储递推结构、调用地推结果的循环
'''         
'''------------------------------------------------------------------------'''
'''------------------------------------------------------------------------'''

##钢条切割问题(即0-1背包问题)
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=89、
eg: 一段长度为n的钢条, n为正整数, 按正整数去切，不同长度能卖不同的钱。怎么切n能卖最多钱。
原理：类似于不递归的斐波那契数, 将子问题的最优解决存储起来, 就避免了迭代, 每次只需要思考
      一个主问题: 对n切一刀, 怎么切卖的最好。不用考虑切若干刀情况。因为主问题切一刀后
      生成两个子问题, 这两个子问题的最优解已经被存储。
由上述原理得出递推式: rn = max(pn, r1 + r[n-1], r2 + r[n-2] ..., r[n-1] + r1)。其中,pn
                    表示不切, r1表示切成一端长度为1的钢条, r[n-1]表示切成长度为n-1的钢条
递推式简化: 把上述切割过程可以想象成将n长的钢条切一刀, 切出来的两段中一段不会再切割, 而
           另外一段能够继续切割。之所以能够这么想象请看下方例子:
               n = 9, 可以想成1(不再切) + 8(可以再切割), 2(不再切) + 7(可以再切割)...
               7(不再切) + 2(可以再切割), 8(不再切) + 1(可以在切割)。取其中一种切割：
               2(不再切) + 7(可以再切割)为例, 之所以2可以看成不再切割, 是因为2(再切割)
               + 7(再切割)的情况已经在1(不再切) + 8(可以再切割)中算了一次, 因为8可以切割
               的情况已经衡量过将8切成1和7的情况, 这时候9 = 1(不切) + 8(切) = 1(不再切)
               + 1(不再切割) +  7(可再切割) = 2(不切) + 7(可再切)。
           综上rn = max(pi + r[n-i]), 1<=i<=n, 这样子问题就可以少一个, 主问题就变成
           以个固定答案(不再切)+一个子问题(可再切割), 通过减少重复减少运算量
'''

#钢条问题自顶向下实现---递归
'''
时间复杂度O(2^n)
'''
p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 21, 23, 24, 26, 28, 30, 32, 34, 35, 37, 38, 40]#长度为20的钢条, 对应不同切割长度收益, index = 0处对应切0米时的收益

def cut_rod_recurision(p, n):
    '''
    返回钢条p中长度为n段的最大收益
    n为目标钢条长度
    非简化递推式的递归实现, 慢
    '''
    if n == 0: 
        return 0
    else: 
        pn = p[n] #完整的一根的收益pn
        for i in range(1, n): #切的情况, 需要考虑r1~r(n-1)
            pn = max(pn, cut_rod_recurision(p, i) + cut_rod_recurision(p, n-i))
        return pn
 
print(cut_rod_recurision(p, 15))
    
def cut_rod_recurision2(p, n):
    '''
    简化递推式的递归实现, 比非简化递推式的递归实现快
    '''
    if n == 0:
        return 0
    else:
        pn = p[n]
        for i in range(1, n + 1): #rn = max(pi + r[n-i]), 1<=i<=n
            pn = max(pn, p[i] + cut_rod_recurision2(p, n-i))
        return pn
    
print(cut_rod_recurision(p, 15))
'''------------------------------------------------------------------------'''

#钢条问题自底向上实现---非递归，即动态规划解法
def cut_rod_DP(p, n):
    '''
    简化递推式的非递归实现, 比递归要快很多
    时间复杂度O(n^2)
    '''
    r = [0] #创建子集最优解列表, 当钢条长度为0, 收益为0
    #递归式 = max(pi + r(n-i)), 1<=i<=n
    for lenth in range(1, n+1): #lenth = [1, n]
        pn = 0 #长度为lenth的钢条最优解
        for i in range(1, lenth+1): #i = [1, lenth], 这个for循环找到长度为lenth的钢条最优解
            pn = max(pn, p[i] + r[lenth-i])
        r.append(pn)
    return r[n]

print(cut_rod_DP(p, 20))
'''------------------------------------------------------------------------'''

#钢条切割问题---输出最优方案(输出怎么切)
'''
要记录如何切割，对每个子问题，保存切割一次时左边切下的长度，当需要调用怎么切的时候, 只需
要通过目标长度左边切多少来计算右边长度，再去看右边长度对应的左边段切多少，依次类推，直到
钢条切完。这样就能通过直到每次左边不切的长度, 来得出具体每段切成多长。
'''

def cut_rod_DP(p, n):
    r = [0] #记录所有长度最优解
    s = [0] #记录所有长度最优解对应左边段不切割的长度的列表
    for length in range(1, n+1):
        pn = 0 #记录当前长度length最优解
        ps = 0 #记录当前长度length最优解对应左边段不切割的长度
        for i in range(1, length+1):
            if p[i] + r[length - i] >= pn:
                pn = p[i] + r[length - i]
                ps = i
        r.append(pn)
        s.append(ps)
    return r[n], s

def cut_rod_DP_Solution(p, n):
    origin_len = n
    r, s = cut_rod_DP(p, n)
    ans = []
    '''
    ans = [s[n]]
    lenth_remain = n - s[n]
    while lenth_remain > 0:
        ans.append(s[lenth_remain])
        lenth_remain -= s[lenth_remain]
    return r, ans
    '''
    while n > 0:
        ans.append(s[n])
        n -= s[n]
    print('长度为%d的钢条最优解为%d切法为：%s' %(origin_len, r, ans))
    return r, ans

print(cut_rod_DP_Solution(p, 20))
'''------------------------------------------------------------------------'''
'''
★★★什么时候能用DP?
DP关键特征: 1) 最优化问题 
           2) 最优子结构(有递推式)：原问题的最优解中涉及多个子问题
                                 在确定最优解使用哪些子问题时, 需要考虑多种选择
           3) 重叠子问题()
'''



