from classdat import coin
from datetime import date
import pickle as kumarca


class RSI:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d")):
        def pridobiRSI(sez):
            """Hidden function: pridobi rsi za time period"""
            prej = sez[0]
            gain, loss = 0, 0
            dolz = len(sez)
            for i in range(1, dolz):
                change = prej - sez[i]
                if change > 0:
                    gain += change
                else:
                    loss += abs(change)
                prej = sez[i]
            gain /= dolz
            loss /= dolz
            if loss == 0:
                return 100
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        """
        :param N: na podlagi zadnjih N dni (closing days) izračuna RSI
        :param datum: od katerega datuma nazaj želi izračunat RSI
        """
        with open("data.bin", "rb") as data:
            coin_p = kumarca.load(data)
            slovar_rsi = {}
            for i in coin_p.values():
                kovanc,prices = i.getname(),i.getprices()
                prices = dict(reversed(prices.items()))
                tab = list(prices.values())
                id = list(prices).index(dat)
                dolz, ost = len(tab), len(prices) % N
                pomozn = {}
                for i,datum in enumerate(prices):
                    if i < id:
                        continue
                    if i == dolz - ost:
                        rsi = pridobiRSI(tab[i:])
                        continue
                    elif i > dolz - ost:
                        pomozn[datum] = rsi
                    else:
                        rsi = pridobiRSI(tab[i:i + N])
                        pomozn[datum] = rsi
                pomozn = dict(reversed(pomozn.items()))
                slovar_rsi[kovanc] = pomozn
            self.slovar_rsi = slovar_rsi
            self.N = N

    def RSIforcoin(self,coin):
        """Vrne RSI od določenega datuma nazaj za dani coin"""
        return self.slovar_rsi[coin]


hopagen = RSI(14)
print(hopagen.RSIforcoin('bitcoin'))

