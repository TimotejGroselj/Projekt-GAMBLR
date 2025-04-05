import random
from classdat import coin
import pickle as kumarca
from ema import EMA
from rsi import RSI
from sma import SMA
from last_day import yesterday

class Gambler:
    def __init__(self,coin:str,dinarcki:float,shortN,longN,repozitorij=0):
        """
        :param coin: za kateri kovanec bomo računal
        :param dinarcki: koliko denarja smo pripravljeni zgamblat
        :param repozitorij: kolk dinarcka mamo notr (v crpyto ceni)
        :param shortN and longN: en N iz krajse dobe in en N iz daljse
        """
        self.shortN,self.longN = shortN,longN
        self.repozitorij,self.dinarcki = repozitorij,dinarcki
        self.coin = coin
        with open("data.bin", "rb") as data:
            coin_price = kumarca.load(data)
        self.prices = coin_price[coin].getprices()

    def buy(self,datum,buywith):
        """
        :param datum: na kateri dan bomo kupili
        :param buywith: koliko želimo kupit $
        :return:
        """
        if buywith > self.dinarcki:
            return 'Failed'
        self.repozitorij += buywith/self.prices[datum]
        self.dinarcki -= buywith
        return 'Succeeded'

    def sell(self,datum,sellwith):
        """
        :param datum: na kateri dan bomo prodali
        :param sellwith: koliko želimo prodat
        :return:
        """
        if sellwith > self.repozitorij*self.prices[datum]:
            return 'Failed'
        self.dinarcki += sellwith
        self.repozitorij -= sellwith/self.prices[datum]
        return 'Succeeded'

    def rsi_yes(self,datum,N=14):
        """Indicira a je market oversold, overbought al pa None"""
        rsi_vceri = RSI(N).getTodayRSI(self.coin,yesterday(datum))
        if rsi_vceri < 30:
            return 1
        elif rsi_vceri > 70:
            return 0
        else:
            return 0.5

    def ema_cross(self,datum,parameter):
        """Ce short Ema - long Ema = nek parameter, potem strong buy, holda sam če je v rangu parametra"""
        razlika_em = EMA(self.shortN).getTodayEMA(self.coin,datum) - EMA(self.longN).getTodayEMA(self.coin,datum)
        if razlika_em > parameter:
            return 1
        if -parameter < razlika_em < parameter:
            return 0.5
        return 0

    def ema_sma(self,datum):
        """Če je overall cena nad emo in sma se kup, če je vmes se holda, sicer proda"""
        cena_danes = self.prices[datum]
        combinacije = [[self.shortN,self.shortN],[self.longN,self.longN],[self.longN,self.shortN],[self.shortN,self.longN]]
        sestevk = 0
        for i in combinacije:
            ema = EMA(i[0]).getTodayEMA(self.coin,datum)
            sma = SMA(i[1]).getTodaySMA(self.coin,datum)
            if ema > cena_danes and sma > cena_danes:
                sestevk += 1
            elif ema < cena_danes and sma < cena_danes:
                continue
            sestevk += 0.5
        if 4 >= sestevk >= 3:
            return 1
        if 2.5 >= sestevk >= 1.5:
            return 0.5
        return 0

    def startgambling(self,datum,parameter):
        """Presodi ali bi na dano ceno prodal,kupil al pa holdou"""
        aprovals = [self.ema_sma(datum),self.rsi_yes(datum,14),self.ema_cross(datum,parameter)]
        s_pik = sum(aprovals)
        if 3 >= s_pik >= 2.5:
            return 'Buy'
        elif 2 >= s_pik >= 1.5:
            if aprovals[2] == 1:
                return 'Buy'
            return 'Hold'
        return 'Sell'


long_per = [21, 26, 50]
short_per = [9, 12, 14]
long,short = random.choice(long_per),random.choice(short_per)
kombinacije_per = {}
tab_indikatorjev = ["EMA","RSI","EMAC"] #kjer bodo mesta ubistvu al 1 (kup) al 0 (prodej) al pa 0.5 (drz)

with open("data.bin", "rb") as data:
    coin_price = kumarca.load(data)
kovanc = "bitcoin"
price_k = coin_price[kovanc].getprices()
for datum,price in price_k.items():
    print(datum,price)

