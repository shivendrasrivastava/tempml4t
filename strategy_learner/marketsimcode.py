import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import matplotlib.pyplot as plt

def reset_backend(backend):
    import sys
    del sys.modules['matplotlib.backends']
    del sys.modules['matplotlib.pyplot']
    import matplotlib as mpl
    mpl.use(backend)  # do this before importing pyplot
    import matplotlib.pyplot as plt
    return plt

reset_backend('agg')
def compute_portvals(df_orders, sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,12,31),start_val = 1000000, commission=9.95, impact=0.005):
    #years , months , days =.year,df_orders.index.month , df_orders.index.day
    years , months , days = df_orders.index.year,df_orders.index.month , df_orders.index.day
    start_date = sd
    end_date = ed
    symbols = df_orders.Symbol.unique()


    #Get data of stocks in orders
    prices_all = get_data(symbols.tolist(),pd.date_range(start_date, end_date) , addSPY=False)
    prices_all.fillna(method = 'ffill' , inplace = True)
    prices_all.fillna(method = 'bfill' , inplace = True)

    prices_all.loc[:, 'Cash'] = 0
    prices_all['Cash'].values[0:] =1.0
    prices_all['Cash'] = prices_all['Cash'].astype(float)
    prices_filtered = pd.concat([prices_all, df_orders], axis=1, join_axes=[df_orders.index])
    prices_filtered = prices_filtered.drop(['Symbol','Order', 'Shares'] , axis = 1)
    prices_filtered = prices_filtered.drop_duplicates(keep="last")

    trades = prices_all.copy(True)
    trades.iloc[:,:]=0
    for order in df_orders.iterrows():
         order_date,order_stock,order_type,order_quantity  = order[0],order[1][0],order[1][1],order[1][2]
         sign = 1 if order_type == "BUY" else -1
         trades[order_stock].loc[order_date] += sign*order_quantity
         cur_stock_price = prices_all[order_stock][order_date]
         trades["Cash"][order_date] +=  float(-1*(sign + impact)*order_quantity*cur_stock_price) - commission


    holdings = trades.copy(True)


    holdings = holdings.cumsum(axis=0)
    holdings['Cash'] += start_val

    port_values = pd.DataFrame(holdings.values*prices_all.values, columns=holdings.columns, index=holdings.index)
    port_values["PortfolioValue"] = port_values.sum(axis =1)
    portfolioValue = pd.DataFrame(port_values['PortfolioValue']).fillna(0.0)



    return portfolioValue

