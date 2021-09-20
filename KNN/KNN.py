# -*- coding: utf-8 -*-
"""
@author: LiGorden

KNN-based on kd tree
Key: 1) Use distance to decide the nearest k neibour and then do the classification
        and regression.
     2) Use CrossValidation to identify the best k.
     3) The distance can be l1/l2（These distance need to standardize Feature 
        before hand. Or can directly use Mahalanobis Distance.
     4) Use kd Tree to search the nearest k neibour
"""
import numpy as np

'''Building KdTree'''
class KdNode:
    def __init__(self, instance, split_feature, left, right, search_status=False):
        '''
        Function: Record the information of a node in KdTree
        Variable: instance = One sample stored in current node
                  split_feature = The index of the feature chosen to split
                  left = left child
        '''
        self.instance = instance
        self.split_feature = split_feature
        self.parent = None
        self.left = left
        self.right = right
        self.search_status = search_status

class KdTree:
    def __init__(self, data):
        #Record feature number k
        self.k = len(data[0]) - 1
        #Constructing KdTrees using recursion
        self.root = self.createNode(0, data)
        #list to record the nearest_neighbors[]
        self.nearest_neighbors = [] #[(instance, distance), (instance, distance)...]
    
    def createNode(self, split_feature, data):
        '''
        Function: Create a KdNode with information of feature chosen to split,
                  left child Kd subtree. Using recursion to construct the kdtree.
        Variable: split_feature = index of feature chosen to split data
                  data = samples(Including y) input before split        
        '''
        if len(data) == 0: 
            #When data has no data within
            return None
        data = data[np.argsort(data[:, split_feature])]
        split_pos = len(data) // 2
        median = data[split_pos]
        split_feature_next = (split_feature + 1) % self.k
        
        #Recuring creatingnode to creat tree
        node_created = KdNode(median, split_feature, \
                      self.createNode(split_feature_next, data[:split_pos]), \
                      self.createNode(split_feature_next, data[split_pos + 1:]))
        #Connect child node with parent if child node is not None
        if node_created.left:
            node_created.left.parent = node_created
        if node_created.right:
            node_created.right.parent = node_created
        return node_created
            
    def preorder(self, root):
        '''
        Function: View the Kd Tree in preorder---View the tree from the left edge
        '''
        print(root.instance)
        if root.left:
            self.preorder(root.left)
        if root.right:
            self.preorder(root.right)
    '''--------------------------------------------------------------------'''

    def search_kdtree(self, test_point, p=2, neighbor_num=3):
        '''
        Function: Serch the constructed tree and find the nearest neighbors for
                  test point
        Variable: test_point---A sample to be predicted with no y label
                  p---method of distance, default by 2-euclidean
                  neighbor_num---default num of nearest neighbors
        '''
        def distance_of_samples(a, b):
            '''
            Function: Calculate the distance between a & b, using method p
            Variable: a---X1 array
                      b---X2 array
            '''
            return (((a-b)**p).sum())**(1/p)
                
        def distance_with_edge(a, instance):
            '''
            Function: Calculate the distance between sample a and edge
            Variable: a and instance here should just be the chosen feature figure.
                      both a & instance do not include y
            '''
            return abs(a - instance)
        
        def find_belonging_area(kdnode, target):
            '''
            Function: Startfrom kdnode, to find the nearest area for target
            Variable: target doesn't have y label since it's test point
            '''
            cur_searching_node = kdnode

            #Find the area which target belongs to
            while cur_searching_node:
                #Find the feature index chosen to split the data in current node
                split_feature_ind = cur_searching_node.split_feature
                #Find the median of the feature
                split_standard = cur_searching_node.instance[split_feature_ind]
                
                if cur_searching_node.left and target[split_feature_ind] <= split_standard:
                    cur_searching_node = cur_searching_node.left
                elif cur_searching_node.right and target[split_feature_ind] > split_standard:
                    cur_searching_node = cur_searching_node.right
                else:
                    return cur_searching_node
                    
            return cur_searching_node
        
        def check_other_route(kdnode, target):
            '''
            Function: Check if current kdnode has alternative child not walk by
                      and the distance between test point and edge of is smaller
                      than the standard, return that node, or None
            Variable: target doesn't have y label since it's test point.
                      self.nearest_neighbors here should alreays be the reverse
                      order by distance
            '''
            split_feature_ind = kdnode.split_feature
            #Condition when need to search the nearest neighbor on another branch of parent node
            if distance_with_edge(target[split_feature_ind], kdnode.instance[split_feature_ind]) <= self.nearest_neighbors[0][1]:
                if kdnode.left and kdnode.left.search_status == False:               
                    return kdnode.left
                elif kdnode.right and kdnode.right.search_status == False: 
                    return kdnode.right
            else: #If other route's edge distance to test sample is larger that anyother distance between samples in neighbors
                return None #If so, dont need to go back to botton_up_writein loop 
            
        def bottom_up_writein(kdnode, target):
            '''
            Function: Write in nearest k neighbor when meet with condition. Stop
                      when find other route and return it.
            Variable: target does not include y label
                      kdnode here is the nearest area to the test point(leave node)
            '''
            while kdnode:
                if kdnode.search_status == False:
                    distance = distance_of_samples(kdnode.instance[:-1], target)
                    if len(self.nearest_neighbors) < neighbor_num:
                        self.nearest_neighbors.append([kdnode.instance, distance])
                        #Reorder self.nearest_neighbor, make sure the first one has the largest distance
                        self.nearest_neighbors = sorted(self.nearest_neighbors, key=lambda x: x[1], reverse=True)
                    elif distance <= self.nearest_neighbors[0][1]:
                        self.nearest_neighbors[0] = [kdnode.instance, distance]
                        self.nearest_neighbors = sorted(self.nearest_neighbors, key=lambda x: x[1], reverse=True)
                    kdnode.search_status = True
                    
                    other_route = check_other_route(kdnode ,target)
                    if other_route:
                        return other_route
                    kdnode = kdnode.parent
                else:
                    kdnode = kdnode.parent
            else: #When kdnode is None, which means it reaches the root, stop
                return None
            
        def find_nearest_neighbors(kdnode, target):
            '''
            Function: Start from kdnode(at bottom) to view if there is any sample 
                      satisfy the condition
            Variable: kd_node---current node viewed
                      target---test point, no y label
            '''
            #Find the nearest area at the bottom
            nearest_area = find_belonging_area(kdnode, target)
            #Input instances into self.neighbors_num from the bottom, and find a node need to restart find_belonging_area
            kdnode_to_restart = bottom_up_writein(nearest_area, target)
            if kdnode_to_restart: #Stop when we arrive the root, when kdnode_to_restart = None
                find_nearest_neighbors(kdnode_to_restart, target)
            return self.nearest_neighbors
        
        #for search_kdtree(self, test_point, p=2, neighbor_num=3):
        return find_nearest_neighbors(self.root, test_point)
    
    def predict(self, test_point, p=2, neighbor_num=3):
        '''
        Function: Predict the test_point label
        Variable: test_point does not include y
        '''
        pass
                
#result = namedtuple('Result_tuple', 'nearest_point nearest_dist nodes_visited')
if __name__ == '__main__':
    import pandas as pd
    from sklearn.model_selection import train_test_split
    
    data = pd.read_csv('../Data/Iris Data/iris.csv')
    X, y = np.array(data)[:, :-1], np.array(data)[:, -1].reshape(-1, 1)
    
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=0.33, shuffle=True, stratify=y, random_state=0)
    
    data_train = np.hstack([X_train, y_train.reshape(-1, 1)])
    kd = KdTree(data_train)
    kd.preorder(kd.root)
    print('----------------Test Searching Kd Tree--------------------')
    import random
    n = random.randint(0, 49)
    t = X_test[n, :]
    print(y_test[n])
    print(t)
    print(kd.search_kdtree(t, p=2, neighbor_num=3))
    #y_hat = kd.predict(X_test, p=2, neighbor_num=3)
    #accuracy = sum(y_hat == y_test)/len(y_test)







        