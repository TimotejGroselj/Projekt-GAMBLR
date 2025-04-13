import random
from classdat import coin
import pickle as kumarca
from ema import EMA
from rsi import RSI
from sma import SMA
from last_day import yesterday
import matplotlib.pyplot as plt

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

    def checkmoni(self):
        """Vrne koliko denarja imas"""
        return self.repozitorij,self.dinarcki

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

    def sellall(self,datum):
        """
        :param datum: na kateri datum bomo izplačali
        :return:
        """
        self.dinarcki += self.repozitorij*self.prices[datum]
        self.repozitorij -= self.repozitorij

    def rsi_yes(self,datum,N=14): #TESTIRANO
        """Indicira a je market oversold, overbought al pa None"""
        vceraj = yesterday(datum)
        if vceraj not in self.prices:
            return 0.5
        rsi_vceri = RSI(N).getTodayRSI(self.coin,vceraj)
        if rsi_vceri < 30:
            return 1
        elif rsi_vceri > 70:
            return 0
        else:
            return 0.5

    def ema_cross(self,datum,parameter): #TESTIRANO
        """Ce short Ema - long Ema = nek parameter, potem strong buy, holda sam če je v rangu parametra"""
        razlika_em = EMA(self.shortN).getTodayEMA(self.coin,datum) - EMA(self.longN).getTodayEMA(self.coin,datum)
        if razlika_em > parameter:
            return 1
        if -parameter < razlika_em < parameter:
            return 0.5
        return 0

    def ema_sma(self,datum): #TESTIRANO
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
            else:
                sestevk += 0.5
        if 4 >= sestevk >= 3: #tuki se da se mau igrt s stevilkami
            return 1
        if 3 > sestevk >= 1:
            return 0.5
        return 0

    def signal(self,datum,parameter,N):
        """Presodi ali bi na dano ceno prodal,kupil al pa holdou"""
        aprovals = [self.ema_sma(datum),self.rsi_yes(datum,N),self.ema_cross(datum,parameter)]
        s_pik = sum(aprovals)
        if 3 >= s_pik >= 2.5:
            return 1 #'Buy'
        if 2 >= s_pik >= 1:
            return 0.5 #'Hold'
        else:
            return 0 #'Sell'

    def set_max_min(self,datum):
        """
        max cena do datuma in min cena do datuma
        """
        max=-1
        min = float("Inf")
        for key in sorted(self.prices.keys()):
            if key==datum:
                break
            if self.prices[key]>=max:
                max=self.prices[key]
            if self.prices[key]<=min:
                min=self.prices[key]
        return max,min

    def set_buy_sell(self,datum):
        """
        vrne številko na intervalu [-1,1], ki nam predstavlja kako daleč od neke srednje vrednostni smo v % glede na maximalno in minimalno ceno, ki smo jo dosegli do zdaj
        return -1 => smo pri min ceni
        return 1 => smo pri max ceni
        return 0 => smo pri sredinski ceni
        """
        mami = self.set_max_min(datum)
        maxi=mami[0]
        mini=mami[1]
        if mini==maxi:
            return 0
        delta=self.prices[datum]-mini
        return 2*(delta/(maxi-mini))-1

    def standard_deviation_ish(self,datum):
        povp = SMA(14, datum).getTodaySMA(self.coin, datum)
        vsota = 0
        for i,date in enumerate(self.prices):
            vsota += abs(self.prices[date] - povp)
            if date == datum:break
        return (vsota/(i+1))

tab_indikatorjev = ["EMA","RSI","EMAC"] #kjer bodo mesta ubistvu al 1 (kup) al 0 (prodej) al pa 0.5 (drz)

with open("data.bin", "rb") as data:
    coin_price = kumarca.load(data)
kovanc = "solana"


price_k = coin_price[kovanc].getprices()
tab_komb = [(9, 21), (12, 21), (14, 21), (9, 26), (12, 26), (14, 26), (9, 50), (12, 50), (14, 50)] #long_per = [21, 26, 50] #short_per = [9, 12, 14]
#tab_komb = [(9, 21),(9, 26),(9, 50)]
#best combos rsi #14 [(9, 21),(9, 26),(9, 50)],5 [(9,50),(14,50),(12,50)] use 5 or 14
#tuki naprej sm jst uporabu nove stvari in delajo

"""
for short,long in [(9,21)]:
    startmoneh = 10000
    gamb = Gambler(kovanc,startmoneh,short,long)
    tab = [0,0,0]
    for i in price_k:
        parameter = gamb.standard_deviation_ish(i)
        signal = gamb.signal(i,parameter,14)
        if signal == 1:
            buy=gamb.checkmoni()[1]*abs(gamb.set_buy_sell(i))
            gamb.buy(i,buy)
            tab[0]+=1
        elif signal == 0:
            sell=gamb.checkmoni()[1]*abs(gamb.set_buy_sell(i))
            gamb.sell(i,sell)
            tab[2] += 1
        else:
            tab[1] += 1
    gamb.sellall(i)
    print(gamb.checkmoni(),tab,short,long) #drugi parameter ti pove kok mas se v $
"""
best_moni = {'bitcoin': (17304.385583417188, (9, 50)),
             'ethereum': (6695.341925051774, (12, 50)),
             'tether': (10010.789543453964, (14, 50)),
             'ripple': (31538.02492690881, (9, 50)),
             'binancecoin': (10051.823200701618, (9, 50)),
             'solana': (15897.01064578032, (9, 50)),
             'usd-coin': (10000.34919653982, (9, 21)),
             'dogecoin': (12374.218810026, (9, 21)),
             'cardano': (14487.853027886042, (9, 21)),
             'tron': (17411.715821141595, (9, 50))}
short_long_tab = [(9,50),(12,50),(14,50),(9,50),(9,50),(9,50),(9,21),(9,21),(9,21),(9,50)]
