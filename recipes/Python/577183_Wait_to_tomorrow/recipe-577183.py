def waitToTomorrow():
    """Wait to tommorow 00:00 am"""

    tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), 
                         hour=0, minute=0, second=0)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds)
