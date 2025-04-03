import matplotlib.pyplot as plt
import pickle
import numpy as np
from classdat import coin
from math import floor


with open("data.bin","rb") as data:
    coin_prices=pickle.load(data)
    
    fig,axs=plt.subplots(2,2,figsize=[19.2,10.8])

    for obj_coin in coin_prices.values():
        d=len(obj_coin.getprices())
        break
        
    for obj_coin in coin_prices.values():
        axs[0][0].semilogy(list(obj_coin.getprices().keys()),list(obj_coin.getprices().values()),label=obj_coin.getname(),linewidth =2)
        axs[0][0].set_xticks([list(obj_coin.getprices().keys())[i] for i in range(0,d,floor(d/6))])
    axs[0][0].set_xlabel("date")
    axs[0][0].set_ylabel("price in USD")
    axs[0][0].set_title("Prices")
    axs[0][0].legend()


    for obj_coin in coin_prices.values():
        axs[0][1].semilogy(list(obj_coin.getmarket_caps().keys()),list(obj_coin.getmarket_caps().values()),label=obj_coin.getname(),linewidth =2)
        axs[0][1].set_xticks([list(obj_coin.getmarket_caps().keys())[i] for i in range(0,d,floor(d/6))])
    axs[0][1].set_xlabel("date")
    axs[0][1].set_ylabel("market cap in USD")
    axs[0][1].set_title("Market caps")
    axs[0][1].legend()
    
    for obj_coin in coin_prices.values():
        axs[1][0].semilogy(list(obj_coin.gettotal_volumes().keys()),list(obj_coin.gettotal_volumes().values()),label=obj_coin.getname())
        axs[1][0].set_xticks([list(obj_coin.gettotal_volumes().keys())[i] for i in range(0,d,floor(d/6))])
    axs[1][0].set_xlabel("date")
    axs[1][0].set_ylabel("total volume")
    axs[1][0].set_title("Total volumes")
    axs[1][0].legend()
axs[1][1].set_axis_off()
fig.savefig("start_data.pdf",bbox_inches="tight")

