import matplotlib.pyplot as plt
import numpy as np
from math import floor
from ema import EMA
from rsi import RSI

import pickle
from classdat import coin
with open("data.bin","rb") as data:
    coin_prices=pickle.load(data)
    
    fig=plt.figure(figsize=[19.2,10.8])

    for obj_coin in coin_prices.values():
        d=len(obj_coin.getprices())
        break
        
    for obj_coin in coin_prices.values():
        plt.semilogy(list(obj_coin.getprices().keys()),list(obj_coin.getprices().values()),label=obj_coin.getname(),linewidth =2)
        plt.xticks([list(obj_coin.getprices().keys())[i] for i in range(0,d,floor(d/12))])
        plt.title("Prices")
    plt.xlabel("date")
    plt.ylabel("price in USD")
    plt.legend()
    fig.savefig("Prices.pdf",bbox_inches="tight")
    
    fig=plt.figure(figsize=[19.2,10.8])
    for obj_coin in coin_prices.values():
        plt.semilogy(list(obj_coin.getmarket_caps().keys()),list(obj_coin.getmarket_caps().values()),label=obj_coin.getname(),linewidth =2)
        plt.xticks([list(obj_coin.getmarket_caps().keys())[i] for i in range(0,d,floor(d/12))])
    plt.xlabel("date")
    plt.ylabel("market cap in USD")
    plt.title("Market caps")
    plt.legend()
    fig.savefig("Market_caps.pdf",bbox_inches="tight")
    
    for obj_coin in coin_prices.values():
        plt.semilogy(list(obj_coin.gettotal_volumes().keys()),list(obj_coin.gettotal_volumes().values()),label=obj_coin.getname())
        plt.xticks([list(obj_coin.gettotal_volumes().keys())[i] for i in range(0,d,floor(d/12))])
    plt.xlabel("date")
    plt.ylabel("total volume")
    plt.title("Total volumes")
    plt.legend()
    fig.savefig("Total volumes.pdf",bbox_inches="tight")
    
    
    
    for coin_id in coin_prices.keys():
        fig=plt.figure(figsize=[19.2,10.8])
        for N in [2,12,20]:
            plt.plot(list(EMA(N).getcoinEMAs(coin_id).keys()),list(EMA(N).getcoinEMAs(coin_id).values()),label=f"N={N}")
            plt.xticks([list(EMA(N).getcoinEMAs(coin_id).keys())[i] for i in range(0,d,floor(d/12))])
        plt.xlabel("date")
        plt.ylabel(coin_id)
        plt.title(coin_id)
        plt.legend()
        fig.savefig(f"EMAS\\EMAS for {coin_id}.pdf",bbox_inches="tight")
    

    for coin_id in coin_prices.keys():
        fig=plt.figure(figsize=[19.2,10.8])
        for N in [5,14,50]:
            plt.plot(list(RSI(N).RSIforcoin(coin_id).keys()),list(EMA(N).RSIforcoin(coin_id).values()),label=f"N={N}")
            plt.xticks([list(EMA(N).RSIforcoin(coin_id).keys())[i] for i in range(0,d,floor(d/12))])
        plt.xlabel("date")
        plt.ylabel(coin_id)
        plt.title(coin_id)
        plt.legend()
        fig.savefig(f"RSI\\RSI for {coin_id}.pdf",bbox_inches="tight")