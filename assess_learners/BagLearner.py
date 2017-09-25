import numpy as np


class BagLearner(object):
    def __init__(self, learner=None, kwargs={}, bags=20, boost=False, verbose=False):
        self.bags = bags
        self.learners = []
        for i in range(self.bags):
          self.learners.append(learner(**kwargs))

    def author(self):
        return 'hsikka3'

    def addEvidence(self, Xtrain, Ytrain):
        rows = Xtrain.shape[0]
        for i in range(self.bags):
            #take a sample chunk of data from the training data
            row_range = np.arange(rows)
            #use np.random.choice to grab sample
            sample_chunk = np.random.choice(row_range, rows) 
            #store sliced samples
            x_sample, y_sample = Xtrain[sample_chunk], Ytrain[sample_chunk]
            #pass to learners
        for i in range(self.bags):
            self.learners[i].addEvidence(x_sample, y_sample)

    def query(self, Xtest):
        #define array to be returned
        return_arr = [] 

        for learner in self.learners: #loop through all the learners
          #for each bag, query a learner and store the result on the array
          return_arr.append(0)
          return_arr[len(return_arr) - 1 ] = learner.query(Xtest)
        
            
        result = np.array(return_arr) #store the result and return
        return np.mean(result, axis=0)