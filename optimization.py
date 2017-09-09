"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data

# PYTHONPATH=..:. python grade_optimization.py
# PYTHONPATH=..:. python optimization.py

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # default values for starting value, risk free rate, and sampling frequency
    sv = 1000000
    rfr = 0.0
    sf = 252.0
    

    prices.fillna(method='ffill', inplace=True)  
    prices.fillna(method='bfill', inplace=True)

    normalized = prices/prices.ix[0]

    guess = []
    for i in range(0,len(syms)):
        guess.append(1.0/len(syms))

    alloc_guess = np.asarray(guess)

    allocs = test_run(alloc_guess, normalized)
    


    # INSERT OPTIMIZATION OF ALLOCATIONS CODE HERE

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    # allocs = np.asarray([0.2, 0.2, 0.3, 0.3, 0.3]) # add code here to find the allocations


    # error when allocs is too low, 4 rather than 5 
    # -- SOLVED: The allocations must be the same length as the syms list

    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats


    # Get daily portfolio value
    port_val = calculate_daily_portfolio_value(normalized, allocs, sv)  # add code here to compute daily portfolio values

    cr = (port_val.ix[-1]/port_val.ix[0]) - 1

    daily_returns = calculate_period_returns(port_val, sf)

    adr = daily_returns.mean() #average daily returns
    sddr = daily_returns.std() #daily return std using DataFrame.std from Pandas

    sr = calculate_sharp_ratio(daily_returns, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        df_norm = df_temp/df_temp.ix[0]
        df_norm.plot()
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.title('Daily Portfolio Value and SPY')
        plt.show()

    return allocs, cr, adr, sddr, sr








#helper functions to calculate stats

def sum_to_one(df):
    return np.sum(df) - 1.0

def test_run(alloc_guess, normed):
    guess = alloc_guess

    min_bounds = []
    for i in alloc_guess:
        min_bounds.append(tuple((0.0, 1.0)))

    min_constraints = ({ 'type': 'ineq', 'fun': sum_to_one})

    result = spo.minimize(compute_sddr,guess,args=(normed,), method='SLSQP',\
        constraints=min_constraints, bounds=min_bounds,options={'disp': True})

    print result.fun
    return result.x

    

# function below is a frankenstein's monster of the functions being used to calculate sddr

def compute_sddr(allocations, norm):
    allocated = norm * allocations
    pos_value = allocated * 1000000
    df = pos_value.sum(axis=1)
    daily_returns = (df/df.shift(1)) - 1
    daily_returns.ix[0] = 0
    daily_returns = daily_returns[1:] 

    return daily_returns.std()


def calculate_daily_portfolio_value(norm, allocations, start_val):
    allocated = norm * allocations
    pos_value = allocated * start_val
    return pos_value.sum(axis=1)


def calculate_period_returns(df, period):
    if period == 252:
        period_returns = (df/df.shift(1)) - 1
        period_returns.ix[0] = 0
        period_returns = period_returns[1:] 
    
    
    return period_returns



def calculate_sharp_ratio(pr, rfr, sf):
    #rfr = 1 + rfr # cumulative rfr
    #drfr = crfr**(1/sf) # taking the sf root of the cumulative rfr
    diff = pr - rfr # storing difference as variable
    fraction = diff.mean()/pr.std() # using equation provided in lecture
    return fraction * np.sqrt(sf)



def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
