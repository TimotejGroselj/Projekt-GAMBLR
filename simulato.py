from update import is_updated
import pickle
from experimentus import Gambler
from classdat import coin

def simulato(coin_obj,short,long,mone=10000):
    """
    vzame en objekt coin in vrne vn simulacijo trading bota za ta coin
    to vrne v obliki slovarja z 
    ključ=datum 
    vrednost=tuple(repozitori,actuall mone)
    """
    name=coin_obj.getname()
    gamb = Gambler(name,mone,short,long)
    one_coin = coin_obj.getprices()
    states=dict()
    for date in one_coin:
        parameter=gamb.standard_deviation_ish(date)
        signal = gamb.signal(date,parameter,14)
        #nastavimo vrednosti, ki bojo odločale ali bomo kupovali ali ne s pomočjo gamblr classa
        if signal == 1:
            buy=gamb.check_money()[1]*abs(gamb.set_buy_sell(date))
            gamb.buy(date,buy)
        elif signal == 0:
            sell=gamb.check_money()[1]*abs(gamb.set_buy_sell(date))
            gamb.sell(date,sell)
        #glede na signal, trenutno oddaljenostjo od max/min, ki smo jih dosegli do zdaj in še preostali denar se odloči koliko kupimo/prodamo coina
        states[date]=gamb.check_money()
    gamb.sellall(date)
    #na koncu kar imamo prodamo
    states[date]=gamb.check_money()
    return states


is_updated() #updates data if necessary

with open("data.bin", "rb") as data:
    coin_prices = pickle.load(data)
coini=dict()
short_long_tab = [(9,50),(12,50),(14,50),(9,50),(9,50),(9,50),(9,21),(9,21),(9,21),(9,50)]
tren = 0
for obj_coin in coin_prices.values():
    obdobje = short_long_tab[tren]
    coini[obj_coin.getname()]=simulato(obj_coin,obdobje[0],obdobje[1])
    print("Loading...")
    tren += 1
    #simuliramo za vsak coin
with open(f"results.bin","wb") as data:
    pickle.dump(coini,data)