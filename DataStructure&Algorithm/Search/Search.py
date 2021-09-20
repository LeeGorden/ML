# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""
def linear_search(li, val):
    '''
    顺序查找, 只能找一个
    时间复杂度: O(n)
    Parameters
    ----------
    li : 待查找列表
    val : 待查找数值
    '''
    for ind, v in enumerate(list):
        if v == val:
            return ind
        else:
            return None
        
def binary_search(li, val):
    '''
    待查找列表li已经从小到大sort, sort的时间复杂度 > O(n), 所以若之查找一次，用顺序
    查找，若查找很多次，先排序。内置Index查找是顺序查找
    时间复杂度: O(log2(n))
    '''
    left = 0
    right = len(li) - 1
    '''
    left, right 分别是左右指针，用来进行二分位置判断
    '''
    while left <= right: #left <= right说明候选区还有值
        mid = (left + right) // 2
        if li[mid] == val:
            return val
        elif li[mid] > val:
            right = mid - 1
        else:
            left = mid + 1
    return None

binary_search([1,2,3,4,5], 3)
    
    