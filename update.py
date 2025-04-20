import pickle
from datetime import date
import time
import subprocess

def is_updated(name):
    """
    Updates data if not up to date
    """
    with open(f"{name}.bin", "rb") as data:
        coin_prices = pickle.load(data)
    price_check = coin_prices["bitcoin"].getprices()
    danes = date.today().strftime("%Y-%m-%d")
    if danes not in price_check:
        print("Data not up to date!")
        time.sleep(1)
        if name=="data":
            subprocess.run(["python", 'start.py'])
        else:
            subprocess.run(["python", 'simulato.py'])
        print("Continuing with the program.")
        time.sleep(1)