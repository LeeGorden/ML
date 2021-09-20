# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
列表的数据结构
https://www.bilibili.com/video/BV1uA411N7c5?p=47&spm_id_from=pageDriver
列表是连续存储的。
数组和列表有两点不一样：
1. 数组元素类型是一样的，一个数组内元素类型要相同，因为要保证每个存储单元长度相同
（这时数组赖以查找的原理）
2. 数组长度固定

插入(不是append，而是在中间插入insert)和删除(remove)对列表来说时间复杂度都是O(n), 因
为python的操作是要将插入/删除后的所有元素后移/前移。
'''