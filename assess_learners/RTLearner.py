import numpy as np
# PYTHONPATH=..:. python grade_learners.py
class RTLearner(object):

    def __init__(self, leaf_size=1, verbose = False):
        self.leaf_size = leaf_size
        

    def author(self):
        return 'hsikka3' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        # call the tree building method with the passed data
        self.tree = self.build_tree(dataX, dataY)
        
    def query(self, Xtest):
        result_arr = []
        #define inner recursive function
        def query_helper(point, curr_ind):
          node = self.tree[int(curr_ind)]
          if node[0] is None:
            return node[1]
          feature_index = int(node[0])
          if point[feature_index] <= node[1]:
            return query_helper(point, curr_ind + node[2])
          else:
            return query_helper(point, curr_ind + node[3])

        for x in Xtest:
            result_arr.append(query_helper(x, 0))
        return np.array(result_arr)

    def build_tree(self, dataX, dataY):
        # setup
        cols = dataX.shape[1] #dataX columns
        rows = dataX.shape[0] #dataX rows
        default_leaf = np.array([[None, np.mean(dataY), None, None]]) #explain this, figure out double arrays
        
        # if all the y data is the same, it doesn't matter
        if np.all(dataY[0] == dataY):
          return default_leaf#return the default leaf

        # if the dataX rows is less than the leaf size, we're being given too few samples of data
        if self.leaf_size >= rows:
          return default_leaf#return the default leaf
        
        #calculate the optimal feature to split on
        # maximum, feature = None, None
        
        # for factor in range(cols): #loop through the factors and check correlations
        #     correlation = np.corrcoef(dataX[:, factor], dataY)[0, 1] #calculate correlation
        #     if maximum == None: #first iteration
        #       maximum, feature = correlation, factor
        #     elif abs(correlation) > abs(maximum): #if correlation exceeds previous maximum
        #       maximum, feature = correlation, factor
        
        #for random feature
        feature = np.random.randint(0, dataX.shape[1])
              
        
        feature_col = dataX[:, feature]
        split_val = np.median(feature_col) #calculate split value by using median of feature column
        
        left_data, right_data = feature_col <= split_val, feature_col > split_val #split data into two parts
        
        if np.all(left_data): ## explain this line
            return default_leaf
        elif np.all(right_data):
            return default_leaf

        #recursively build trees
        left_tree, right_tree = self.build_tree(dataX[left_data], dataY[left_data]), self.build_tree(dataX[right_data], dataY[right_data]) 

        root = np.array([[feature, split_val, 1, left_tree.shape[0] + 1]]) #explain this, also figure out double arrays

        left_append = np.append(root, left_tree, axis = 0)
        tree = np.append(left_append, right_tree, axis = 0)
        #print tree
        return tree