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
        #take a sample chunk of data from the training data
        row_range = np.arange(rows)
        sample_chunk = None 
        # keeping sample out here works..?
        # sample_chunk = np.random.choice(row_range, rows)
        for learner in self.learners:
            #store sliced samples
            sample_chunk = np.random.choice(row_range, rows)
            x_sample, y_sample = Xtrain[sample_chunk], Ytrain[sample_chunk]
            #pass to learners
            learner.addEvidence(x_sample, y_sample)

    def query(self, Xtest):
        #define array to be returned
        return_arr = [] 

        for learner in self.learners:
          #for each bag, query a learner and store the result on the array
          return_arr.append(0)
          return_arr[len(return_arr) - 1 ] = learner.query(Xtest)
        
        #convert result to np array, take mean and return
        result = np.mean(np.array(return_arr), axis=0) 
        return result