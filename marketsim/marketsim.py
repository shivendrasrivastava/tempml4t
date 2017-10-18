"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'hsikka3'  # replace tb34 with your Georgia Tech username.

def compute_portvals(orders_file = "./orders/orders-01.csv", start_val = 1000000, commission=9.95, impact=0.005):
    ## Data Frame of Orders
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    # grab symbols from orders for later use
    syms = orders.drop_duplicates('Symbol','first',False).values[:,0]
    # start and end dates
    start_date = orders.index[0]
    end_date = orders.index[-1]

    dates = pd.date_range(start_date, end_date)

    ## Data Frame of Prices
    prices = get_data(syms.tolist(), dates, True, 'Adj Close').assign(Cash = 1.0)

    ## Data Frame of Trades

    trades = prices.copy()
    for column in trades:
        trades[column] = 0

    # loop through orders
    # for each order
        # if BUY
            ## store shares
            ## multiply shares by price on that date, multiply by -1, set to cash
        # if SELL
            ## store shares * -1
            ## multiply shares by price on that date, set to cash

     # set first cash to start val? i don't know if this is necessary

    for index, row in orders.iterrows():
        
        impact_buy = 1.0 + impact
        impact_sell = 1.0 - impact

        if (row['Order'] == 'BUY'):
            trades.loc[index,row['Symbol']] += row['Shares']
            trades.loc[index,'Cash'] += row['Shares'] * ((prices.loc[index,row['Symbol']] * -1) * impact_buy)

        if (row['Order'] == 'SELL'):
            trades.loc[index,row['Symbol']] += row['Shares'] * -1
            trades.loc[index,'Cash'] += row['Shares'] * ((prices.loc[index,row['Symbol']]) * impact_sell)
        
        ## account for commission
        trades.loc[index,'Cash'] -= commission

    ## Data Frame of Holdings
    temp_holdings = trades.copy()
    temp_holdings.loc[start_date,'Cash'] = start_val + temp_holdings.loc[start_date,'Cash']
    holdings = temp_holdings.cumsum(axis=0)

    ##Data Frame of Values
    values = prices * holdings

    return values.sum(axis=1)

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    compute_portvals("./orders/orders-02.csv")
    # compute_portvals("./orders/orders-02.csv")
    # compute_portvals("./orders/orders-03.csv")
    # compute_portvals("./orders/orders-04.csv")
    # compute_portvals("./orders/orders-05.csv")
    # compute_portvals("./orders/orders-06.csv")
    # compute_portvals("./orders/orders-07.csv")
    # compute_portvals("./orders/orders-08.csv")
    # compute_portvals("./orders/orders-09.csv")
    # compute_portvals("./orders/orders-10.csv")
    # compute_portvals("./orders/orders-11.csv")
    # compute_portvals("./orders/orders-12.csv")