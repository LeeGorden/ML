# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
最大公约数GCD—Greatest Common Devisor
https://www.bilibili.com/video/BV1uA411N7c5?p=95
原理: gcd(a, b) = gcd(b, a mod b)
eg: gcd(60, 21) = gcd(21, 18), gcd(18, 3) = gcd(3, 0) = 3
'''
def gcd_recurision(a, b):
    if b == 0:
        return a
    else:
        return gcd_recurision(b, a % b)
    
print(gcd_recurision(12, 16))

def gcd(a, b):
    while b > 0:
        r = a % b
        a = b
        b = r
    return a

print(gcd(12, 16))
'''------------------------------------------------------------------------'''

#欧几里得算法(GCD)应用
class Fraction:
    '''
    欧几里得算法实现一个分数类, 支持分数的四则运算
    '''
    def __init__(self, a, b):
        '''
        a是分子, b是分母
        '''
        self.a = a
        self.b = b
        x = self.gcd(a, b) 
        self.a /= x
        self.b /= x
    
    def gcd(self, a, b): 
        '''
        约分
        '''
        while b > 0:
            r = a % b
            a = b
            b = r
        return a
    
    
    ##分数加法
    def min_common_times(self, a, b):
        '''
        利用最大公约数求最小公倍数
        eg: gcd(12, 16) = 4, 12/4 = 3, 16/4 = 4; 最小公倍数 = 3 * 4 * 4
        '''
        x = self.gcd(a, b)
        return x * (a/x) * (b/x)
        
    def __add__(self, other): #重载这个类与自身之间的+号运算
        # eg: #a/b + c/d
        a = self.a
        b = self.b
        c = other.a
        d = other.b
        Denominator = self.min_common_times(b, d) #分母
        Numerator =  a * (Denominator / b) + c * (Denominator / d) #分子
        return Fraction(Numerator, Denominator)
    
    def __str__(self):
        return '%d/%d' % (self.a, self.b)

print(Fraction(15, 30))
print(Fraction(10, 30))
print(Fraction(15, 30)+Fraction(10, 30))
