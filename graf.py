import matplotlib.pyplot as plt
import numpy as np
from math import floor
from ema import EMA
from rsi import RSI
from sma import SMA
from pathlib import Path

import pickle
from classdat import coin
with open("data.bin","rb") as data:
    coin_prices=pickle.load(data)
    
    for obj_coin in coin_prices.values():
        d=len(obj_coin.getprices())
        break
    
    Path("EMAS").mkdir(parents=True, exist_ok=True)
    for coin_id in coin_prices.keys():
        fig=plt.figure(figsize=[19.2,10.8])
        for N in [2,12,14,26,50]:
            plt.plot(list(EMA(N).getcoinEMAs(coin_id).keys()),list(EMA(N).getcoinEMAs(coin_id).values()),label=f"N={N}")
            plt.xticks([list(EMA(N).getcoinEMAs(coin_id).keys())[i] for i in range(0,d,floor(d/6))])
        plt.xlabel("date")
        plt.ylabel("EMA value")
        plt.title(coin_id)
        plt.legend()
        fig.savefig(f"EMAS\\EMAS for {coin_id}.pdf",bbox_inches="tight")
        plt.close()

    Path("RSI").mkdir(parents=True, exist_ok=True)
    for coin_id in coin_prices.keys():
        fig=plt.figure(figsize=[19.2,10.8])
        for N in [5,14,50]:
            plt.plot(list(RSI(N).getcoinRSIs(coin_id).keys()),list(RSI(N).getcoinRSIs(coin_id).values()),label=f"N={N}")
            plt.xticks([list(RSI(N).getcoinRSIs(coin_id).keys())[i] for i in range(0,d,floor(d/6))])
        plt.xlabel("date")
        plt.ylabel("RSI value")
        plt.title(coin_id)
        plt.legend()
        fig.savefig(f"RSI\\RSI for {coin_id}.pdf",bbox_inches="tight")
        plt.close()

    Path("SMAS").mkdir(parents=True, exist_ok=True)
    for coin_id in coin_prices.keys():
        fig=plt.figure(figsize=[19.2,10.8])
        for N in [2,12,14,26,50]:
            plt.plot(list(SMA(N).getcoinSMAs(coin_id).keys()),list(EMA(N).getcoinEMAs(coin_id).values()),label=f"N={N}")
            plt.xticks([list(SMA(N).getcoinSMAs(coin_id).keys())[i] for i in range(0,d,floor(d/6))])
        plt.xlabel("date")
        plt.ylabel("SMA value")
        plt.title(coin_id)
        plt.legend()
        fig.savefig(f"SMAS\\SMAS for {coin_id}.pdf",bbox_inches="tight")
        plt.close()

    fig,axs=plt.subplots(2,2,figsize=[19.2,10.8])


        
    for obj_coin in coin_prices.values():
        axs[0][0].semilogy(list(obj_coin.getprices().keys()),list(obj_coin.getprices().values()),linewidth =2)
        axs[0][0].set_xticks([list(obj_coin.getprices().keys())[i] for i in range(0,d,floor(d/6))])
        axs[0][0].set_title("Prices")
    axs[0][0].set_xlabel("date")
    axs[0][0].set_ylabel("price in USD")

    for obj_coin in coin_prices.values():
        axs[0][1].semilogy(list(obj_coin.getmarket_caps().keys()),list(obj_coin.getmarket_caps().values()),linewidth =2)
        axs[0][1].set_xticks([list(obj_coin.getmarket_caps().keys())[i] for i in range(0,d,floor(d/6))])
    axs[0][1].set_xlabel("date")
    axs[0][1].set_ylabel("market cap in USD")
    axs[0][1].set_title("Market caps")
    for obj_coin in coin_prices.values():
        axs[1][0].semilogy(list(obj_coin.gettotal_volumes().keys()),list(obj_coin.gettotal_volumes().values()))
        axs[1][0].set_xticks([list(obj_coin.gettotal_volumes().keys())[i] for i in range(0,d,floor(d/6))])
    axs[1][0].set_xlabel("date")
    axs[1][0].set_ylabel("total volume")
    axs[1][0].set_title("Total volumes")

    for obj_coin in coin_prices.values():
        axs[1][1].plot(0,0,label=obj_coin.getname(),linewidth =2)
    axs[1][1].set_title("Legend")
    axs[1][1].axis("off")
    axs[1][1].legend(loc="upper left")
    fig.savefig(f"starting_data.pdf",bbox_inches="tight")
    plt.show()
    plt.close()