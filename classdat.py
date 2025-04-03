import datetime
import requests
class coin():
    def __init__(self,json,name):
        self.name=name
        data_=[json["prices"],json["market_caps"],json["total_volumes"]]
        data=[dict(),dict(),dict()]
        for i in range(len(data_[0])):
            lep_datum=datetime.datetime.fromtimestamp(data_[0][i][0]/1000).strftime("%Y-%m-%d")
            for j in range(3):
                data[j][lep_datum]=data_[j][i][1]
        [self.prices,self.market_caps,self.total_volumes]=data

    def getprices(self):
        return self.prices
    def getmarket_caps(self):
        return self.market_caps
    def gettotal_volumes(self):
        return self.total_volumes
    def getname(self):
        return self.name
    def __str__(self):
        return f"Data of {self.name} with info about prices,market caps and total volumes from {min(self.getprices().keys())} to {max(self.getprices().keys())}."
    
    
url=f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=364"
response=requests.get(url).json()
thingy=coin(response,"bitcoin")
#testerji uncommenti če te zanima kako zgleda
#print(thingy.getprices())
#print()
#print(thingy.getmarket_caps())
#print()
#print(thingy.gettotal_volumes())
#print()
#print(thingy)