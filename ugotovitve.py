import pickle
with open("results.bin","rb") as data:
        coini=pickle.load(data)
for name,numbers in coini.items():
    print(f"Profit pri {name}: {numbers[sorted(numbers.keys())[-1]][1]-numbers[sorted(numbers.keys())[0]][1]}")