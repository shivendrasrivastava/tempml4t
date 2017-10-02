"""
Test best4 data generator.  (c) 2016 Tucker Balch
"""

import numpy as np
import pandas as pd
import math
import LinRegLearner as lrl
import DTLearner as dt
from gen_data import best4LinReg, best4DT
import time

# compare two learners' rmse out of sample
def compare_os_rmse(learner1, learner2, X, Y):

  # compute how much of the data is training and testing
  train_rows = int(math.floor(0.6* X.shape[0]))
  test_rows = X.shape[0] - train_rows

  # separate out training and testing data
  train = np.random.choice(X.shape[0], size=train_rows, replace=False)
  test = np.setdiff1d(np.array(range(X.shape[0])), train)
  trainX = X[train, :]
  trainY = Y[train]
  testX = X[test, :]
  testY = Y[test]

  # train the learners
  learner1.addEvidence(trainX, trainY) # train it
  learner2.addEvidence(trainX, trainY) # train it

  # evaluate learner1 out of sample
  predY = learner1.query(testX) # get the predictions
  rmse1 = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

  # evaluate learner2 out of sample
  predY = learner2.query(testX) # get the predictions
  rmse2 = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

  return rmse1, rmse2


def ratio(numerator, denominator):
  return 1.0 if denominator == 0 else numerator / denominator


def test_code():

  # create two learners and get data
  lrlearner = lrl.LinRegLearner(verbose = False)
  dtlearner = dt.DTLearner(verbose = False, leaf_size = 1)
  X, Y = best4LinReg(int(np.mod(time.time()*10000, 10000)))

  # compare the two learners
  rmseLR, rmseDT = compare_os_rmse(lrlearner, dtlearner, X, Y)

  # share results
  #    print
  #    print "best4LinReg() results"
  #    print "RMSE LR    : ", rmseLR
  #    print "RMSE DT    : ", rmseDT
  if rmseLR < 0.9 * rmseDT:
    print '.',
  else:
    print "LR >= 0.9 DT:  fail", 'LR RMSE=', rmseLR, 'DT RMSE=', rmseDT
  linear_ratio = ratio(rmseLR, rmseDT)

  # get data that is best for a random tree
  lrlearner = lrl.LinRegLearner(verbose = False)
  dtlearner = dt.DTLearner(verbose = False, leaf_size = 1)
  X, Y = best4DT(int(np.mod(time.time()*10000, 10000)))

  # compare the two learners
  rmseLR, rmseDT = compare_os_rmse(lrlearner, dtlearner, X, Y)

  # share results
  #    print
  #    print "best4DT() results"
  #    print "RMSE LR    : ", rmseLR
  #    print "RMSE DT    : ", rmseDT
  if rmseDT < 0.9 * rmseLR:
    print '.',
  else:
    print "DT >= 0.9 LR:  fail", 'DT RMSE=', rmseDT, 'LR RMSE=', rmseLR
  dt_ratio = ratio(rmseDT, rmseLR)
  return linear_ratio, dt_ratio

start = time.time()
dt_ratios = []
linear_ratios = []
for i in range(100,0,-1) :
  lin_r, dt_r = test_code()
  linear_ratios.append(lin_r)
  dt_ratios.append(dt_r)
  if (i%10) == 1 : print i-1
print 'elapsed time ', time.time()-start, 'secs'
print
print 'best4LinReg() ratios summary'
print pd.Series(linear_ratios).describe()
print
print 'best4DT() ratios summary'
print pd.Series(dt_ratios).describe()


# def test_seeds():
#     total = 1000
#     success_count = 0
#     for seed in xrange(total):
#         lrlearner = lrl.LinRegLearner(verbose=False)
#         dtlearner = dt.DTLearner(verbose=False, leaf_size=1)
#         X, Y = best4DT(seed)
#         rmseLR, rmseDT = compare_os_rmse(lrlearner, dtlearner, X, Y)
#         if rmseDT < 0.9 * rmseLR:
#             success_count += 1
#             if success_count % 100 == 0:
#                 print("Successful: {}".format(success_count))
#         else:
#             print("Failed at seed {}".format(seed))
#     print("Successful iterations: {} out of {}".format(success_count, total))

# if __name__=="__main__":
#     # test_code(446)
#     test_seeds()