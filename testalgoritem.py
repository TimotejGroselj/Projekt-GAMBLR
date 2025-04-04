import datetime
import pickle
from classdat import coin
from ema import EMA
from last_day import yesterday

class bot:
    def __init__(self,cene,km,money=10000):
        """
        cene=sl. classu coin
        money=mone to spend
        km=procent kolk mone dava notr/vn glede na izračunano številko  
        """
        self.investicije=dict()
        #ključ:datum
        #vrednost:vložen denar (-float)/pobran denar ven(float) sprot updatas money
        #če na dan nč ne nrdiš ni elementa
        self.cene=cene
        self.km=km
        self.mone=money
    def invest(self,date,amount):
        """
        pove kolko investirat kir dan
        in prever če mava dost dnarja
        če lhka še vseen investirava sam hočeva preveč investirava kkr lhka
        pozitivn amount: izplacava nek amount
        negativn amount: vlozva nek amount
        """
        if sum(list(self.investicije.values()))+amount<=self.mone:
            self.investicije[date]=amount
            self.mone+=amount
        elif sum(list(self.investicije.values()))<=self.mone:
            self.investicije[date]=self.mone-sum(list(self.investicije.values()))
            self.mone=0
        return None
        
class EMA_bot(bot):
    """
    bot, ki simulira obnašanje eme
    kdm=koef kuk agresivno ema vpliva
    N=idk
    """        
    def __init__(self, cene, km, kdm, N, money=10000):
        super().__init__(cene, km, money)
        self.kdm=kdm
        self.N=N
        
    def calculato_faze(self,do_dneva,coin_id):
        """
        do dneva je str oblike '%Y-%m-%d', ki pove do katerega datuma upošteva podatke
        ter vrne slovar oblike {dan:efekt emme} ki bo pol odloču kaj se zgodi investiciji tist dan za en coin
        """

        ema=EMA(self.N,do_dneva).getcoinEMAs(coin_id)
        date_range=sorted(list(ema.keys()))

        le_god=dict()
        for key in date_range[1:]:
            le_god[key]=(ema[yesterday]-ema[key])*self.kdm
            
        return le_god
    
    def decision_maker(self,god_param_invest,god_param_dropout,do_dneva,coin_id):
        """
        glede na god param se odloč al bomo kupl al prodal
        """
        how_much_coin=0
        #very much to do sam mam dost basicly nekak morva vedt kuk coina mava de veva u kuk dnarja se nama investicije prevedejo
        #a to misls kok npr. bitocina je vredn $10 000 ? -> k pol je to sam ($10 000 aka self.mone)/(trenutna cena btc-ja v $).
        for key,val in self.calculato_faze(do_dneva,coin_id):
            if val>god_param_invest:
                kok_dnarja=(val-god_param_invest)*self.km*self.mone
                self.invest(key,-kok_dnarja)
                kok_coina=kok_dnarja/self.cene[coin_id].getprices()[key]
                how_much_coin+=kok_coina
            if val<god_param_dropout:
                kok_coina=(god_param_dropout-val)*self.km*how_much_coin
                kok_dnarja=kok_coina*self.cene[coin_id].getprices()[key]
                self.invest(key,kok_dnarja)
                how_much_coin+=kok_coina
            if how_much_coin<0:
                how_much_coin=0
