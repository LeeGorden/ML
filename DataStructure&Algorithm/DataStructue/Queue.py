# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
https://www.bilibili.com/video/BV1uA411N7c5?p=50
队列是一个数据集合，允许在列表的一端进入，另一端删除。
队列进行插入的一端称为队尾(rear), 插入动作称为进队或入队；进行删除的一端称为队头(front)
, 删除动作成为出队
队列的性质: FIFO (First in First out)
队列不能简单的用列表实现，因为先进先出的原则，为了减少时间复杂度，先出的时候不用remove
而是将front指针往后移一位。而这样做随着先出的元素增多，list前部会有冗余。
列表实现方式：环形队列，将list的rear位置后一位与front index相连。当环形队列除了front
            位置都填充完毕，称为队满。
用取余数的方式实现收尾相连。当指针 == Maxsize - 1时，在前进一个位置就到0位置。
队首前进1到达的index: front = (front + 1) % Maxsize
队尾前进1到达的index: rear = (rear + 1) % Maxsize
队空条件: front == rear
队满条件: (rear + 1) % Maxsize == front
'''
#队列的实现
class Queue:
    def __init__(self, size):
        self.queue = [0 for _ in range(size)] #创建队列大小size
        self.size = size
        self.front = 0 #队首初始index
        self.rear = 0 #队尾初始index
        
    def push(self, element): #进队
        if not self.is_filled():
            self.rear = (self.rear + 1) % self.size
            self.queue[self.rear] = element
        else:
            raise IndexError('Queue is filled')
            
    def pop(self): #出队（读取后值还在，但是front指针已经移过该值）
        if not self.is_empty():
            self.front = (self.front + 1) % self.size
            return self.queue[self.front]
        else:
            raise IndexError('Queue is empty') #raise是要求输出报错
    
    def is_empty(self): #判断队空
        return self.rear == self.front
    
    def is_filled(self): #判断队满
        return (self.rear + 1) % self.size == self.front
    
q = Queue(5)
for i in range(4): #因为规定队伍front位置是要空出来的，所以size为5的queue只能村四个元素
    q.push(i)
q.push(1)
q.pop()
'''------------------------------------------------------------------------'''
        
#python队列的内置模块
'''
python内置的是双向队列，队首可以进出，队尾可以进出
基本操作：队首进队，队首出队，队尾进队，队尾出队
'''
#引入双向队列模块
from collections import deque #不能直接import queue，python的queue模块是保证线程安全的模块、

q = deque([100,101,102,103,104], 5) #定队列只能放5个元素(5可不加)，size=6. 当进入第6个元素时，队首自动出队
q.append(1) #队尾进队
q.popleft() #队首出队并输出

#下列代码用于双向队列，一般单项队列用的比较多
q.appendleft(999) #队首进队
q.pop() #队尾出队

'''------------------------------------------------------------------------'''
#读取文件后n行
def tail(n):
    with open('Queue.txt', 'r') as f: #读取整个文件作为f
        q = deque(f, n) #将整个文件从头到位写入que，因为长度是5，所以后面写入时会把前面顶出来
        return q
'''
with open('Queue.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        print(line)
'''

for line in tail(5):
    print(line, end='') #end=''表示去除\n输出


