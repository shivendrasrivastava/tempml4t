import numpy as np
# PYTHONPATH=..:. python grade_learners.py
class DTLearner(object):

    def __init__(self, leaf_size=1, verbose = False):
        self.leaf_size = leaf_size
        

    def author(self):
        return 'hsikka3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        # call the tree building method with the passed data
        self.tree = self.build_tree(dataX, dataY)
        
    def query(self, Xtest):
        def query_helper(row, curr_ind):
          
          #if its a leaf, it'll have -1 for first arg
          if self.tree[int(curr_ind)][0] == -1:
            return self.tree[int(curr_ind)][1]
          
          #recursively travel and check if current node is less than current feature
          if self.tree[int(curr_ind)][1] > row[int(self.tree[int(curr_ind)][0])]:
            #call recursive function on position of next node
            left_position = curr_ind + self.tree[int(curr_ind)][2]
            return query_helper(row, left_position)
          elif self.tree[int(curr_ind)][1] == row[int(self.tree[int(curr_ind)][0])]:
            left_position = curr_ind + self.tree[int(curr_ind)][2]
            return query_helper(row, left_position)
          else:
            right_position = curr_ind + self.tree[int(curr_ind)][3]
            return query_helper(row, right_position)

        result_arr = []
        counter = 0
        for x in Xtest:
            leaf = query_helper(x, 0)
            result_arr.insert(counter, leaf)
            counter += 1
        return np.array(result_arr)

    def build_tree(self, dataX, dataY):
        # setup
        cols = dataX.shape[1] #dataX columns
        rows = dataX.shape[0] #dataX rows
        Ymean = np.mean(dataY)
        leaf = [-1, Ymean, None, None]
        ysim = dataY[0] == dataY
        return_leaf = np.array([leaf]) 
        
        # if all the y data is the same, it doesn't matter
        
        if np.all(ysim):
          return return_leaf#return leaf

        # if the dataX rows is less than the leaf size, we're being given too few samples of data
        if self.leaf_size >= rows:
          return return_leaf#return the default leaf
        
        #calculate the optimal feature to split on
        maximum, feature = None, None
        
        for factor in range(cols): #loop through the factors and check correlations
            correlation = np.corrcoef(dataX[:, factor], dataY)[0, 1] #calculate correlation
            if maximum == None: #first iteration
              maximum, feature = correlation, factor
            elif abs(correlation) > abs(maximum): #if correlation exceeds previous maximum
              maximum, feature = correlation, factor
              
        
        feature_col = dataX[:, feature]
        split = np.median(feature_col) #calculate split value by using median of feature column
        
        left_data, right_data = feature_col <= split, feature_col > split #split data into two parts

        #store left and right xy samples
        left_X, left_Y = dataX[left_data], dataY[left_data]
        right_X, right_Y = dataX[right_data], dataY[right_data]

        if np.all(left_data): 
            return return_leaf
        elif np.all(right_data):
            return return_leaf

        #recursively build trees
        left_tree, right_tree = self.build_tree(left_X, left_Y), self.build_tree(right_X, right_Y) 

        # current root will always be starting on the next line
        current_root = [feature, split, 1, left_tree.shape[0] + 1]
        tree_root = np.array([current_root]) 

        #append left subtree to current tree
        left_append = np.append(tree_root, left_tree, axis = 0)
        #append append right append to tree after left append
        tree = np.append(left_append, right_tree, axis = 0)
        #print tree
        return tree
