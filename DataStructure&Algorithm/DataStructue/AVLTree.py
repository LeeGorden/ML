# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:06:23 2021

@author: 李可豪
"""

'''
AVL树(改进的二叉搜索树)
https://www.bilibili.com/video/BV1uA411N7c5?p=69&spm_id_from=pageDriver
定义: 是一颗自平衡的二叉搜索树, 平衡是指任何一个节点其子节点的高度差不能超过1
性质：AVL树内任何节点的左右子树高度只差<=1，这样插入和查找的效率会高很多
     根的左右子树都是平衡二叉树
'''
'''------------------------------------------------------------------------'''
##AVL维持平衡属性的方法(平衡式插入方法): AVL旋转
'''
原理: 当插入一个节点之后，可能发生不平衡现象, 只有插入节点侧的节点平衡会受影响。这种现
      象可以通过之调整根的一侧子树来实现，我们需要找出第一个破坏了平衡条件的节点，称之
      为k, k的两棵子树的高度差是2。
不平衡的原理：不平衡的出现可能右4种情况。
             1) 不平衡是由于对k的右孩子的右子树下的节点(无论左右，包括该子树的data因为有可能是一个很小的树，根节点只有一侧有节点)插入导致的——左旋
             2) 不平衡是由于对k的左孩子的左子树下的节点(无论左右，包括该子树的data)插入导致的——右旋
             3) 不平衡是由于对k的右孩子的左子树下的节点(无论左右，包括该子树的data)插入导致的——右旋+左旋
             4) 不平衡是由于对k的左孩子的右子树下的节点(无论左右，包括该子树的data)插入导致的——左旋+右旋
https://www.bilibili.com/video/BV1uA411N7c5?p=75&spm_id_from=pageDriver
'''
from BinarySearchTree import BiTreeNode, BST

class AVLNode(BiTreeNode): #继承类
    def __init__(self, data): #这里直接套用BiTreeNode的构造函数
        BiTreeNode.__init__(self, data)
        self.bf = 0 #创建balance factor
        
class AVLTree(BST): #继承类BST，但需要重写insert和delete
    def __init__(self, li = None):
        BST.__init__(self, li)
    
    #旋转函数
    '''
    在插入前我们都假定树已经平衡, 无论是那种rotate, rotate之后k节点位置的bf一定是0
    '''
    def rotate_left(self, p, c): #左旋, p即是k, c是k的右孩子, 输出是旋转之后的k即其子树
        s2 = c.lchild 
        p.rchild = s2 #c把s2给p
        if s2: #当s2不是None, s2可能是None因为关键的是左右两树层数之差。
            s2.parent = p
        
        c.lchild = p
        p.parent = c
        
        #跟新p(第一个bf不平衡的点k的balance factor, 某个节点的balance factor = 节点下面右子树的层数-节点下面左子树的层数) 和 其右子节点c的bf
        p.bf = 0
        c.bf = 0
        #对于插入时这个bf写法是对的，对于删除带来的bf变动，这个bf赋值需要另外调整
        return c #旋转后k节点不再是当前根节点，c是当前根节点
    
    def rotate_right(self, p ,c): #右旋
        s2 = c.rchild
        p.lchild = s2
        if s2:
            s2.parent = p
            
        c.rchild = p
        p.parent = c
        
        p.bf = 0
        c.bf = 0
        return c
    
    def rotate_right_left(self, p, c): #右旋-左旋
        #右旋
        g = c.lchild
        s3 = g.rchild
        c.lchild = s3 #这里s3可能是None，但是就算是None也能把None连上去
        if s3: #当S3不是None，反链会parent
            s3.parent = c
        g.rchild = c
        c.parent = g #不用判断c有没有，因为c一定右data
        
        #左旋
        s2 = g.lchild
        p.rchild = s2
        if s2:
            s2.parent = p
        g.lchild = p
        p.parent = g
        
        #★跟新BF
        if g.bf > 0: #即g.bf = 1, g下一开始插入后旋转前右孩子的层数比左边大1，则如下
            p.bf = -1
            c.bf = 0
        elif g.bf < 0: #即当g.bf = -1， g下一开始插入后旋转前左孩子层数大
            p.bf = 0
            c.bf = 1
        else: #根节点一侧没有节点, 插入的是g(k右孩子的左子树node本身)
            p.bf = 0
            c.bf = 0
        g.bf = 0
        return g #返回旋转之后的子树, 这个子树原本的根节点是k的位置，★所以整个函数整体上来说就是调整不平衡的节点变成平衡
    
    def rotate_left_right(self, p, c):
        g = c.rchild
        s2 = g.lchild
        c.rchild = s2
        if s2:
            s2.parent = c
        g.lchild = c
        c.parent = g
        
        s3 = g.rchild
        p.lchild = s3
        if s3:
            s3.parent = p
        g.rchild = p
        p.parent = g
        
        if g.bf < 0:
            p.bf = 1
            c.bf = 0
        elif g.bf > 0:
            p.bf = 0
            c.bf = -1
        else:
            p.bf = 0
            c.bf = 0
        g.bf = 0
        return g
        
    def insert_no_rec(self, val): #重写BST的insert_no_rec
        #和BST一样要先插入, 插入完成后判断是否平衡，若不平衡运用旋转使其平衡
        p = self.root
        if not p: #空树特殊处理
            self.root =AVLNode(val)
            return
        while True:
            if val < p.data:
                if p.lchild: #如果p的左子树不是None
                    p = p.lchild
                else: #如果p的左子树是None
                    p.lchild = AVLNode(val)
                    p.lchild.parent = p
                    node = p.lchild #保存插入的节点
                    break
            elif val > p.data:
                if p.rchild:
                    p = p.rchild
                else:
                    p.rchild = AVLNode(val)
                    p.rchild.parent = p
                    node = p.rchild #保存插入的节点
                    break
            else: #当val等于p.data
                return #因为这里node对应键值已经存在
            
        #跟新Balance Factor, 需要从下往上依次找节点中不平衡的地方, 对不平衡处进行旋转, ★并且调整不平衡处上面的所有node的bf
        while node.parent: #当node的父节点不是None
            #判断插入的是左孩子还是右孩子
            if node.parent.lchild == node: #左子树来的node, 此时node.parent.bf -= 1
                #跟新node.parent.bf -= 1, 需要分类讨论，注意：原本所有的node在循环结尾(也就是经过旋转调整后),每一个node的初始bf只可能是-1,0,1
                if node.parent.bf < 0: #原来父节点bf=-1, 跟新后变成-2, 这里要采用右旋或者左旋-右旋
                    #★注意，因为这边是循环, 插入节点的父节点层层网上找父节点, 所以上层会出现node.parent.bf<0的情况。如果是刚插入的node他的parent只能是0
                    k_prior = node.parent.parent # 因为下面的旋转操作最后的到了一个旋转后的k, 所以这里要提前准备好k的parent,用来连接旋转后的k
                    p_before_rorate = node.parent
                    #看node的BF
                    if node.bf > 0: #此时用左旋右旋
                        n = self.rotate_left_right(node.parent, node)
                    else: #此时node.bf < 0, 用右旋
                        n = self.rotate_right(node.parent, node)
                    #因为再rotate函数中已经跟新过k节点的bf, 所以这里不用重新赋值bf, 且无论哪种rotate, rotate之后k节点位置的节点bf都是0
                    #记得后面将k_prior 与 n(调整后的k)链接
                elif node.parent.bf > 0: #初始的node.parent.bf = 1, 跟新之后变成0, 不需要旋转
                    node.parent.bf = 0 
                    break #当有一个node 的bf绝对值变为0, 不需要在传递, 因为当一层node.bf变为0时, 只是本身被填平, 更上层node的bf不会再变化了，因为每次插入后都会旋转保持平衡, 如果再上一个循环中parent != 0且平衡, 那么在这个循环中变成0指示填平, 仍然平衡
                else: #原来node.parent.bf = 0, 跟新之后变成-1, parent.bf需要跟新但不需要旋转
                    node.parent.bf = -1
                    node = node.parent #进入下一次循环，看上层的父节点会不会有出现k, 因为这里parent.bf时从0变成-1, 不是被填平, 所以会对上层节点bf产生冲击
                    continue
                
            else: #当node是从右子树传来，此时node.parent.bf += 1
                if node.parent.bf > 0: #原本node.parent.bf = 1， 现在变成2, 采用左旋/右旋左旋
                    k_prior = node.parent.parent
                    p_before_rorate = node.parent
                    if node.bf < 0: #此时node.bf = -1, 采用右旋左旋
                        n = self.rotate_right_left(node.parent, node)
                    else: #此时node.bf = 1, 采用右旋, node不可能是0
                        n = self.rotate_right(node.parent, node)
                    #当node.parent经过代码判断再此情况(node从右子树传来)有必要进入旋转的时候(node.parent.bf从1变成2), 那么node.bf一定不是0。因为如果node时0的话,表示再上一个循环中该node作为parents已经=0, 那么再上一个循环就会break退出循环。
                    #记得在最后连起k_prior和n
                elif node.parent.bf < 0: #原来的node.parent = -1, 现在变成0
                    node.parent.bf = 0
                    break
                else: #原来的node.parent.bf = 0
                    node.parent.bf = 1
                    node = node.parent
                    continue
                
            #链接旋转后k位置的子树与k_prior
            n.parent = k_prior
            if k_prior: #当k存在, k位置的n可能是根节点, k_prior就是None
                if p_before_rorate == k_prior.lchild:
                    k_prior.lchild = n
                else:
                    k_prior.rchild = n
                break #这里和下面之所以是两个break, 是因为插入前的树一定是平衡的, 插入后的树有3类情况: 1)发生旋转, 这时候会触发这个if语句。而旋转的结果是将k位置的节点调整平衡后, k之上的节点不用调整bf, 他们的bf不会变, 随意进入这个if语句可以直接break。                                                                                            #2)插入的值只是填平子树的某一层, 所以更换node.parent.bf = 0之后可以直接break。                                                                                      #3)插入的值使子树新开的一层, 但没有打破该节点node.parent.bf的平衡性, 但是不知道node.parent.parent....parent.bf有没有被打破, 所以需要continue层层去看, 直到遇到调整bf 到 0的节点进入类2) break.
            else:
                self.root = n
                break
          
    def delete_no_rec(self, val): 
        pass

if __name__ == '__main__':
    tree = AVLTree([2,1,4,5,3,7,6,9,10,8])
    tree.pre_order(tree.root)
    print('')
    tree.in_order(tree.root)