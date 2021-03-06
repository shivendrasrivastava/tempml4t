"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""
import numpy as np
import math

def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    X = np.random.standard_normal(size=(100, 16))
    #map onto an equation so LinRegLearner will have an easier time
    Y = X[:,0] + 4*X[:,1] + 3*X[:,2] + 2*X[:,3] + X[:,4] + 4*X[:,5] + 3*X[:,6] + 2*X[:,7] + X[:,8] + 4*X[:,9] + 3*X[:,10] + 2*X[:,11] + X[:,12] + 4*X[:,13] + 3*X[:,14] + 2*X[:,15]
    return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    return np.random.normal(size=(100, 50)), np.random.standard_normal(size=(100))

    # works 99% of the time
    # X = np.random.random(size = (30,80))
    # np.random.seed(seed) 
    # # return a random x, and a y that is just one column of the x
    # return X, np.random.random(size = (30,80))[:,63]

def author():
    return 'hsikka3' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
