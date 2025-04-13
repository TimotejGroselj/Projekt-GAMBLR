from classdat import coin
from datetime import date
import pickle as kumarca
import time
import subprocess

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
                if dat not in list(prices):
                    print("Podatki niso posodobljeni!")
                    time.sleep(2)
                    print("Začenjam s posodobitvijo.")
                    subprocess.run(["python", 'start.py'])
                    print("Nadaljujem s programom.")
                    time.sleep(2)
                id = list(prices).index(dat)
                dolz, ost = len(tab), len(prices) % N
                pomozn = {}
                for i,datum in enumerate(prices):
                    if i < id:
                        continue
                    if i == dolz - ost:
                        rsi = pridobiRSI(tab[i:])
                        pomozn[datum] = rsi
                        continue
                    elif i > dolz - ost:
                        pomozn[datum] = rsi
                    else:
                        rsi = pridobiRSI(tab[i:i + N])
                        pomozn[datum] = rsi
                pomozn = dict(reversed(pomozn.items()))
                slovar_rsi[kovanc] = pomozn
            self.slovar_rsi = slovar_rsi

    def getcoinRSIs(self,coin):
        """Vrne RSI do določenega datuma za dani coin"""
        return self.slovar_rsi[coin]

    def getTodayRSI(self,coin,date):
        """Vrne današnji RSI"""
        return self.slovar_rsi[coin][date]



