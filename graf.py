import matplotlib.pyplot as plt

from start import coin_prices,graf_data

table_bit=coin_prices["prices"]
x=[]
for coin in coin_prices:
    x.append([el[0] for el in coin_prices["prices"][:-1]])
    y=[el[1] for el in coin_prices["prices"][:-1]]

fig=plt.figure()
for coinx in x:
    plt.plot(coinx,y,label="price graph in USD")
    plt.xlabel("date")
    plt.ylabel("price in USD")
    plt.legend()
    plt.show()
