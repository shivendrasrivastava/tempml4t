import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data

def calculate_prices(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')
  return price

def calculate_SMA(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')
  # JPMdf = JPMdf/JPMdf.iloc[0]
  rollingDF = pd.rolling_mean(price,window=20)
  return rollingDF

def calculate_EMA(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')
  # JPMdf = JPMdf/JPMdf.ioc[0]
  rollingDF = pd.rolling_mean(price,window=20)
  return rollingDF

def calculate_upper_band(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')

  double_std = 2 * pd.rolling_std(price,window=20)

  upper_band = calculate_SMA(symbols,sd,ed) + double_std 

  return upper_band

def calculate_lower_band(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')

  double_std = 2 * pd.rolling_std(price,window=20)

  lower_band = calculate_SMA(symbols,sd,ed) - double_std

  return lower_band

def calculate_volatility(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')
  price = df.iloc[0:,1:]

  volatility_df = pd.rolling_std(price,window=20)

  return volatility_df

def calculate_momentum(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')
  price = df.iloc[0:,1:]





if __name__ == "__main__":
    # plt.plot(calculate_volatility(), label='Volatility')
    # # plt.plot(calculate_prices(), label='Price')
    # # plt.plot(calculate_SMA(), label='SMA')
    # # plt.plot(calculate_lower_band(), label='lower band')
    # # plt.plot(calculate_upper_band(), label='upper band')
    # plt.plot(calculate_prices()/calculate_SMA(), label='Price/SMA')
    # plt.legend()
    # plt.show()
    print calculate_SMA()
    


