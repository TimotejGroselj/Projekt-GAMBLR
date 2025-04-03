import datetime
def yesterday(today):
    today=datetime.datetime.strptime(today,"%d-%m-%Y")
    yesterday=today-datetime.timedelta(days=1)
    yesterday=yesterday.strftime("%d-%m-%Y")
    return yesterday

