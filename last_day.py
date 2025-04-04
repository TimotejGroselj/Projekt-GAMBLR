import datetime
def yesterday(today):
    today=datetime.datetime.strptime(today,"%Y-%m-%d")
    yesterday=today-datetime.timedelta(days=1)
    yesterday=yesterday.strftime("%Y-%m-%d")
    return yesterday

