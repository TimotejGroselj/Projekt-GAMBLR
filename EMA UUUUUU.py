import requests
from start import bitcoin_price,graf_data
import datetime

def get_EMA_today(N,smoothing=2):
    """
    :param N:za kok dni te zanima
    :param smoothing: basicly konstanta
    :return: vrne vrenost EMA v N tem dnevu
    """
    alpha = smoothing / (N + 1)
    EMAp = 60000 #to se se nastav po potrebi
    for i in range(N):
        date,value = bitcoin_price['prices'][i]
        EMAt = alpha*value + (1-alpha)*EMAp
        EMAp=EMAt
    return EMAt,value


print(get_EMA_today(50))

