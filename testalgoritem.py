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
        if sum(list(self.investicije.value()))+amount<=self.mone:
            self.investicije[date]=amount
        elif sum(list(self.investicije.value()))<=self.mone:
            self.investicije[date]=self.mone-sum(list(self.investicije.value()))
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

        ema=EMA(self.N,self.do_dneva).getcoinEMAs(coin_id) #class EMA(N,do_dneva), metoda get coin ima samo en parameter :)
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
        for key,val in self.calculato_faze(do_dneva,coin_id):
            if val>god_param_invest:
                self.investicije[key]=((val-god_param_invest)*self.km)*self.cene[coin_id].getprices()[key]
            if val<god_param_dropout:
                self.investicije[key]=-((god_param_dropout-val)*self.km)*self.cene[coin_id].getprices()[key]
            if how_much_coin<0:
                how_much_coin=0
