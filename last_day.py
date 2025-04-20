import datetime
def yesterday(today):
    """
    takes str of form %Y-%m-%d representing a date and returns yesterdays date in the same format
    """
    today=datetime.datetime.strptime(today,"%Y-%m-%d")
    yesterday=today-datetime.timedelta(days=1)
    yesterday=yesterday.strftime("%Y-%m-%d")
    return yesterday

