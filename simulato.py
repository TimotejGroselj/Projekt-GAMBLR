from update import is_updated
import pickle
from experimentus import Gambler
from classdat import coin

def simulato(coin_obj,short,long,mone=10000):
    """
    takes one object of coin and returnes a simulation for said coin
    the simulation is represented as a dict with keys=dates,values=tuple(amount of coin owned,money in the bank)
    """
    name=coin_obj.getname()
    gamb = Gambler(name,mone,short,long)
    one_coin = coin_obj.getprices()
    states=dict()
    for date in one_coin:
        parameter=gamb.standard_deviation_ish(date)
        signal = gamb.signal(date,parameter,14)
        #we set the values that decide if we buy/sell/do nothing with gamblr class
        if signal == 1:
            buy=gamb.check_money()[1]*abs(gamb.set_buy_sell(date))
            gamb.buy(date,buy)
        elif signal == 0:
            sell=gamb.check_money()[1]*abs(gamb.set_buy_sell(date))
            gamb.sell(date,sell)
        #with consideration of signal,current distance to max/min which have been reached to this day and money left in the bank we decide how much we buy/sell
        states[date]=gamb.check_money()
    gamb.sellall(date)
    #at the end we sell everything we have
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
    #simulates for every coin
with open(f"results.bin","wb") as data:
    pickle.dump(coini,data)