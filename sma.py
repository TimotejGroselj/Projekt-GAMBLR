from classdat import coin
from datetime import date
import pickle as kumarca


class SMA:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d")):
        """
        :param N: na vsake N dni izračuna SMA
        :param dat: od katerega datuma nazaj želi izračunat SMA
        """
        with open("data.bin", "rb") as data:
            coin_p = kumarca.load(data)
            slovar_sma = {}
            for i in coin_p.values():
                kovanc, prices = i.getname(), i.getprices()
                prices = dict(reversed(prices.items()))
                tab = list(prices.values())
                if dat in list(prices):
                    id = list(prices).index(dat)
                else:
                    raise Exception("Podatki niso posodobljeni. Poženi start.py")
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

    def getcoinSMAs(self,coin):
        """Vrne SMA za dani kovanec"""
        return self.slovar_sma[coin]

    def getTodaySMA(self,coin,datum):
        """Vrne danasnji SMA za dani kovanec"""
        return self.slovar_sma[coin][datum]

