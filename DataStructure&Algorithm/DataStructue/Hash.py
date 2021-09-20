# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
哈希表
https://www.bilibili.com/video/BV1uA411N7c5?p=62&spm_id_from=pageDriver
定义：哈希表通过hash函数来计算数据存储位置的结构，通常支持-\
     插入键值对insert(key,value);
     get(key)
     删除键值对delete(key)
     哈希表是一种线性表的存储结构。哈希表由一个直接寻址表和一个哈希函数组成。哈希函数
     h(k)将元素关键字k作为自变量，返回元素的存储下标。
字典、集合(只有key)都是运用了hash
'''

#hash表的实现(拉链法)
class LinkList: #创造单链表
    class Node: #链表内的节点, class套class和函数套函数一样
        def __init__(self, item = None):
            self.item = item
            self.next = None
            
    class LinkListIterator: #创建迭代器类，迭代通过__next__实现
        def __init__(self, node):
            self.node = node
        def __next__(self): #重写class LinkListIterator的内置循环函数，让循环的下一个按照__next__的方式表达，在后面的for循环中体现
            if self.node: #如果传进来的节点不是None
                cur_node = self.node
                self.node = cur_node.next #将当前node转化为nextnode
                return cur_node.item #输出当前node的内容
            else:
                raise StopIteration #如果node是空，停止循环
            
    def __init__(self, iterable = None): #传入一个列表到linklist中作为初始节点head,iterable是一个list
        self.head = None
        self.tail = None
        if iterable: #如果iterable不是None而是在创建Linklist时已经有主动写入链表的话，将列表iterable中的这些元素各自以Node的形式进行尾插
            self.extend(iterable)
    
    def extend(self, iterable): #将iterable内多个元素各自以Node的形式进行尾插。
        for obj in iterable:
            self.append(obj)
    
    def append(self, obj): #将obj以Node的形式进行尾插
        s = LinkList.Node(obj) #将obj写成链表节点形式
        if not self.head: #表示如果head是空的，没有head节点
            self.head = s
            self.tail = s
        else:
            self.tail.next = s
            self.tail = s #跟新尾巴
            
    def remove(self, obj): #将obj移出链表
        if not self.head:
            return 'LinkList is Empty'
        else:
            prior_Node = self.head
            cur_Node = self.head
            while cur_Node.item != obj and cur_Node.item != None:
                prior_Node = cur_Node
                cur_Node = cur_Node.next
            else:
                if cur_Node == None:
                    return 'Obj not in LinkList'
                else:
                    if prior_Node.item == cur_Node.item:
                        self.head = None
                    else:
                        prior_Node.next = cur_Node.next
            
    def find(self, obj):
        for n in self: #查看这个类LinkList内的内容iterable，每个iterable是一串Node
            #这个self是LinkList这个类，它能写进for也是依靠__iter__; 它的循环依靠LinkListIterator的__next__
            if n == obj:
                return True
        else:
            return False
        
    def __iter__(self): #重写内置循环函数, 这个函数的目的是让这个class支持迭代, 即能够如下写for i in LinkList(List支持for循环，但是LinkList链表不支持for循环)
        #写了这个函数后，LinkList就是一个可迭代的对象了
        return self.LinkListIterator(self.head) #使用迭代器类
    
    def __repr__(self): #重写内置print函数, 只有这个类LinkList是可迭代对象才能遍历，才能print
        return '<<'+', '.join(map(str, self))+'>>'
        #这里self指LinkList, 是一个可迭代对象, 可迭代对象在repr时会把每次迭代结果print
        #map(str, self)表示将self每次迭代的元素换成对应的string, 由于self是可迭代对象, map(str, self)也是可迭代对象
        #join是将字符链接 
        
lk = LinkList([1,2,3,4,5])
print(lk)
lk.remove(5)
print(lk)
#hash的构造
'''
哈希表的目的是创建一个类似集合的东西(key独特)
'''
class HashTable:
    def __init__(self, size = 101): #这里设置了size = 101，也可以取None后续自行设置
        self.size = size
        self.T = [LinkList() for _ in range(self.size)]
        
    def h(self, k): #假设k是整数输入
        return k % self.size
    
    def find(self, k):
        i = self.h(k) #哈希函数转换输入值
        return self.T[i].find(k) #查找输入值k是否已经在哈希表T中i位置的链表上
    
    def insert(self, k):
        i = self.h(k) #哈希函数转换输入值
        if self.find(k): #如果k已经在哈希表的一个链表内,输出"重复插入"
            print('Duplicated Insert')
        else:
            self.T[i].append(k) #否则进行插入
    
    def delete(self, k):
        i = self.h(k)
        if self.find(k):
            self.T[i].remove(k)
        else:
            print('Obj not in Hashtable')
    
    def __repr__(self):
        return '<<'+', '.join(map(str, self.T))+'>>'

ht = HashTable()
ht.insert(0)
ht.insert(1)
ht.insert(0)
ht.delete(1)
print(ht)
'''-------------------------------------------------------------------------'''

##哈希表的应用
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=64
'''




