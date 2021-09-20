# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
树状结构--链式存储方式(往下.children; 往上.parent)
https://www.bilibili.com/video/BV1uA411N7c5?p=65&spm_id_from=pageDriver
'''
#树的实例
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=66&spm_id_from=pageDriver
eg:模拟文件目录
'''

class Node:
    def __init__(self, name, type = 'dir'): #type默认dir(目录)
        self.name = name
        self.type = type #'dir'目录 or 'file'文件
        self.children = [] #指向子节点
        self.parent = None #指向父节点, 父节点只有一个所以不是list
        
    def __repr__(self):
        '''
        这里写__repr__(self),使得任何试图print Node(包括Node下的children等)的企图
        都会返回__repr__(self)中的内容。而__str__写在这里的话是在只在print Node(不包括
        Node下的children等)的时候进行返回。
        '''
        return self.name
        
n = Node('Hello')
n2 = Node('World')
n.children.append(n2)
n2.parent = n

class FileSystemTree:
    def __init__(self):
        self.root = Node('/', type = 'dir') #定义根目录
        self.now = self.root #当前文件夹/文件
        
    def mkdir(self, name): #创建文件夹
        #name要以"/"结尾，因为文件夹是以"/"结尾
        if name[-1] != '/':
            name += '/' #如果输入的name不是以/结尾，自动补上
        node = Node(name) #创建文件夹(节点)
        #建立创建文件夹与上级的联系
        self.now.children.append(node)
        node.parent = self.now
        
    def ls(self): #展示当前目录下的所有子目录
        return self.now.children
    
    def cd(self, name): #切换目录
        if name[-1] != '/':
            name += '/'
        #返回上级目录
        if name == '../':
            self.now = self.now.parent
            return
        #向下切换目录
        for child in self.now.children:
            if child.name == name:
                self.now = child
                return
        raise ValueError('Invalid dir')
            
            
        
        
file = FileSystemTree()
print(file.root)
file.mkdir('var/')
file.mkdir('bin/')
print(file.root.children)
print(file.ls())

file.cd('bin/')
file.mkdir('binchild/')
print(file.ls())

#返回上级目录
file.cd('../')
print(file.ls())
'''------------------------------------------------------------------------'''

#二叉树
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=67&spm_id_from=pageDriver
'''
class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.lchild = None #左节点
        self.rchild = None #右节点
        
'''------------------------------------------------------------------------'''

#二叉树的遍历
'''
https://www.bilibili.com/video/BV1uA411N7c5?p=68
'''
def pre_order(root): #二叉树的前序遍历, 当前节点打印在每次迭代前面
    if root: #如果root不是空, 当root == None, 递归终止
        print(root.data, end ='')
        pre_order(root.lchild) #递归左子树
        pre_order(root.rchild) #递归右子树
        
def in_order(root): #二叉树的中序遍历, 当前节点打印在每次迭代中间
    if root:
        in_order(root.lchild)
        print(root.data, end = '')
        in_order(root.rchild)
        
def post_order(root): #二叉树的后序遍历, 当前节点打印在每次迭代后面
    if root:
        post_order(root.lchild)
        post_order(root.rchild)
        print(root.data, end = '')

from collections import deque
def level_order(root): #层次遍历不只适用于二叉树，多叉树也能使用。也是一个BFS
    queue = deque()
    queue.append(root)
    while len(queue) > 0: #只要队不空
        node = queue.popleft()
        print(node.data, end =',')
        if node.lchild:
            queue.append(node.lchile)
        if node.rchile:
            queue.append(node.rchile)

        

    
        
        

        


        





