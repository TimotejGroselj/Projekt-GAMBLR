import requests
url="https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=364"
url2="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=price_change_percentage_24h_desc&per_page=10&page=1&sparkline=false"
bitcoin_price=requests.get(url).json()
graf_data=requests.get(url2).json()


