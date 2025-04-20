import pickle
from matplotlib import pyplot as plt
from update import is_updated
def max_prof(start_mone,obj_coin):
    """
    returns max profit, that we could get
    """
    return (start_mone/min(obj_coin.getprices().values()))*max(obj_coin.getprices().values())
def profit(numbers):
    """
    returns how much we profited according to dict investicij
    """
    return numbers[sorted(numbers.keys())[-1]][1]-numbers[sorted(numbers.keys())[0]][1]

with open("results.bin","rb") as data:
    coini_profit=pickle.load(data)
with open("data.bin", "rb") as data:
    coin_price = pickle.load(data)
is_updated("results")
fig=plt.figure(figsize=[19.2,10.8])
prof=[]
prof_max=[]
proc_prof=[]
št=0
for name,numbers in coini_profit.items():
    prof.append(profit(numbers))
    prof_max.append(max_prof(numbers[sorted(numbers.keys())[0]][1],coin_price[name]))
    proc_prof.append(prof[-1]/numbers[sorted(numbers.keys())[0]][1])
    print(f"Profit pri {name}: {prof[-1]}")
    #claculate profit of bot and max possible profit for each coin
    plt.text(-0.3+št*1,prof_max[-1]+100,f"{round(prof_max[-1],2)}$")
    plt.text(-0.3+št*1,prof[-1]+100,f"{round(prof[-1],2)}$")
    št+=1
    #adds text on graphs in appropriate locations so they are aligned with bars
plt.bar(coini_profit.keys(),prof,zorder=2,edgecolor = 'k',label="Profiti bota")
plt.bar(coini_profit.keys(),prof_max,edgecolor = 'k',label="Največji možni profiti")
plt.plot(coini_profit.keys(),[0 for _ in range(len(coini_profit.keys()))],color="k")
plt.legend()
plt.xlabel("coin")
plt.ylabel("profit")
plt.show()
plt.close()
#draws bar graph
print(f"Povprečno bot vrne {100+100*(sum(proc_prof)/len(proc_prof))}% začetne investicije")
    
    