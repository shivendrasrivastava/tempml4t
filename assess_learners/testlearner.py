"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt 
import BagLearner as bl 
import InsaneLearner as il 
import matplotlib.pyplot as plt
import time
import sys

if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        sys.exit(1)
    inf = open(sys.argv[1])
    
    data = np.array([map(float,s.strip().split(',')[1:]) for s in inf.readlines()[1:]])

    # compute how much of the data is training and testing
    train_rows = int(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]

    print testX.shape
    print testY.shape

    rmse_arr = []

    start_time = time.time()
    for i in range(1,30):
        # create a learner and train it
        learner = bl.BagLearner(learner = rt.RTLearner, kwargs = {"leaf_size": i}, bags = 30, boost = False, verbose = False) # create a LinRegLearner
        learner.addEvidence(trainX, trainY) # train it
        print learner.author()

        # evaluate in sample
        # predY = learner.query(trainX) # get the predictions
        # rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        # print
        # print "In sample results"
        # print "RMSE: ", rmse
        # rmse_arr.append(rmse)
        # c = np.corrcoef(predY, y=trainY)
        # print "corr: ", c[0,1]

        # evaluate out of sample
        predY = learner.query(testX) # get the predictions
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        print
        print "Out of sample results"
        print "RMSE: ", rmse
        rmse_arr.append(rmse)
        c = np.corrcoef(predY, y=testY)
        print "corr: ", c[0,1]

    print("--- %s seconds ---" % (time.time() - start_time))

    # plt.ylabel('RMSE')
    # plt.xlabel('Leaf Size')
    # plt.title('The Impact of Leaf Size on RMSE - 30 bags of Random Trees')
    # plt.plot(rmse_arr)
    
    # for i in range(1,29):
    #     print i, ',', rmse_arr[i]
    # plt.show()

