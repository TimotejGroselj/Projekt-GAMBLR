import pickle
from matplotlib import pyplot as plt
def max_prof(start_mone,obj_coin):
    """
    vrne maximalni profit, ki ga lahko dobiš
    """
    return (start_mone/min(obj_coin.getprices().values()))*max(obj_coin.getprices().values())
def profit(numbers):
    """
    vrne koliko smo profitirali iz slovarja investiciji
    """
    return numbers[sorted(numbers.keys())[-1]][1]-numbers[sorted(numbers.keys())[0]][1]


with open("results.bin","rb") as data:
    coini_profit=pickle.load(data)
with open("data.bin", "rb") as data:
    coin_price = pickle.load(data)
fig=plt.figure(figsize=[19.2,10.8])
prof=[]
prof_max=[]
proc_prof=[]
for name,numbers in coini_profit.items():
    prof.append(profit(numbers))
    prof_max.append(max_prof(numbers[sorted(numbers.keys())[0]][1],coin_price[name]))
    proc_prof.append(prof[-1]/numbers[sorted(numbers.keys())[0]][1])
    print(f"Profit pri {name}: {prof[-1]}")
plt.bar(coini_profit.keys(),prof,zorder=2,edgecolor = 'k')
plt.bar(coini_profit.keys(),prof_max,edgecolor = 'k')
plt.plot(coini_profit.keys(),[0 for _ in range(len(coini_profit.keys()))],color="k")
plt.xlabel("coin")
plt.ylabel("profit")
plt.show()
plt.close()
print(f"Povprečno bot vrne {100+100*(sum(proc_prof)/len(proc_prof))}% začetne investicije")
    
    