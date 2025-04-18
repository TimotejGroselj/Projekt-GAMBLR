from classdat import coin
from datetime import date
import pickle 


class RSI:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d")):
        """
        :returns: {every_coin : {every_date:SMA}},where every_date is capped at "dat"
        :param N: how many days are included in an interval
        :param dat: to which date it calculates RSI
        """
        def getRSI(sez):
            """Hidden function: get rsi for elements in sez"""
            previous = sez[0]
            gain, loss = 0, 0
            length = len(sez)
            for i in range(1, length):
                change = previous - sez[i]
                if change > 0:
                    gain += change
                else:
                    loss += abs(change)
                previous = sez[i]
            gain /= length
            loss /= length
            if loss == 0:
                return 100
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        with open("data.bin", "rb") as data:
            coin_p = pickle.load(data)
            rsi_dict = {}
            for i in coin_p.values():
                coin,prices = i.getname(),i.getprices()
                prices = dict(reversed(prices.items()))
                tab = list(prices.values())
                id = list(prices).index(dat)
                length, ost = len(tab), len(prices) % N
                extra = {}
                for i,date in enumerate(prices):
                    if i < id:
                        continue
                    if i == length - ost:
                        rsi = getRSI(tab[i:])
                        extra[date] = rsi
                        continue
                    elif i > length - ost:
                        extra[date] = rsi
                    else:
                        rsi = getRSI(tab[i:i + N])
                        extra[date] = rsi
                extra = dict(reversed(extra.items()))
                rsi_dict[coin] = extra
            self.rsi_dict = rsi_dict

    def getcoinRSIs(self,coin):
        """For a given coin, returns RSI for every date: {date:RSI}"""
        return self.rsi_dict[coin]

    def getTodayRSI(self,coin,date):
        """Returns today's RSI for a given coin"""
        return self.rsi_dict[coin][date]


