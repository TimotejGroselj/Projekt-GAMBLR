# projekt-avtizma
Projekt Jake Perbila in Timoteja Grošlja

Program z uporabo podatkov iz api naslova https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false
pridobi imena najbol popularnih coinov nato z uporabo api https://api.coingecko.com/api/v3/coins/"ime coina"/market_chart?vs_currency=usd&days=364 
in uporabo različnih metod za analiziranje trendov simulira kako bi se obnašal "trading bot", ki sprejema odločitve glede kupovanja ter 
prodajanja določenega kovanca za celo leto. 

Če si želite ogledati grafe, ki prikazujejo začetne podatke, ter grafe različnih metod analiziranja trendov poženite graf.py. 
Če pa vas zanimajo samo končni rezultati bota, ki je "tradal" eno leto z začetnim kapitalom 10000 Eur pa poženite ugotovitve.py.