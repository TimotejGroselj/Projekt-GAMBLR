
from classdat import coin
from datetime import date
import pickle 


class EMA:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d"),smoothing=2):
        """
        :returns: {every_coin : {every_date:EMA}},where every_date is capped at "dat"
        :param N: how many days are included in an interval
        :param dat: to which date it calculates EMA
        :param smoothing: factor, which "adjust" EMA with an actual coin price
        """
        with open("data.bin","rb") as data:
            coin_p = pickle.load(data)
            alpha = smoothing / (N + 1)
            ema_dict = {}
            for i in coin_p.values():
                coin,prices = i.getname(),i.getprices()
                EMAp = 0
                pomozn = {}
                for date in prices:
                    if EMAp == 0:
                        EMAp = prices[date]
                    value = prices[date]
                    EMAt = alpha * value + (1 - alpha) * EMAp
                    pomozn[date] = EMAt
                    EMAp = EMAt
                    if date == dat: break
                ema_dict[coin] = pomozn
        self.ema_dict = ema_dict

    def getcoinEMAs(self,coin):
        """For a given coin, returns EMA for every date: {date:EMA}"""
        return self.ema_dict[coin]

    def getTodayEMA(self,coin,date):
        """Returns today's EMA for a given coin"""
        return self.ema_dict[coin][date]







