
from classdat import coin
from datetime import date
import pickle as kumarca

class EMA:
    def __init__(self,N,smoothing=2):
        with open("data.bin","rb") as data:
            coin_p = kumarca.load(data)
            alpha = smoothing / (N + 1)
            slovar_em = {}
            for i in coin_p.values():
                kovanc,prices = i.getname(),i.getprices()
                EMAp = 0
                pomozn = {}
                for datum in prices:
                    if EMAp == 0:
                        EMAp = prices[datum]
                    else:
                        value = prices[datum]
                        EMAt = alpha * value + (1 - alpha) * EMAp
                        pomozn[datum] = EMAt
                        EMAp = EMAt
                slovar_em[kovanc] = pomozn
        self.slovar_em = slovar_em
        self.N = N

    def getcoinEMAs(self,coin):
        return self.slovar_em[coin]

    def getLatestEMA(self,coin):
        day = date.today().strftime("%d-%m-%Y")
        return self.slovar_em[coin][day]




upam = EMA(45)
print(upam.getcoinEMAs("bitocin"))
print(upam.getLatestEMA("bitcoin"))





