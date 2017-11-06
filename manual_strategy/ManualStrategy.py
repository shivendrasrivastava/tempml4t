import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib
matplotlib.use('Agg')


from util import get_data, plot_data
from indicators import calculate_prices, calculate_lower_band, calculate_upper_band, calculate_SMA, calculate_volatility
from marketsimcode import compute_portvals

def checkBBVal(price, sma, std):
    diff = (price-sma)
    bbval = diff/(2*std)
    return bbval



def testPolicy(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    prices = calculate_prices([symbol],sd,ed)
    orders_df = prices.copy().drop([symbol],axis=1).assign(Symbol = 'JPM').assign(Order = 'BUY').assign(Shares = 0)

    sma = calculate_SMA([symbol],sd, ed)
    std = calculate_volatility([symbol],sd,ed)

    current_holdings = 0
    for i in range(0,len(prices.values[:,0])):

      if(i==0):
        orders_df.loc[orders_df.index[i],'Order'] = 'SELL'
        orders_df.loc[orders_df.index[i],'Shares'] = 1000
        current_holdings = -1000
        
        #do nothing in this iteration
      elif(i >= 21):
        #get current price, current sma, and current std for equation
        curr_price = prices.loc[prices.index[i],'JPM']
        curr_sma = sma.loc[sma.index[i], 'JPM']
        curr_std = std.loc[std.index[i], 'JPM']

        bb_val = checkBBVal(curr_price,curr_sma,curr_std)
        
        if(bb_val < -1):
          if(current_holdings < 1000):
            orders_df.loc[orders_df.index[i],'Order'] = 'BUY'
            orders_df.loc[orders_df.index[i],'Shares'] = 2000
            current_holdings += 2000
            
            matplotlib.pyplot.axvline(x=orders_df.index[i], color='r', linestyle='--')
          
        elif(bb_val > 1):
          if(current_holdings > -1000):
            orders_df.loc[orders_df.index[i],'Order'] = 'SELL'
            orders_df.loc[orders_df.index[i],'Shares'] = 2000
            current_holdings -= 2000
            
            matplotlib.pyplot.axvline(x=orders_df.index[i], color='g', linestyle='--')
          
      else:
        orders_df.loc[orders_df.index[i],'Order'] = 'BUY'
        orders_df.loc[orders_df.index[i],'Shares'] = 0
        

   
    return orders_df

    

  

def benchmark(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    prices = calculate_prices([symbol],sd,ed)
    
    benchmark_df = prices.copy().drop([symbol],axis=1)
    benchmark_df = benchmark_df.assign(Symbol = 'JPM')
    benchmark_df = benchmark_df.assign(Order = 'BUY')
    benchmark_df = benchmark_df.assign(Shares = 0)
    benchmark_df.iloc[0,2] = 1000

    # orders = pd.read_csv('./benchmark.csv', index_col='Date', parse_dates=True)
    # print orders

    return benchmark_df

if __name__ == "__main__":

    ## the in sample plots
    benchmark_val = compute_portvals(benchmark(),100000)
    # print benchmark_val
    first_benchmark = benchmark_val.iloc[0]

    manual_strategy = compute_portvals(testPolicy(),100000)
    # print manual_strategy
    first_manual_strategy = manual_strategy.iloc[0]

    matplotlib.pyplot.plot(benchmark_val/first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(manual_strategy/first_manual_strategy, label='Manual Rule Based Trader', color='k')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Portfolio Comparison - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('figures/manual_strategy_in_sample.pdf')
    matplotlib.pyplot.clf()


    ## the out of sample plots, simply exit out of the in sample and out will be presented
    out_benchmark = compute_portvals(benchmark('JPM', dt.datetime(2010,1,1), dt.datetime(2011,12,31)),100000)
    # print out_benchmark
    out_first_benchmark = out_benchmark.iloc[0]

    out_manual_strategy = compute_portvals(testPolicy('JPM', dt.datetime(2010,1,1), dt.datetime(2011,12,31)),100000)
    # print out_manual_strategy
    out_first_manual_strategy = out_manual_strategy.iloc[0]

    matplotlib.pyplot.plot(out_benchmark/out_first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(out_manual_strategy/out_first_manual_strategy, label='Manual Rule Based Trader', color='k')
    matplotlib.pyplot.xlim([dt.datetime(2010,1,1), dt.datetime(2011,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Portfolio Comparison - Out of Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('figures/manual_strategy_out_sample.pdf')
    

    