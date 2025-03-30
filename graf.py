import matplotlib.pyplot as plt

from start import bitcoin_price,graf_data

table_bit=bitcoin_price["prices"]
x1=[el[0] for el in table_bit]
y=[el[1] for el in table_bit]

fig=plt.figure()
plt.plot(x1,y,label="price graph in USD")
plt.xlabel("date")
plt.ylabel("price in USD")
plt.legend()
plt.show()
