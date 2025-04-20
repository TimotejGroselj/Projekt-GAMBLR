import datetime
import requests
class coin():
    """
    consits of data about:
    range of dates for which we have data
    dict of prices
    dict of market caps
    dict total volumes
    name of coin
    """
    def __init__(self,json,name):
        self.name=name
        data_=[json["prices"],json["market_caps"],json["total_volumes"]]
        #unpacks values
        data=[dict(),dict(),dict()]
        for i in range(len(data_[0])):
            nice_date=datetime.datetime.fromtimestamp(data_[0][i][0]/1000).strftime("%Y-%m-%d")
            #writes date in a std form for our project
            for j in range(3):
                data[j][nice_date]=data_[j][i][1]
        [self.prices,self.market_caps,self.total_volumes]=data
        #from dict in which values are tuples we create 3 dict for prices market caps and total volumes
        
    def getprices(self):
        return self.prices
    def getmarket_caps(self):
        return self.market_caps
    def gettotal_volumes(self):
        return self.total_volumes
    def getname(self):
        return self.name
    def getdates(self):
        return sorted(list(self.getprices().keys()))
    def __str__(self):
        return f"Data of {self.name} with info about prices,market caps and total volumes from {min(self.getprices().keys())} to {max(self.getprices().keys())}."
    
    