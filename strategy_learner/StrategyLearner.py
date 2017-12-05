"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import datetime as dt
import pandas as pd
import util as ut
import indicators
import numpy as np
import QLearner
import marketsimcode
import random as rand


def get_benchmark(prices , start_val , symbol):
    symbol1 = symbol
    prices_new = prices.copy()
    prices_new.dropna(inplace=True)
    benchmark = prices_new*1000
    left_money = start_val - benchmark[symbol1].iloc[0]
    benchmark = benchmark + left_money
    return benchmark

def compute_portfolio_stats(port_val,rfr , sf):
    daily_return = (port_val[1:] / port_val[0:-1].values)-1
    sddr = daily_return.std()
    adr = daily_return.mean()* (252.0/sf)
    sr  = (sf**0.5) * (adr - rfr )/sddr
    ev = port_val.ix[-1]
    cr = (port_val.iloc[-1]/port_val.iloc[0]) - 1

    print "Cumilatice Return: " , cr[0]
    print "Avg Daily Return: " , adr[0]
    print "Std Daily Return: " , sddr[0]
    print "Port Val: " , port_val.iloc[-1][0]

def get_orders_from_trades(trades, symbol):
    orders = trades.copy(True)

    orders.columns = ["Shares"]
    orders.loc[:, 'Symbol'] = symbol
    orders.loc[:,"Order"] = "NOTHING"
    orders["Order"][(orders["Shares"] < 0)] = "SELL"
    orders["Order"][(orders["Shares"]  >= 0)] = "BUY"

    #orders = orders.drop(orders[orders.Order == "NOTHING"].index)

    orders["Shares"][(orders["Shares"]  < 0)] = -1*orders["Shares"][(orders["Shares"]  < 0)]

    orders = orders[["Symbol","Order","Shares"]]

    return orders

