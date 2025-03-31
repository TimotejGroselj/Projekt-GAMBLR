import requests
import datetime
import time

url1="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
response=requests.get(url1)
if response.status_code!=200:
    print("napaka preveč")
graf_data=response.json()
coin_prices=dict()


while len(graf_data)!=len(coin_prices):
    for el in graf_data:
        #print(el["id"])
        if el['id'] not in coin_prices:
            url=f"https://api.coingecko.com/api/v3/coins/{el['id']}/market_chart?vs_currency=usd&days=364"
            response=requests.get(url)
            print(response)
            if response.status_code==200:
                coin_prices[el["id"]]=response.json()
                with open(f"{el['id']}","w") as data:
                    for key in coin_prices[el["id"]]:
                        data.write(f"{key}:\n")
                        for par in coin_prices[el["id"]][key]:
                            par[0]=datetime.datetime.fromtimestamp(par[0]/1000)
                            data.write(f"\t{par}\n")

                            
            else:
                time.sleep(5)




