"""
template for generating data to fool learners (c) 2016 Tucker Balch
"""
from random import randint
import numpy as np
import math

# this function should return a dataset (X and Y) that will work
# better for linear regression than decision trees
def best4LinReg(seed=1489683273):
    np.random.seed(seed)
    X = np.random.standard_normal(size=(100, 4))
    Y = np.random.standard_normal(size=(100))
    return X, Y


# def best4DT(seed=1489683273):
#     np.random.seed(seed)
#     X = np.random.random(size=(100,4))
#     arr = []
#     # for row in X:
#     #     index = np.random.randint(0,4)
#     #     print row[index]
#     #     arr.append(row[index] * 2)
#     # Y = np.array(arr)

#     Y = X[:,2] * np.random.random() + X[:,1] * np.random.random()
#     correlation = np.corrcoef(X[:, 2], Y)
#     # print correlation
#     # print X
#     # print Y
   
#     return X, Y
#     return X, Y

def best4DT(seed=1489683273):
    np.random.seed(seed)
    X = np.random.normal(size=(100, 50))
    Y = np.random.standard_normal(size=(100))
    #Y = np.array([4,4,4,4,4,4,4,4,4,4])
    return X, Y


#best one so far

# def best4DT(seed=1489683273):
#     np.random.seed(seed)
#     X = np.random.random(size=(100, 50))
#     Y = np.random.standard_normal(size=(100))
#     return X, Y

def author():
    return 'hsikka3' #Change this to your user ID

if __name__=="__main__":
    print "they call me Tim."
