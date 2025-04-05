import datetime
from ema import EMA
from last_day import yesterday
import pickle
from classdat import coin
with open("data.bin","rb") as data:
    coin_prices=pickle.load(data)
    
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
        self.delaunmone=money
        for key in self.cene:
            self.dates=self.cene[key].getdates()
            break
    def invest(self,date,amount):
        """
        pove kolko investirat kir dan
        in prever če mava dost dnarja
        če lhka še vseen investirava sam hočeva preveč investirava kkr lhka
        pozitivn amount: izplacava nek amount
        negativn amount: vlozva nek amount
        """
        if sum(list(self.investicije.values()))+amount<=self.delaunmone:
            self.investicije[date]=amount
            self.delaunmone+=amount
        elif sum(list(self.investicije.values()))<=self.delaunmone:
            self.investicije[date]=self.delaunmone-sum(list(self.investicije.values()))
            self.delaunmone=0
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
        #a to misls kok npr. bitocina je vredn $10 000 ? -> k pol je to sam ($10 000 aka self.delaunmone)/(trenutna cena btc-ja v $).
        for key,val in self.calculato_faze(do_dneva,coin_id):
            if val>god_param_invest:
                kok_dnarja=(val-god_param_invest)*self.km*self.delaunmone
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
    def simulato(self,god_param_invest,god_param_dropout):
        """
        simulira delovanje eme za eno leto za vse coine
        """
        result=dict()
        for coin_obj in self.cene:
            coin_id=coin_obj.getname()
            for datum in self.dates:
                self.decision_maker(god_param_invest,god_param_dropout,datum,coin_id)
            result[coin_id]={"mone":self.delaunmone,"investicije":self.investicije}
            self.investicije=dict()
            self.delaunmone=self.mone
        return result


with open("data.bin","rb") as data:
    coin_prices=pickle.load(data) 
trainer=EMA_bot(coin_prices,0.2,1,20) 
print(trainer.simulato(0,0))

        