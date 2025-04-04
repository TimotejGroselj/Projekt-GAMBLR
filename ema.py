
from classdat import coin
from datetime import date
import pickle as kumarca

class EMA:
    def __init__(self,N,dat = date.today().strftime("%Y-%m-%d"),smoothing=2):
        """Ustvari slovar,kjer so ključi imena kovancev,
        vrednosti pa slovarji oblike {datum:cena} za vsak datum"""
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
                    value = prices[datum]
                    EMAt = alpha * value + (1 - alpha) * EMAp
                    pomozn[datum] = EMAt
                    EMAp = EMAt
                    if datum == dat: break
                slovar_em[kovanc] = pomozn
        self.slovar_em = slovar_em
        self.N = N

    def getcoinEMAs(self,coin):
        """Vrne slovar {datum:price} em za dani kovanec"""
        return self.slovar_em[coin]



#mmy dodj se datum not k bi mbi dibr sinergiziral (to je definitivno beseda) z rsi in sma in nasplosno machine learning
upam = EMA(45)
print(upam.getcoinEMAs("bitcoin"))
print(upam.getLatestEMA("bitcoin"))





