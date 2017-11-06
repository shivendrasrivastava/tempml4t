import pandas as pd
import numpy as np
import datetime as dt
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
from util import get_data, plot_data
from indicators import calculate_prices
from marketsimcode import compute_portvals



def testPolicy(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    prices = calculate_prices([symbol],sd,ed)
    orders_df = prices.copy().drop([symbol],axis=1).assign(Symbol = 'JPM').assign(Order = 'BUY').assign(Shares = 0)

    trades_count = 0
    current_holdings = 0
    for i in range(0,len(prices.values[:,0])):
      current_val = prices.loc[prices.index[i],'JPM']
      previous_val = prices.loc[prices.index[i - 1],'JPM']

      if(i==0):
        orders_df.loc[orders_df.index[i],'Order'] = 'SELL'
        orders_df.loc[orders_df.index[i],'Shares'] = 1000
        current_holdings = -1000
        trades_count+=1
        #do nothing in this iteration
      elif(current_val > previous_val):
        if(current_holdings < 1000):
          orders_df.loc[orders_df.index[i - 1],'Order'] = 'BUY'
          orders_df.loc[orders_df.index[i - 1],'Shares'] = 2000
          current_holdings += 2000
          trades_count+=1
      elif(current_val < previous_val):
        if(current_holdings > -1000):
          orders_df.loc[orders_df.index[i - 1],'Order'] = 'SELL'
          orders_df.loc[orders_df.index[i - 1],'Shares'] = 2000
          current_holdings -= 2000
          trades_count+=1
      else:
        orders_df.loc[orders_df.index[i - 1],'Order'] = 'BUY'
        orders_df.loc[orders_df.index[i - 1],'Shares'] = 0
        

    
    
    return orders_df
        

    

  

def benchmark(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    prices = calculate_prices([symbol],sd,ed)
    
    benchmark_df = prices.copy().drop([symbol],axis=1)
    benchmark_df = benchmark_df.assign(Symbol = 'JPM')
    benchmark_df = benchmark_df.assign(Order = 'BUY')
    benchmark_df = benchmark_df.assign(Shares = 0)
    benchmark_df.iloc[0,2] = 1000

    

    return benchmark_df

def calculate_period_returns(df, period):
    if period == 252:
        period_returns = (df/df.shift(1)) - 1
        period_returns.ix[0] = 0
        period_returns = period_returns[1:] 
    #fill in other periods here
    
    return period_returns

def print_stats(df):
    print '--------- Portfolio Information -----------'
    cum_return = df.iloc[-1]/df.iloc[0] - 1
    daily_returns = calculate_period_returns(df,252)
    mean_dr = daily_returns.mean()
    std_dr = daily_returns.std()
    print 'Cumulative Return -> ', cum_return
    print 'Mean of Daily Returns ->', mean_dr
    print 'Standard Deviation of Daily Returns ->', std_dr
    print 'Final Portfolio Value ->', df[-1]


def testCode():
    benchmark_val = compute_portvals(benchmark(),100000, 0.0, 0.0)
    first_benchmark = benchmark_val.iloc[0]

    bps_val = compute_portvals(testPolicy(), 100000, 0.0, 0.0)
    first_bps = bps_val.iloc[0]

    print '                        '
    print '                        '
    print '                        '

    
    print 'Benchmark'
    print_stats(benchmark_val)
    print '_______________________________________'
    print 'Best Possible Strategy'
    print_stats(bps_val)

    matplotlib.pyplot.plot(benchmark_val/first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(bps_val/first_bps, label='Best Possible Strategy', color='k')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.ylim([0,7])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Benchmark vs BPS - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('best_possible_in_sample.pdf')

if __name__ == "__main__":
    testCode()



    
    