
from data import sl_kuvancou
import datetime
import os
import requests
url1="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"

def get_EMAs(coin,N,smoothing=2):
    tab = []
    """
    :param N:za kok dni te zanima
    :param smoothing: basicly konstanta
    :return: vrne vrenost EMA v N tem dnevu
    """
    coin_price = sl_kuvancou[coin]
    povp = 0
    for i in range(N):
        date,value = coin_price['prices'][i]
        povp += value
    alpha = smoothing / (N + 1)
    EMAp = povp/N
    for i in range(N,len(coin_price['prices'])):
        date,value = coin_price['prices'][i]
        EMAt = alpha*value + (1-alpha)*EMAp
        tab.append([EMAt, value, date])
        EMAp=EMAt
    return tab


#def EMA_today(coin,N):
js = requests.get(url1).json()
sl = {}
for i in js:
    print(i['id'],str(datetime.datetime.today())[:-7],i['current_price'])

times = [9,12,26,50,100,200]



"""
last_emas = {}
for i in sl_kuvancou:
    last_emas[i] = {9:"",12:"",26:"",50:"",100:"",200:""}

tabd = []
for coin in sl_kuvancou:
    for i in times:
        file_p = os.path.join(f"EMA_{coin}",f"Time_{i}.txt")
        tab = get_EMAs(coin, i)
        with open(file_p,"r") as f:
            for line in f:
                pass
            last = line[:-1]
            tabd.append(last.split(','))


tab_index = 0
for crypto in sl_kuvancou:
    for period in times:
        last_emas[crypto][period] = tabd[tab_index]
        tab_index += 1
print(last_emas)
"""

"""
for coin in sl_kuvancou:
    name = f'EMA_{coin}'
    os.makedirs(name)
    for i in times:
        file_p = os.path.join(name,f"Time_{i}.txt")
        tab = get_EMAs(coin, i)
        with open(file_p,"w") as f:
            for t in tab:
                line = f"{t[0]},{t[1]},{t[2]}\n"
                f.write(line)

"""
