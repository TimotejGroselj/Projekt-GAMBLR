from classdat import coin
from datetime import date
import pickle


class SMA:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d")):
        """
        :returns: {every_coin : {every_date:SMA}},where every_date is capped at "dat"
        :param N: how many days are included in an interval
        :param dat: to which date it calculates SMA
        """
        with open("data.bin", "rb") as data:
            coin_p = pickle.load(data)
            sma_dict = {}
            for i in coin_p.values():
                coin, prices = i.getname(), i.getprices()
                prices = dict(reversed(prices.items()))
                tab = list(prices.values())
                id = list(prices).index(dat)
                length,remainder = len(tab),len(prices)%N
                extra = {}
                for i, date in enumerate(prices):
                    if i < id:
                        continue
                    if i >= length - remainder:
                        extra[date] = tab[i]
                    else:
                        extra[date] = sum(tab[i:i + N]) / N
                extra = dict(reversed(extra.items()))
                sma_dict[coin] = extra
        self.sma_dict = sma_dict

    def getcoinSMAs(self,coin):
        """For a given coin, returns SMA for every date: {date:SMA}"""
        return self.sma_dict[coin]

    def getTodaySMA(self,coin,date):
        """Returns today's SMA for a given coin"""
        return self.sma_dict[coin][date]

