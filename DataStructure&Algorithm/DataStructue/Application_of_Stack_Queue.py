# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
迷宫问题(对应两种算法：深度优先算法DFS，广度优先算法BFS)
https://www.bilibili.com/video/BV1uA411N7c5?p=53
https://www.bilibili.com/video/BV1uA411N7c5?p=55&spm_id_from=pageDriver
'''

#栈的算法---深度优先搜索(回溯法)
'''
原理：从一个节点开始，任意找下一个能走的点(进栈)，当找不到能走的点时，退回上一个点寻找是否有
其他方向的点(出栈)。
优缺点：代码少，但是不是最短路径
'''
#建立迷宫，1表示墙，0代表能走
maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

#封装方向列表，上下左右顺序在这个封装里无所谓,因为总要一个一个试的
direcs = [
        lambda x,y: (x-1,y), #上
        lambda x,y: (x,y+1), #右
        lambda x,y: (x+1,y), #下
        lambda x,y: (x,y-1)  #左
        ]

def maze_path(x1, y1, x2, y2):
    '''
    (x1, y1):起点位置,x表示行，y表示列
    (x2, y2):终点位置
    '''
    stack = []
    stack.append((x1, y1)) #存入起点元组
    while len(stack) > 0:
        #只要栈不空时循环
        curNode = stack[-1] #当前节点，即栈的最后一位
        #寻找上下左右四个方向的节点位置; 上:(x-1, y),下:(x+1, y),左:(x,y-1),右:(x,y+1)
        if curNode[0] == x2 and curNode[1] ==y2: #当走到重点的时候，走到了终点
            print('找到了路径！')
            for p in stack: #返回找到的第一条路径
                print(p)
            return True
        
        for direc in direcs: #循环方向封装，表示试探下一步能不能走
            nextNode = direc(curNode[0], curNode[1]) #nextNode是元组
            #如果下一步能走
            if maze[nextNode[0]][nextNode[1]] == 0:
                stack.append(nextNode)
                maze[nextNode[0]][nextNode[1]] = 2 #2表示这个节点已经走过，这里是行得通的节点标记
                break #找到一个能走的点就行，否则需要找下一个
        else:  #当前节点没有下一个能走的节点时
            maze[nextNode[0]][nextNode[1]] = 2 #2表示这个节点已经走过,这里是行不通的节点标记
            stack.pop() #当前节点没有下一步可走的时候，将当前节点移除栈，表示不是合适路径
    else:
        print('没有路！')
        return False
    
maze_path(1,1,8,8)
'''------------------------------------------------------------------------'''

#队列的算法---广度优先搜索
'''
原理：从一个节点开始，寻找所有接下来能走的点，继续不断找直到找到出口。每次多个路径都走一步，
     当不能走时这条路废弃，其他路继续走一步。由于每一步都是一步一步走，那么先到终点的路径
     一定是最短的。与栈不同，队列存的是各个路径的当前终端。
     在到达终点后要输出路径，方法是在寻路的过程中建立一个list，用来记录是哪一步让我们走到
     当前位置的。这样子就能够在获取最后位置步骤顺序index后可以返回找路径。
'''
maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

direcs = [
        lambda x,y: (x-1,y), #上
        lambda x,y: (x,y+1), #右
        lambda x,y: (x+1,y), #下
        lambda x,y: (x,y-1)  #左
        ]

from collections import deque

def print_r(path): #回查路径函数
    curNode = path[-1] #path是所有路径
    realpath = []     #real_path记录到达终点的路径
    while curNode[2] != -1: #这里当curNode对应index curNode=-1时，表示已经退回到第一个点
        realpath.append(curNode[0:2]) #将路径节点坐标(x,y)放到real_path
        curNode = path[curNode[2]] #找是curNode是哪个节点带进来的, 然后进入下一次迭代, curNode[2]是一个index
    realpath.append(curNode[0:2]) #注：realpath内的元素是倒叙的，从终点到起点，所以要reverse
    realpath.reverse() #时间复杂度=O(n)
    for node in realpath:
        print(node)

def maze_path_queue(x1, y1, x2, y2):
    queue = deque()
    queue.append((x1, y1, -1)) #队列内的元素是turple,(x1, y1, 让它进队的数的index)
    path = [] #记录出队的节点，用以往回找路径
    while len(queue) > 0: #当队空的时候，说明当前节点往后走是死胡同
        curNode = queue.popleft() 
        #★注意，这一步一定是popleft，因为要保证不同路径每次都只走一步，所以要把最左边的节点取出来当作curNode进入求nextNode环节。这也是BFS用到queue的地方
        path.append(curNode) #将curNode放到path中
        
        #判断是否到达重点
        if curNode[0] == x2 and curNode[1] == y2:
            print_r(path)
            return True
        
        #尝试四个方向
        for direc in direcs:
            nextNode = direc(curNode[0], curNode[1])
            if maze[nextNode[0]][nextNode[1]] == 0:
                queue.append((nextNode[0], nextNode[1], len(path)-1))
                #nextNode由curNode带进来的，curNode在path中的下标是最后一位的index，所以这里是len(path)-1
                #★注意，这里是当前节点所有可行nextNode按照direc内的方向依次append进queue，只想他们的当前节点是同一个，即path中index = len(path)-1的节点
                maze[nextNode[0]][nextNode[1]] = 2 #标记已经走过
            #这里与DFS不同不用break，DFS找到节点就停，这里要继续找其他可行节点
    else:
        print('没有路')
        return False
            
maze_path_queue(1,1,8,8)
    
    