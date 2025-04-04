from classdat import coin
from datetime import date
import pickle as kumarca


class SMA:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d")):
        """
        :param N: na vsake N dni izračuna SMA
        :param datum: od katerega datuma nazaj želi izračunat SMA
        """
        with open("data.bin", "rb") as data:
            coin_p = kumarca.load(data)
            slovar_sma = {}
            for i in coin_p.values():
                kovanc, prices = i.getname(), i.getprices()
                prices = dict(reversed(prices.items()))
                tab = list(prices.values())
                id = list(prices).index(dat)
                dolz,ost = len(tab),len(prices)%N
                pomozn = {}
                for i, datum in enumerate(prices):
                    if i < id:
                        continue
                    if i >= dolz - ost:
                        pomozn[datum] = tab[i]
                    else:
                        pomozn[datum] = sum(tab[i:i + N]) / N
                pomozn = dict(reversed(pomozn.items()))
                slovar_sma[kovanc] = pomozn
        self.slovar_sma = slovar_sma

    def SMAforcoin(self,coin):
        """Vrne SMA za dani kovanec"""
        return self.slovar_sma[coin]

lala = SMA(5,"22-03-2025") #lesgoooo datum is werking
print(lala.SMAforcoin("bitcoin"))
