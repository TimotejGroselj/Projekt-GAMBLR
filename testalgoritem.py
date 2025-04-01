###
# parametri:
# delta dane metode
# delta vrednosti
# stanje vrednosti glede na preteklost(a je ful pocen glede na preteklost al ful drg)
# dan "denar"
# procenti za use te vrednosti k jih bo treba zbruteforcat da bojo prou
###

def bot(podatki,money,kdm,kdv,kdp,kdmo):
    investicije=dict()
    #ključ:datum
    #vrednost:vložen denar (-float)/pobran denar ven(float)
    #če na dan nč ne nrdiš ni elementa
    for el in podatki:
        #podatki bojo neki nek iterator v kirm bo datum,ema,cena za cel dataset do datuma
        date=el["date"]
        ema=el["ema"]
        price=el["price"]
        past_low=min(price)
        past_max=max(price)
        
    
    
    return None


