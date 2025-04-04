###
# parametri:
# delta dane metode
# delta vrednosti
# stanje vrednosti glede na preteklost(a je ful pocen glede na preteklost al ful drg)
# dan "denar"
# procenti za use te vrednosti k jih bo treba zbruteforcat da bojo prou
###
import datetime
import pickle
from classdat import coin
from ema import EMA
from last_day import yesterday

class bot:
    def __init__(self,cene,kdv,km,money=10000):
        """
        cene=sl. classu coin
        money=mone to spend
        kdv=koef v % (vrednosti od 0 do 1) kolk na odločitev vpliva delta cene
        kdp=koef v % (vrednosti od 0 do 1) kolk na odločitev vpliva razdalja od max in min
        km=procent kolk mone dava notr/vn glede na izračunano številko  
        """
        self.investicije=dict()
        #ključ:datum
        #vrednost:vložen denar (-float)/pobran denar ven(float) sprot updatas money
        #če na dan nč ne nrdiš ni elementa
        self.cene=cene
        self.kdv=kdv
        self.km=km
        self.mone=money
        self.date=list(self.cene.values().keys()).sorted()
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
    """        
    def __init__(self, cene, kdv, km, kdm, N, money=10000):
        super().__init__(cene, kdv, km, money)
        self.kdm=kdm
        self.N=N
    def calculato_faze(self,do_dneva,coin_id):
        """
        do dneva je str oblike '%Y-%m-%d', ki pove do katerega datuma upošteva podatke
        ter vrne slovar oblike {dan:sl} in sl oblike {effekt value:vr,effekt metode:vr}, ki bo pol odloču kaj se zgodi investiciji tist dan za en coin
        """
        coin_obj=self.cene[coin_id]
        coin_p=coin_obj.getprices()
        alldate=coin_obj.getdates()
        if do_dneva not in alldate:
            raise Exception("Invalid date")
        ema=EMA(self.N).getcoinEMAs(coin_id,do_dneva)
        date_range=[]
        for el in alldate:
            if el == do_dneva:
                break
            else:
                date_range.append(el)
        le_god=dict()
        for key in date_range[1:]:
            le_god[key]={"value_ef":(coin_p[yesterday(key)]-coin_p[key])*self.kdv,"method_ef":(ema[yesterday]-ema[key])*self.kdm}
            
        return le_god
    


