import matplotlib.pyplot as plt
import datetime
from start import bitcoin_price,graf_data

table_bit=bitcoin_price["prices"]
x1=[datetime.datetime.fromtimestamp(int(str(el[0])[:-3])) for el in table_bit]
y=[el[1] for el in table_bit]

fig=plt.figure()
plt.plot(x1,y,label="price graph in USD")
plt.xlabel("date")
plt.ylabel("price in USD")
plt.legend()
plt.show()
