# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
二叉搜索树
https://www.bilibili.com/video/BV1uA411N7c5?p=69&spm_id_from=pageDriver
'''
from collections import deque

##二叉搜索树
class BiTreeNode:
    def __init__(self, data):
        self.data = data
        self.lchild = None #左节点
        self.rchild = None #右节点
        self.parent = None #父节点
        #self.count = 0 #这里可以设置data出现的次数，当出现两次相同数字的时候可以通过计数表示
        #但是一般放到node里面的data都是键值或者说至少都是独特的(比如一个字典的key)。所以一般不会写count
        
class BST:
    def __init__(self, li):
        self.root = None
        #创建初始树
        if li:
            for val in li:
                self.insert_no_rec(val)
    
    #二叉搜索树的插入
    def insert(self, node, val): #递归的插入写法，比较慢。写insert的时候写insert(类实例中是从root开始添加所以要.root, val)
        #在节点node处插入一个值val, 如果val小于node中的data，放在node左孩子处，如果val大于node中的data，放在node右孩子处
        if not node: #如果node是空, 新建立一个node
            node = BiTreeNode(val)
        elif val < node.data:
            node.lchild = self.insert(node.lchild, val) #将父节点连接上左孩子
            node.lchild.parent = node #将左孩子连接上父节点
        elif val > node.data:
            node.rchild = self.insert(node.rchild, val)
            node.rchild.parent = node
        return node
    
    def insert_no_rec(self, val): #非递归的插入写法(用循环写), 比递归快
        p = self.root
        if not p: #空树特殊处理
            self.root =BiTreeNode(val)
            return
        while True:
            if val < p.data:
                if p.lchild: #如果p的左子树不是None
                    p = p.lchild
                else: #如果p的左子树是None
                    p.lchild = BiTreeNode(val)
                    p.lchild.parent = p
            elif val > p.data:
                if p.rchild:
                    p = p.rchild
                else:
                    p.rchild = BiTreeNode(val)
                    p.rchild.parent = p
            else: #让val等于p.data
                return #因为这里node插入的相当于字典的key/或者集合内元素，如果已经有这个key/元素就什么都不用干
     
    #二叉搜索树的遍历
    def pre_order(self, root): #二叉树的前序遍历, 当前以root为根节点打印在每次迭代前面
        if root: #如果root不是空, 当root == None, 递归终止
            print(root.data, end =',')
            self.pre_order(root.lchild) #递归左子树
            self.pre_order(root.rchild) #递归右子树
        
    def in_order(self, root): #二叉树的中序遍历, 当前节点打印在每次迭代中间
        if root:
            self.in_order(root.lchild)
            print(root.data, end = ',')
            self.in_order(root.rchild)
        
    def post_order(self, root): #二叉树的后序遍历, 当前节点打印在每次迭代后面
        if root:
            self.post_order(root.lchild)
            self.post_order(root.rchild)
            print(root.data, end = ',')

    def level_order(self, root): #层次遍历不只适用于二叉树，多叉树也能使用。也是一个BFS
        queue = deque()
        queue.append(root)
        while len(queue) > 0: #只要队不空
            node = queue.popleft()
            print(node.data, end =',')
            if node.lchild:
                queue.append(node.lchild)
                if node.rchild:
                    queue.append(node.rchild)
                    
    #二叉搜索树的查询
    def query(self, node, val): #递归版本查询：因为需要递归，所以需要放进去一个node
        if not node: #若当前节点是空的, 返回None表示找不到
            return None
        if node.data < val:
            return self.query(node.rchild, val)
        elif node.data > val:
            return self.query(node.lchild, val)
        else: #当找到键值时，返回node，如果需要什么数据就取node里面找
            return node
    
    def query_no_rec(self, val): #非递归版本查询, 不需要在function中写node
        p = self.root
        while p: #只要p不是空
            if p.data > val:
                p = p.lchild
            elif p.data < val:
                p = p.rchild
            else:
                return p
        else:
            print('None node Found')
            return None
    
    #★二叉树的删除
    '''
    https://www.bilibili.com/video/BV1uA411N7c5?p=72&spm_id_from=pageDriver
    '''
    def __remove_node_1(self, node): #__为隐藏函数, 调用class者不可见，只用在class内部，由程序开发人员操作
        #情况1的删除: 删除的node是叶子节点
        if not node.parent: #当要删除的节点父节点为None(只有根节点的parent是None, 所以这判断要删除的节点是不是根节点)
            self.root = None
        #判断要删除的叶子节点使其父亲节点的那个节点
        if node == node.parent.lchild:
            node.parent.lchild = None
        else:
            node.parent.rchild = None
            
    def __remove_node_21(self, node):
        #情况2:删除的node只有一个左孩子
        if not node.parent:
            self.root = node.lchild
            node.lchild.parent = None         
        elif node == node.parent.lchild:
            node.parent.lchild = node.lchild
            node.lchild.parent = node.parent
        else:
            node.parent.rchild = node.lchild
            node.lchild.parent = node.parent
            
    def __remove_node_22(self, node):
        #情况2:删除的node只有一个右孩子
        if not node.parent:
            self.root = node.rchild
            node.rchild.parent = None         
        elif node == node.parent.lchild:
            node.parent.lchild = node.rchild
            node.rchild.parent = node.parent
        else:
            node.parent.rchild = node.rchild
            node.rchild.parent = node.parent  
    
    def delete(self, val):
        if not self.root: #如果是空树
            print('The tree is empty!')
            return 
        #当不是空树
        node = self.query_no_rec(val)
        if not node: #当node不存在
            print('There is no such node')
            return
        if not node.lchild and not node.rchild: #当node是叶子节点
            self.__remove_node_1(node)
        elif not node.rchild: #当node没有右孩子(此时一定有左节点, 因为上面已经筛选出叶子节点)
            self.__remove_node_21(node)
        elif not node.lchild: #当node没有左孩子
            self.__remove_node_22(node)
        else: #当node即有左节点又有右节点
            #比较要删除node左节点中最大数和右节点中最小数
            min_node = node.rchild
            while min_node.lchild: #找到删除node右节点中最小数
                #若当前分支还有左节点(对应删除node右节点中最小数)
                min_node = min_node.lchild
            node.data = min_node.data
            #删除min_node(因为min_node对应是删除node右节点中最小数, 所以找到的min_node不可能右lchild)
            if min_node.rchild:
                self.__remove_node__22(min_node)
            else:
                self.__remove_node_1(min_node)
        
if __name__ == '__main__':
    #二叉搜索树的建立、插入以及遍历
    '''
    平均情况下二叉搜索数进行的时间复杂度是O(Logn), 最坏情况下二叉搜索树所有节点只有左子节
    点(或者右子节点)，时间复杂度变成n。解决方案: 1) 随机插入(不是找第一个元素插入，而是随
    机打乱插入,但问题是现实中的数据有时是一个一个来的不是一堆一堆来的,每次的数据只有一个。
    这是由于只有一个数字随机插入失效)。2) AVL数(改进的二叉搜索树)
    '''
    tree = BST([4,6,7,9,2,1,3,5,8])  
    tree.insert_no_rec(10)
    tree.insert_no_rec(10)
    print('二叉搜索树前序遍历') 
    tree.pre_order(tree.root)
    print('') 
    print('二叉搜索树中序遍历，发现二叉搜索树的中序序列一定是升序的')
    tree.in_order(tree.root) 
    print('') 
    print('二叉搜索树后序遍历')
    tree.post_order(tree.root)
    print('') 
    print('二叉搜索树后序遍历')
    tree.level_order(tree.root)
    print('') 
    #二叉搜索树的查询
    nodetofind = tree.query_no_rec(4)
    nodetofind = tree.query_no_rec(10)
    nodetofind = tree.query_no_rec(11)
    #二叉搜索树的删除
    tree.delete(4)
    tree.in_order(tree.root)
    tree.delete(11)
    tree.in_order(tree.root)