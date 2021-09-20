# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
栈的数据结构
https://www.bilibili.com/video/BV1uA411N7c5?p=48
定义：Stack是一个数据集合，可以理解为只能在一端进行插入或者删除的list。
特点：后进先出LIFO，跟电梯进出一样
栈的概念：栈顶(最后一个元素的位置)，栈底(第一个元素的位置)
栈的基本操作：进栈(push，在栈顶放如一个元素)、出栈(pop，取出栈顶的元素)、
             取栈顶(gettop,看一眼栈顶的元素不取出)
栈的实现：list。进栈-list.append, 出栈-list.pop, 取栈顶-list[-1]
'''
#栈的代码实现
class Stack:
    '''
    即使不创建class，只要保证在list的使用中只用append和pop也能保证这个list是stack
    '''
    def __init__(self):
        self.stack = []
        
    def push(self, element):
        self.stack.append(element)
        
    def pop(self):
        return self.stack.pop() #list.pop()默认删除列表最后一个元素并返回
    
    def gettop(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None
    
    def isempty(self):
        return len(self.stack) == 0
        
'''------------------------------------------------------------------------'''

#栈的应用
'''
括号匹配问题：利用栈的进栈出栈原理（类似电梯进出），来判断括号是否匹配
()[]-匹配
([{}])-匹配
([)]-不匹配
'''
def brace_match(s):
    '''
    s是括号string eg:'()[]{}'
    '''
    match = {')':'(',']':'[','}':'{'}
    stack = Stack() #利用写好的class Stack创建一个栈
    for ch in s:
        if ch in {'(','[','{'}: 
            #{'(','[','{'}是一个集合,如果是这三个左括号中的一个，则进栈
            stack.push(ch)
        else: #否则ch一定是右括号之一
            if stack.isempty(): #当栈顶之前没有左括号，但是ch是右括号，这时出错
                return False
            elif stack.gettop() == match[ch]: 
                #栈顶的元素正好和右括号匹配，删除栈顶的左括号表示已经找到和录入右括号匹配的左括号
                stack.pop()
            else: #当右括号和栈顶的左括号不匹配，报错
                return False
    if stack.isempty():
        return True
    else:
        return False
    
brace_match('{}[]()}')
brace_match('{}[]()')