#Should holdings be part of the state ???
class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.qLearner = None
        self.steps , self.number_of_indicators = 5,3

    def author(self):
        return 'snagamalla3' # replace tb34 with your Georgia Tech username.

    def get_thresholds(self,data,steps):
        step_size = int((data.shape[0] + 1)/steps)
        data_sort = data.sort_values(data.columns[0], ascending = True)
        thresholds = []
        for i in range(steps):
            thresholds.append(data_sort.ix[min((i + 1)*step_size , data.shape[0] -1)].values[0])
        return thresholds

    def discretize_data(self,thresholds,data):
        disc_data = data.copy()
        for i in range(len(thresholds)):
            if i == 0:
                disc_data[data <= thresholds[i]] = i
                continue
            # if  i == len(thresholds) - 1 :
            #     #disc_data.iloc[0,data[0] > thresholds[i]] = i
            #     disc_data[data > thresholds[i]] = i
            #     continue

            disc_data[np.logical_and(data <= thresholds[i], data > thresholds[i - 1])] = i
        return disc_data

    def discritize_states(self , price_data , steps):
        disc_inds = self.discretize_indicators(price_data , steps)
        #disc_inds.fillna(0,inplace = True)
        states = disc_inds["BB"]
        states = states.add(disc_inds["SMA"]*steps , fill_value = 0)
        states = states.add(disc_inds["MACD"]*(steps**2) , fill_value = 0)
        final_states = states.sum(axis =1)
        return final_states.astype('int32')

    def discretize_indicators(self , price_data , steps ):
        #Intialize

        ind,ind_data,thresholds = indicators.Indicators(price_data) ,{},{}

        #Get indicator data
        ind_data["SMA"] = ind.simple_moving_averages_indicator()
        ind_data["BB"] = ind.boilinger_bands_indicator()
        ind_data["MACD"] = ind.moving_average_convergence_divergence()

        ind_data["BB"].fillna(0,inplace = True)
        ind_data["SMA"].fillna(0,inplace = True)
        ind_data["MACD"].fillna(0,inplace = True)



        #Get thresholds
        for key,val in ind_data.iteritems():
            # print key , val.shape
            thresholds[key] = self.get_thresholds(val,steps)
        ind_disc = {}
        #print "Thres"
        #Discritize Indicators
        for key,val in thresholds.iteritems():
            thresholds_cur = val
            ind_disc[key] =self.discretize_data(thresholds_cur,ind_data[key])
        return ind_disc

    def executeAction(self ,action,cur_trades ,index):
        if action == 0:
            cur_trades.ix[index] = 0
        elif action == 1:
            cur_trades.ix[index] = 1000 - self.cur_num_stocks
            self.cur_num_stocks = 1000
        elif action == 2:
            cur_trades.ix[index] = -1000 - self.cur_num_stocks
            self.cur_num_stocks = -1000





    def get_state_from_ind(self , inds , steps):
        state = 0
        for i in range(len(inds)):
            state += inds[i]*(steps**i)
        # if state > 124:
        #     print state , inds
        return int(state)

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "UNH", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):

        # add your code to do learning here

        # example usage of the old backward compatible util function
        #print symbol
        syms=[symbol]
        #sd = sd - dt.timedelta(days=2)
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates , False)  # automatically adds SPY
        prices = prices_all[symbol]  # only portfolio symbols
        prices_with_SPY = ut.get_data(syms, dates)[symbol]
        prices = prices_with_SPY.to_frame()
        prices.fillna(method="ffill",inplace=True)
        prices.fillna(method="bfill",inplace=True)

        #print "Training " , prices.shape

        daily_return = (prices[1:] / prices[0:-1].values)-1

        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices

        #Get Discritized Indicator
        steps,number_of_indicators = self.steps,self.number_of_indicators
        #disc_inds = self.discretize_indicators(prices_all , steps)
        states = self.discritize_states(prices_all , steps)

        number_of_states,number_of_actions = steps**number_of_indicators,3
        #Intialize QLearner
        qLearner = QLearner.QLearner (num_states=number_of_states, \
        num_actions = number_of_actions, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False)
        min_iters,max_iters = 10,950
        cur_iter =0

        #make trades as data frame
        cur_trades = prices_with_SPY.copy(True)
        cur_trades.ix[:]=0
        train_trades = cur_trades.copy(True)

        #reward is nothing but daily return
        self.cur_num_stocks = 0
        while  cur_iter < max_iters :
            if cur_iter > min_iters:
                equalTrades = train_trades == cur_trades
                # print "Equal Trades ", np.sum(equalTrades)[0]
                if equalTrades.sum() == equalTrades.shape[0]:
                    break
            #print cur_iter

            train_trades = cur_trades.copy(True)
            start =True
            for row in prices_with_SPY.iteritems():
                #Maintain the order of indicators SMA,BB,MACD
                index  = row[0]

                # if np.isnan(disc_inds["BB"].loc[index][0]):
                #     bb_val = 0
                # else:
                #     bb_val = disc_inds["BB"].loc[index][0]
                # cur_indicators = [disc_inds["SMA"].loc[index][0],bb_val,disc_inds["MACD"].loc[index][0]]
                #cur_state = self.get_state_from_ind(cur_indicators ,steps)
                cur_state = states.ix[index]

                if start:
                    start = False
                    action = qLearner.querysetstate(cur_state)
                    self.executeAction(action,cur_trades ,index)
                    reward = 0
                    continue
                #See how to compute state , reward  and execute action
                state = cur_state
                action = qLearner.query(state,reward)
                reward = self.cur_num_stocks * daily_return.ix[index]
                #print "Exec"
                self.executeAction(action,cur_trades ,index)
                #cur_trades.append(action)
            cur_iter += 1

        self.qLearner = qLearner

        #orders = get_orders_from_trades(train_trades , symbol)
        # print "Training"
        # port_val = marketsimcode.compute_portvals(orders , sd ,ed , start_val=sv , commission=0,impact=0)
        # compute_portfolio_stats(port_val,0,252)
        # print "BenchMark"
        # compute_portfolio_stats(get_benchmark(prices,sv, symbol) , 0 , 252)
        #
        # print orders

        return train_trades.to_frame()

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "UNH", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates , False)  # automatically adds SPY
        prices = prices_all[symbol]  # only portfolio symbols
        prices_with_SPY = ut.get_data(syms, dates)[symbol]
        prices = prices_with_SPY.to_frame()
        prices.fillna(method="ffill",inplace=True)
        prices.fillna(method="bfill",inplace=True)

        #print symbol , prices.shape , sd ,ed
        trades = prices_with_SPY.copy(True)
        trades.ix[:]=0

        steps,number_of_indicators = self.steps,self.number_of_indicators
        #disc_inds = self.discretize_indicators(prices_all , steps)
        states = self.discritize_states(prices_all , steps)

        #print "Done Discretization"


        #make trades as data frame
        self.cur_num_stocks = 0

        for index, row in prices_with_SPY.iteritems():

            #Maintain the order of indicators SMA,BB,MACD
            # if np.isnan(disc_inds["BB"].loc[index][0]):
            #     bb_val = 0
            # else:
            #     bb_val = disc_inds["BB"].loc[index][0]
            # cur_indicators = [disc_inds["SMA"].loc[index][0],bb_val,disc_inds["MACD"].loc[index][0]]
            cur_state = states.ix[index]
            #cur_state = self.get_state_from_ind(cur_indicators ,steps)
            action = self.qLearner.querysetstate(cur_state)
            self.executeAction(action,trades ,index)
        #orders = get_orders_from_trades(trades , symbol)
        # print "Testing"
        # port_val = marketsimcode.compute_portvals(orders , sd ,ed , start_val=sv , commission=0,impact=0)
        # compute_portfolio_stats(port_val,0,252)
        # print "BenchMark"
        # compute_portfolio_stats(get_benchmark(prices,sv , symbol) , 0 , 252)

        # trades = prices_all[[symbol,]]  # only portfolio symbols
        # trades.values[:,:] = 0 # set them all to nothing
        # trades.values[0,:] = 1000 # add a BUY at the start
        # trades.values[40,:] = -1000 # add a SELL
        # trades.values[41,:] = 1000 # add a BUY
        # trades.values[60,:] = -2000 # go short from long
        # trades.values[61,:] = 2000 # go long from short
        # trades.values[-1,:] = -1000 #exit on the last day

        return trades.to_frame()

if __name__=="__main__":
    np.random.seed = 1481090001
    rand.seed = 1481090001
    sl = StrategyLearner()
    sl.addEvidence(symbol="AAPL",sd=dt.datetime(2008,1,1),ed=dt.datetime(2009,12,31),sv=100000)
    sl.testPolicy(symbol="AAPL",sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000)
    sl.testPolicy(symbol="AAPL",sd=dt.datetime(2010,1,1),ed=dt.datetime(2011,12,31),sv=100000)

    print "One does not simply think up a strategy"
