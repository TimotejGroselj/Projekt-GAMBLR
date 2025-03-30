import requests
from start import bitcoin_price,graf_data
import datetime


class EMA:
    #from start import bitcoin_price, graf_data
    import datetime

    def __init__(self,time_period,start="0"):
        self.N = time_period
        self.date = start.split()[0]

    def get_EMA_today(self):
        alpha = 2 / (self.N + 1)
        print(bitcoin_price)
        if self.date in [i[0] for i in bitcoin_price['prices']] and self.date != "0":
            raise "Invalid Date"
        #for i in range()


"""
short: N=9,12,20
mid: N=26,50
longshlong: N=100,200
"""
N = 26
alpha = 2/(N+1)
EMAt =1
print(bitcoin_price)
#bull = EMA(26,"2025-03-30")
#print(bull.get_EMA_today())