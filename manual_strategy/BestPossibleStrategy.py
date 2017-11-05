import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
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

    orders = pd.read_csv('./benchmark.csv', index_col='Date', parse_dates=True)

    return benchmark_df

if __name__ == "__main__":

    
    benchmark_val = compute_portvals(benchmark(),100000, 0.0, 0.0)
    first_benchmark = benchmark_val.iloc[0]

    bps_val = compute_portvals(testPolicy(), 100000, 0.0, 0.0)
    first_bps = bps_val.iloc[0]

    plt.plot(benchmark_val/first_benchmark, label='Benchmark', color='b')
    plt.plot(bps_val/first_bps, label='Best Possible Strategy', color='k')
    plt.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    plt.ylim([0,7])
    plt.xticks(rotation=10)
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Benchmark vs BPS - In Sample')
    plt.legend()
    plt.savefig('figures/best_possible_in_sample.pdf')