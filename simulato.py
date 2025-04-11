import pickle
from experimentus import Gambler
from classdat import coin
def simulato(coin_obj,mone=10000):
    """
    vzame en objekt coin in vrne vn simulacijo trading bota za ta coin
    to vrne v obliki slovarja z 
    ključ=datum 
    vrednost=tuple(repozitori,actuall mone)
    """
    name=coin_obj.getname()
    gamb = Gambler(name,mone,12,26)
    one_coin = coin_obj.getprices()
    states=dict()
    for date in one_coin:
        parameter=gamb.set_param(date)
        signal = gamb.signal(date,parameter,14)
        #nastavimo vrednosti, ki bojo odločale ali bomo kupovali ali ne s pomočjo gamblr classa
        if signal == 1:
            buy=gamb.checkmoni()[1]*abs(gamb.set_buy_sell(date))
            gamb.buy(date,buy)
        elif signal == 0:
            sell=gamb.checkmoni()[1]*abs(gamb.set_buy_sell(date))
            gamb.sell(date,sell)
        #glede na signal, trenutno oddaljenostjo od max/min, ki smo jih dosegli do zdaj in še preostali denar se odloči koliko kupimo/prodamo coina
        states[date]=gamb.checkmoni()
    gamb.sellall(date)
    #na koncu kar imamo prodamo
    states[date]=gamb.checkmoni()
    return states
            
with open("data.bin", "rb") as data:
    coin_prices = pickle.load(data)
coini=dict()
for obj_coin in coin_prices.values():
    coini[obj_coin.getname()]=simulato(obj_coin)
    print("loading...")
    #simuliramo za vsak coin
with open(f"results.bin","wb") as data:
    pickle.dump(coini,data)