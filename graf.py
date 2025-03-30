import matplotlib.pyplot as plt
import datetime
from start import bitcoin_price,graf_data

table=bitcoin_price["prices"]
x=[datetime.datetime.fromtimestamp(int(str(el[0])[:-3])) for el in table]
y=[el[1] for el in table]

fig=plt.figure()
plt.plot(x,y)
plt.show()
