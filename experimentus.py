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
    def set_max(self,datum):
        max=-1
        for key in sorted(self.prices.keys()):
            if key==datum:
                break
            if self.prices[key]>=max:
                max=self.prices[key]
        return max
    def set_min(self,datum):
        min=float("Inf")
        for key in sorted(self.prices.keys()):
            if key==datum:
                break
            if self.prices[key]<=min:
                min=self.prices[key]
        return min
    def set_buy_sell(self,datum):
        """
        vrne številko na intervalu [-1,1], ki nam predstavlja kako daleč od neke srednje vrednostni smo v % glede na maximalno in minimalno ceno, ki smo jo dosegli do zdaj
        return -1 => smo pri min ceni
        return 1 => smo pri max ceni
        return 0 => smo pri sredinski ceni
        """
        maxi=self.set_max(datum)
        mini=self.set_min(datum)
        if mini==maxi:
            return 0
        delta=self.prices[datum]-mini
        return 2*(delta/(maxi-mini))-1

tab_indikatorjev = ["EMA","RSI","EMAC"] #kjer bodo mesta ubistvu al 1 (kup) al 0 (prodej) al pa 0.5 (drz)

with open("data.bin", "rb") as data:
    coin_price = kumarca.load(data)
kovanc = "bitcoin"
price_k = coin_price[kovanc].getprices()
parameter = 400 #odvisn od kovanca
tab_komb = [(9, 21), (12, 21), (14, 21), (9, 26), (12, 26), (14, 26), (9, 50), (12, 50), (14, 50)] #long_per = [21, 26, 50] #short_per = [9, 12, 14]
startmoneh = 10000

#I HOPE THIS DOES THA MACHINUS LERNUS
#Edin rd bi shranjevou na en file (pickle perhaps??)
"""
todo = []
for do in range(3):  # 1.kup/prodej
    b = random.random()
    s = random.random()
    todo.append((b,s))
    todo.append((s,s))
    todo.append((b,b))
todo.append((b,s))

ns = [14] #2.N
for nek_n in range(9):
    n = random.randrange(1,100)
    ns.append(n)

for buy,sell in todo:
    sl_n = {}
    buy *= startmoneh
    sell *= startmoneh
    for n_ in ns:
        gamb = Gambler(kovanc, startmoneh, 12, 26)
        tab = [0,0,0]
        sl_zas = {}
        for i in price_k:
            signal = gamb.signal(i,parameter,14)
            if signal == 1:
                gamb.buy(i,buy)
                tab[0]+=1
            elif signal == 0:
                gamb.sell(i,sell)
                tab[2] += 1
            else:
                tab[1] += 1
            #print(gamb.checkmoni())
        gamb.sellall(i)
        sl_zas[n_] = (gamb.checkmoni()[1],tab)
        #print(gamb.checkmoni()) #drugi parameter ti pove kok mas se v $
    sl_n[(buy, sell)] = sl_zas
# ta sl_n bi rd shranjevou na en file


for i in long_per:
    for n in short_per:
        tab_komb.append((n,i))
print(tab_komb)
"""
"""
"""
#OD TUKI NAPREJ LOH POZENS ZA PROBO

"""
startmoneh = 10000
gamb = Gambler(kovanc,startmoneh,12,26)
tab = [0,0,0]
parameter = 400
buy = startmoneh*0.05
sell = startmoneh*0.03

for i in price_k:
    signal = gamb.signal(i,parameter,14)
    if signal == 1:
        gamb.buy(i,buy)
        tab[0]+=1
    elif signal == 0:
        gamb.sell(i,sell)
        tab[2] += 1
    else:
        tab[1] += 1
    print(gamb.checkmoni())
gamb.sellall(i)
print(gamb.checkmoni()) #drugi parameter ti pove kok mas se v $
print(tab)
#nucam se mby stop-loss in take-profit
"""
startmoneh = 10000
gamb = Gambler(kovanc,startmoneh,12,26)
tab = [0,0,0]
parameter = 400

for i in price_k:
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
    print(gamb.checkmoni())
gamb.sellall(i)
print(gamb.checkmoni()) #drugi parameter ti pove kok mas se v $
print(tab)


#3.parameter odvisn od kovanca


#4.long/short



