# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 12:29:15 2021

@author: 李可豪
"""

def hanoi(n, a, b, c):
    '''
    Parameters
    将n个盘子从a经过b移动到c
    '''
    if n > 0: #如果a还有盘子的话继续
        #将上方n-1个盘子从a经过c移动到b
        hanoi(n-1, a, c, b)
        #将第n个盘子从a移动到c
        print('把 %s 号圆盘从  %s 位置移动到 %s 位置' % (n,a,c)) #moving from a to c
        #将n-1个盘子从b经过a移动到c
        hanoi(n-1, b, a, c)   
hanoi(3, 'A', 'B', 'C')
