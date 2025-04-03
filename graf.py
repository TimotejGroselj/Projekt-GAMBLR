import matplotlib.pyplot as plt
import pickle
from classdat import coin
from math import floor


with open("data.bin","rb") as data:
    coin_prices=pickle.load(data)
    
    fig=plt.figure(figsize=[19.2*0.8,10.8*0.8])

    for obj_coin in coin_prices.values():
        d=len(obj_coin.getprices())
        break
        
    for obj_coin in coin_prices.values():
        plt.semilogy(list(obj_coin.getprices().keys()),list(obj_coin.getprices().values()),label=obj_coin.getname(),linewidth =2.5,)
        plt.xticks([list(obj_coin.getprices().keys())[i] for i in range(0,d,floor(d/12))])
    plt.xlabel("date")
    plt.ylabel("price in USD")
    plt.legend()

    plt.show()
