# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
链表
https://www.bilibili.com/video/BV1uA411N7c5?p=57
定义：链表是由一系列节点组成的元素集合。每个节点都包含两部分，数据域(item)和指向下一个
     节点的指针next。通过节点之间的互相连接，最终形成一个链表。
'''
#原理(手动创造链表结构)
class Node:
    def __init__(self, item):
        self.item = item
        self.next = None #与创建类Node中的子内容next，None适合之后赋值的任何类型，这里先放一个None建立一个内存

a = Node(1)
b = Node(2)
c = Node(3)
a.next = b
b.next = c
print(a.next.item) # = b.item
print(a.next.next.item) # = c.item
#这样子只需要a这个节点就能依次找到b和c的结构叫链表
'''------------------------------------------------------------------------'''

#链表的创建和遍历
'''
头插法：在链表前面插入节点。尾插法：在链表结尾插入节点
'''
def create_linklist(li):
    head = Node(li[0]) #根据第一个元素创建头节点
    for element in li[1:]:
        node = Node(element) #创建新节点
        #头插法
        node.next = head
        head = node
    return head

def create_linklist_tail(li):
    head = Node(li[0])
    tail = head
    for element in li[1:]:
        node = Node(element)
        #尾插法
        tail.next = node
        tail = node
    return head

def print_linklist(lk):
    #链表的遍历
    while lk: #只要lk不是None，就能打印数据域
        print(lk.item, end='') #end=''表示打印时候不换行
        lk = lk.next

lk = create_linklist([1,2,3])
print_linklist(lk)

lk = create_linklist_tail([1,2,3])
print_linklist(lk)

'''------------------------------------------------------------------------'''

#链表节点的插入和删除
'''
currentNode--insertNode--followingNode
插入
时间复杂度: O(1)，比列表快(O(n))
步骤：insertNode.next = currentNode.next; currentNode.next = insertNode
'''

'''
删除
时间复杂度: O(1)，比列表快(O(n))
步骤：currentNode.next = deleteNode.next; del deleteNode
'''
'''------------------------------------------------------------------------'''
'''------------------------------------------------------------------------'''

#双链表
'''
技能往后找next，又能往前找pior
'''
class BinaryNode:
    def __init__(self, item):
        self.item = item
        self.next = None
        self.pior = None
'''------------------------------------------------------------------------'''
#双俩表的插入和删除
'''
插入
时间复杂度: O(1)，比列表快(O(n))
步骤：insertNode.next = currentNode.next; currentNode.next.pior = insertNode;
     insertNode.pior = currentNode; currentNode.next = insertNode
'''

'''
删除
时间复杂度: O(1)，比列表快(O(n))
步骤：currentNode.next = deleteNode.next; deleteNode.next.pior = currentNode; 
     del deleteNode
'''
'''------------------------------------------------------------------------'''
'''------------------------------------------------------------------------'''

#链表复杂度分析
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=61
C:\Personal\MachineLearning\Python\Algorithm Material\Leetcode\Data Structure & Algorithm of Python\数据结构\链表复杂度分析.jpg
栈和队列都能用链表代替。
'''


