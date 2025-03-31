import requests
import datetime
import time

url1="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
response=requests.get(url1)
if response.status_code!=200:
    print("napaka preveč")
graf_data=response.json()
coin_prices=dict()


with open(f"data.py","w") as data:
    data.write("{")
    for el in graf_data:
        time.sleep(15)
        url=f"https://api.coingecko.com/api/v3/coins/{el['id']}/market_chart?vs_currency=usd&days=364"
        response=requests.get(url)
        print(response)
        coin_prices[el["id"]]=response.json()
        data.write(f"'{el['id']}':"+"{")
        for key in coin_prices[el["id"]]:
            data.write(f"'{key}':[")
            for par in coin_prices[el["id"]][key]:
                par[0]=datetime.datetime.fromtimestamp(par[0]/1000).strftime("%Y-%m-%d %H:%M:%S")
                data.write(f"{par},\n")
            data.write("],")
        data.write("},") 
    data.write("}")      





