import datetime
import time

def getTimeDict():
    
    rawTime = str(datetime.datetime.now())
    timelist = rawTime.split()
    date=timelist[0].split('-')
    time = timelist[1].split(':')
    timeDict = dict()
    timeDict['year'] = int(date[0])
    timeDict['month'] = int(date[1])
    timeDict['day'] = int(date[2])
    timeDict['hour'] = int(time[0])
    timeDict['minute'] = int(time[1])
    timeDict['second'] = float(time[2])
    timeDict['weekday'] = datetime.datetime.today().weekday()
    return timeDict
