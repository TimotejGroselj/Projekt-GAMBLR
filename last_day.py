import datetime
def yesterday(today):
    """
    sprejme str oblike %Y-%m-%d ki predstavlja datum in vrne vcerjasnji dan v istem formatu
    """
    today=datetime.datetime.strptime(today,"%Y-%m-%d")
    yesterday=today-datetime.timedelta(days=1)
    yesterday=yesterday.strftime("%Y-%m-%d")
    return yesterday

