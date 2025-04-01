###
# parametri:
# delta dane metode
# delta vrednosti
# stanje vrednosti glede na preteklost(a je ful pocen glede na preteklost al ful drg)
# dan "denar"
# procenti za use te vrednosti k jih bo treba zbruteforcat da bojo prou
###
import datetime
def bot(podatki,money,kdm,kdv,kdp,km):
    """
    money=mone
    kdm=koef v % (vrednosti od 0 do 1) kolk na odločitev vpliva delta eme
    kdv=koef v % (vrednosti od 0 do 1) kolk na odločitev vpliva delta cene
    kdp=koef v % (vrednosti od 0 do 1) kolk na odločitev vpliva razdalja od max in min
    km=koef v % (vrednosti od 0 do 1) kolk mone dava notr/vn glede na izračunano številko

    """
    investicije=dict()
    #ključ:datum
    #vrednost:vložen denar (-float)/pobran denar ven(float) sprot updatas money
    #če na dan nč ne nrdiš ni elementa
    for el in podatki:
        #podatki bojo neki nek iterator v kirm bo datum,ema,cena za cel dataset do datuma
        date=el["date"]
        ema=el["ema"]
        price=el["price"]
        past_low=min(price)
        past_max=max(price)
        dm="delta eme"
        dv="delta vrednosti"
        dp="razdalja od min in max iz preteklosti"
        
        
        
    
    
    return None


