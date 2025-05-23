import requests
import time
import pickle
from classdat import coin


url1="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
response=requests.get(url1)
if response.status_code!=200:
    print("Call limit exceeded!")
else:
    print("Updating...")
    print("This might take cca 5 min.")
graf_data=response.json()
coin_prices=dict()
#gets the names of coins

with open(f"data.bin","wb") as data:
    for el in graf_data:
        time.sleep(15)
        url=f"https://api.coingecko.com/api/v3/coins/{el['id']}/market_chart?vs_currency=usd&days=364"
        response=requests.get(url)
        if response.status_code==200:
            print("Gathering data...")
        else:
            raise Exception("Unable to get data now.Try again!")
        coin_prices[el["id"]]=coin(response.json(),el["id"])
        #gathers data about the coins and puts it into a class
    pickle.dump(coin_prices,data)
print("Update complete!")
#saves classes to a file


