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

class bot:
    def __init__(self,cene,kdv,kdp,km,money=10000):
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
        self.kdp=kdp
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
    def __init__(self, cene, kdv, kdp, km, kdm, money=10000):
        super().__init__(cene, kdv, kdp, km, money)
        self.kdm=kdm
    def calculato_faze(self,do_dneva):
        """
        do dneva je str oblike '%d-%m-%Y', ki pove do katerega datuma upošteva podatke
        ter vrne le magič number, ki bo pol odločla kaj se zgodi investiciji
        """
        
        
    


