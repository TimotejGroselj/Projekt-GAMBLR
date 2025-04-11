import datetime
import requests
class coin():
    """
    vsebuje podatke o:
    range datumov za katere imamo podatke
    sl. cen
    sl. market caps
    sl. total volumnov
    ime coina
    """
    def __init__(self,json,name):
        self.name=name
        data_=[json["prices"],json["market_caps"],json["total_volumes"]]
        #razpakira vrednosti
        data=[dict(),dict(),dict()]
        for i in range(len(data_[0])):
            nice_date=datetime.datetime.fromtimestamp(data_[0][i][0]/1000).strftime("%Y-%m-%d")
            #zapiše datum v std obliko za projekt
            for j in range(3):
                data[j][nice_date]=data_[j][i][1]
        [self.prices,self.market_caps,self.total_volumes]=data
        #iz slovarja kjer so vrednosti pari ustvarimo 3 slovarje za cene market caps in total volumne
        
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
    
    