from classdat import coin
from datetime import date
import pickle as kumarca

class RSI:
    def __init__(self,N,datum = date.today().strftime("%d-%m-%Y")):
        """
        :param N: na podlagi zadnjih N dni (closing days) izračuna RSI
        :param datum: od katerega datuma nazaj želi izračunat RSI
        """
        with open("data.bin", "rb") as data:
            coin_p = kumarca.load(data)
            slovar_sma = {}
            for i in coin_p.values():
                kovanc,prices = i.getname(),i.getprices()
                prices = dict(reversed(prices.items()))
                k,countd = 0,0
                gain,loss = 0,0
                for date,price in prices.items():
                    if date == datum:
                        k = 1
                        prej = price
                    if countd == N:
                        break
                    if k == 1:
                        change = prej - price
                        if change < 0:
                            loss += abs(change)
                        else:
                            gain += change
                        prej = price
                        countd += 1
                loss /= N
                gain /= N
                RS = gain / loss
                RSI = 100 - (100 / (1 + RS))
                slovar_sma[kovanc] = {N:RSI}
            self.slovar_sma = slovar_sma
            self.N = N

    def RSIforcoin(self,coin):
        """Vrne RSI za zadnjih N dni za dani coin"""
        return self.slovar_sma[coin][self.N]


hopagen = RSI(5)
print(hopagen.RSIforcoin('bitcoin'))