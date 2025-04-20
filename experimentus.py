
from classdat import coin
import pickle 
from ema import EMA
from rsi import RSI
from sma import SMA
from last_day import yesterday


class Gambler:
    def __init__(self,coin:str,money:float,shortN,longN,repository=0):
        """
        :param coin: which coin to invest in
        :param money: how much money are we willing to give
        :param repository: how much "coin" do we have
        :param shortN and longN: short period N and long period N (check SMA.py for extra understanding)
        """
        self.shortN,self.longN = shortN,longN
        self.repository,self.money = repository,money
        self.coin = coin
        with open("data.bin", "rb") as data:
            coin_price = pickle.load(data)
        self.prices = coin_price[coin].getprices()

    def check_money(self):
        """
        :return: how much "coin" do you have and leftover money
        """
        return self.repository,self.money

    def buy(self,date,buywith):
        """
        :param date: on which date are you buying
        :param buywith: how much money do we want to invest in this coin
        :return: Failed if not enough money
        """
        if buywith > self.money:
            return 'Failed'
        self.repository += buywith/self.prices[date]
        self.money -= buywith

    def sell(self,date,sellwith):
        """
        :param date: on which date are you selling
        :param sellwith: how much money we want to take out of repository
        :return: Failed if not enough in repository
        """
        if sellwith > self.repository*self.prices[date]:
            return 'Failed'
        self.money += sellwith
        self.repository -= sellwith/self.prices[date]

    def sellall(self,date):
        """
        :param date: on which date are you exiting aka selling all
        :return: None
        """
        self.money += self.repository*self.prices[date]
        self.repository -= self.repository

    def rsi_yes(self,date,N=14): #TESTIRANO
        """
        :param date: current date
        :param N: check RSI.py
        :return: a buy signal 1 if market is oversold, signal 0 if it is overbought and 0.5 else
        """
        previous_day = yesterday(date)
        if previous_day not in self.prices:
            return 0.5
        rsi_yesterday = RSI(N).getTodayRSI(self.coin,previous_day)
        if rsi_yesterday < 30:
            return 1
        elif rsi_yesterday > 70:
            return 0
        else:
            return 0.5

    def ema_cross(self,date,parameter): #TESTIRANO
        """
        :param date: current date
        :param parameter: what difference are you allowing to be
        :return: buy signal 1 if ema_diff > parameter, hold signal 0.5 if ema_diff is < |parameter| and 0 else
        """
        ema_difference = EMA(self.shortN).getTodayEMA(self.coin,date) - EMA(self.longN).getTodayEMA(self.coin,date)
        if ema_difference > parameter:
            return 1
        if -parameter < ema_difference < parameter:
            return 0.5
        return 0

    def ema_sma(self,date):#TESTIRANO
        """
        :param date: current date 
        :return: signal 1 if at least 3/4 times are ema and sma greater than today's price, 
        signal 0.5 if are less than 3/4 but more than 1/4, 0 else
        """
        price_today = self.prices[date]
        combinations = [[self.shortN,self.shortN],[self.longN,self.longN],[self.longN,self.shortN],[self.shortN,self.longN]]
        #we take different periods to know for sure if we want to buy, sell or hold
        desidion = 0
        for i in combinations:
            ema = EMA(i[0]).getTodayEMA(self.coin,date)
            sma = SMA(i[1]).getTodaySMA(self.coin,date)
            if ema > price_today and sma > price_today: #if both are above price we add 1
                desidion += 1
            elif ema < price_today and sma < price_today: #if both are below price we add 0
                continue
            else:
                desidion += 0.5
        if 4 >= desidion >= 3: #decides whether to buy,hold or sell
            return 1
        if 3 > desidion >= 1:
            return 0.5
        return 0

    def signal(self,date,parameter,N):
        """
        :param date: current date
        :param parameter: check ema_cross function
        :param N: check rsi_yes function
        :return: Gambler decides if he wants to buy (1), sell (0) or hold (0.5), based on approvals of other functions
        """
        aprovals = [self.ema_sma(date),self.rsi_yes(date,N),self.ema_cross(date,parameter)]
        indicator = sum(aprovals)
        if 3 >= indicator >= 2.5:
            return 1 #'Buy'
        if 2 >= indicator >= 1:
            return 0.5 #'Hold'
        else:
            return 0 #'Sell'

    def set_max_pricemin(self,date):
        """
        :param date: to which date are we looking to
        :return: (max price to date, min price to date)
        """
        max=-1
        min = float("Inf")
        for key in sorted(self.prices.keys()):
            if key==date:
                break
            if self.prices[key]>=max:
                max=self.prices[key]
            if self.prices[key]<=min:
                min=self.prices[key]
        return max,min

    def set_buy_sell(self,date):
        """
        :param date: to which date are we looking to get max,min price
        :return: number on interval [-1,1], which shows, how far are we from some medium value (parametrization) in % based on current max and min price
        return -1 => at min price
        return 1 => at max price
        return 0 => at medium price
        """
        sets = self.set_max_pricemin(date)
        max_price=sets[0]
        min_price=sets[1]
        if min_price==max_price:
            return 0
        delta=self.prices[date]-min_price
        return 2*(delta/(max_price-min_price))-1

    def standard_deviation_ish(self,date):
        """
        :param date: to which date are we calculating std
        :return: extra modified std
        """
        average = SMA(14, date).getTodaySMA(self.coin, date)
        part_sum = 0
        for i,dat in enumerate(self.prices):
            part_sum += abs(self.prices[dat] - average)
            if dat == date:break
        return (part_sum/(i+1))
