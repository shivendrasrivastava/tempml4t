import numpy as np
import pandas as pd
from util import get_data
import datetime as dt

class Indicators:

    def __init__(self,price_data , time_period = 5):
        self.price_data = price_data
        self.time_period = time_period
        self.price_data.fillna(method="ffill",inplace=True)
        self.price_data.fillna(method="bfill",inplace=True)

    def boilinger_bands_indicator(self):
        price_data = self.price_data.copy()
        price_data["SMA"] = pd.rolling_mean(self.price_data,self.time_period,0)
        price_data["std"] = pd.rolling_std(self.price_data,self.time_period , min_periods =1)
        price_data.fillna(0,inplace=True)
        price_data["bb"] = price_data.iloc[:,0]
        price_data["bb"]= (price_data.iloc[:,0] - price_data.iloc[:,1])/(2*price_data.iloc[:,2])
        boilinger_band_ind = pd.DataFrame(price_data["bb"] , index=price_data.index)
        return boilinger_band_ind

    def simple_moving_averages_indicator(self):
        price_data = self.price_data.copy()
        price_data["SMA"] = pd.rolling_mean(self.price_data,self.time_period,0)
        smaInd = (price_data.iloc[:,0]/price_data.iloc[:,1])
        price_data = price_data/price_data.iloc[0]
        price_data["smaInd"] = smaInd
        return  pd.DataFrame(price_data["smaInd"] , index=price_data.index)


    def moving_average_convergence_divergence(self):
        price_data = self.price_data.copy()
        #print "Init = " , price_data.shape

        price_data["ema26"] = pd.ewma(self.price_data, span=26)
        # print "EMA26 = " , price_data.shape
        price_data["ema12"] = pd.ewma(self.price_data, span=12)
        # print "EMA12 = " , price_data.shape
        macd = pd.DataFrame(price_data["ema12"]  - price_data["ema26"] , columns=["MACD"], index=price_data.index)

        # print "MACD = " , macd.shape

        macd["Signal"] = pd.ewma(macd,span=9)
        macd["Indicator"] = macd["MACD"] - macd["Signal"]

        # print "MACD Final = " , macd.shape

        macd_indicator = pd.DataFrame(macd["Indicator"] , index=price_data.index)
        # print "MACD INd = " , macd_indicator.shape

        return macd_indicator



# sd = dt.datetime(2008,1,1)
# ed = dt.datetime(2009,12,31)
# dates = pd.date_range(start=sd, end=ed)
# syms = ['JPM']
# price_data = get_data(syms,dates,False)
# ind = Indicators(price_data,time_period=10)
# sma = ind.simple_moving_averages_indicator()
# bbi = ind.boilinger_bands_indicator()
# macd = ind.moving_average_convergence_divergence()
#
# print sma.head(5) , np.max(sma) , np.min(sma)
# print bbi.head(5) , np.max(bbi) , np.min(bbi)
# print macd.head(5) , np.max(macd) , np.min(macd)
#
# print "Done Indicators"
#save_plot_data(bb,"bb" ,"Data" , "BB")


