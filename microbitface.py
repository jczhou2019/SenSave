from asyncio import _leave_task
import serial
import csv
from currentTime import getTimeDict
import pandas as pd
from csvCreate import startCSV
import datetime
from final_face_detection_v3 import TakeSnapshotAndSave, Face_Recognition
import final_face_detection_v3
import time

'''
Serial code (sensor data)
e = exit code
b = bedroom
k = kitchen
t = toilet
l = living room
o = outside
f = first(sensor nearer to door)
s = second(sensor further from door)

csv format
lastMovement = year/month/day/hour/minute/second/location
elderlyHabits = year/month/day/hour/minute/second/weekday/duration/location
ownerVisitor = year/month/day/hour/minute/second/personCount/elderly
'''
startCSV()

#ser = serial.Serial('COM4', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
ser = serial.Serial('COM4', 115200)

'''
lastMovement = year/month/day/hour/minute/second/location
elderlyHabits = year/month/day/hour/minute/second/weekday/duration/location
ownerVisitor = year/month/day/hour/minute/second/personCount/elderly
'''

firstTrigger = False
secondTrigger = False

def returnPerson():
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = data["elderly"].tail(1)
    return [elderly, personCount]

def strangerEnter():
    timeDict = getTimeDict()
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = data["elderly"].tail(1)

    df = pd.DataFrame({
        'year' : timeDict['year'],
        'month' : timeDict['month'],
        'day' : timeDict['day'],
        'hour' : timeDict['hour'],
        'minute' : timeDict['minute'],
        'second' : timeDict['second'],
        'personCount': [personCount + 1],
        'elderly' : elderly
        })
    df.to_csv('ownerVisitor.csv', mode='a', index=False, header=False)

def strangerLeave():
    timeDict = getTimeDict()
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = data["elderly"].tail(1)

    df = pd.DataFrame({
        'year' : timeDict['year'],
        'month' : timeDict['month'],
        'day' : timeDict['day'],
        'hour' : timeDict['hour'],
        'minute' : timeDict['minute'],
        'second' : timeDict['second'],
        'personCount': [personCount - 1],
        'elderly' : elderly
        })
    df.to_csv('ownerVisitor.csv', mode='a', index=False, header=False)

def elderlyEnter():
    timeDict = getTimeDict()
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = True

    df = pd.DataFrame({
        'year' : timeDict['year'],
        'month' : timeDict['month'],
        'day' : timeDict['day'],
        'hour' : timeDict['hour'],
        'minute' : timeDict['minute'],
        'second' : timeDict['second'],
        'personCount': [personCount],
        'elderly' : elderly
        })
    df.to_csv('ownerVisitor.csv', mode='a', index=False, header=False)

def elderlyLeave():
    timeDict = getTimeDict()
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = False

    df = pd.DataFrame({
        'year' : timeDict['year'],
        'month' : timeDict['month'],
        'day' : timeDict['day'],
        'hour' : timeDict['hour'],
        'minute' : timeDict['minute'],
        'second' : timeDict['second'],
        'personCount': [personCount],
        'elderly' : elderly
        })
    df.to_csv('ownerVisitor.csv', mode='a', index=False, header=False)

def updateLastMovement(location):
    timeDict = getTimeDict()
    df = pd.DataFrame({
        'year' : timeDict['year'],
        'month' : timeDict['month'],
        'day' : timeDict['day'],
        'hour' : timeDict['hour'],
        'minute' : timeDict['minute'],
        'second' : timeDict['second'],
        'location': [location]
        })
    df.to_csv('lastMovement.csv', mode='a', index=False, header=False)

def returnLocation():
    data = pd.read_csv("LastMovement.csv")
    location =data["location"].tail(1).item()
    return location

def elderlyHabitUpdate(location):

    data = pd.read_csv("elderlyHabits.csv")
    year =int(data["year"].tail(1))
    month =int(data["month"].tail(1))
    day =int(data["day"].tail(1))
    hour =int(data["hour"].tail(1))
    minute =int(data["minute"].tail(1))

    startTime = datetime.datetime(year, month, day, hour, minute, 0)
    durationDelta = datetime.datetime.now() - startTime
    durationDeltaSeconds = durationDelta.total_seconds()
    duration = durationDeltaSeconds/(60*60)

    data.loc[data.index[-1] ,['location']] = location
    data.loc[data.index[-1], ['duration']] = duration
    data.to_csv('elderlyHabits.csv', index=False, header=True)

    timeDict = getTimeDict()
    df = pd.DataFrame({
        'year' : [timeDict['year']],
        'month' : [timeDict['month']],
        'day' : [timeDict['day']],
        'hour' : [timeDict['hour']],
        'minute' : [timeDict['minute']],
        'second' : [timeDict['second']],
        'weekday' : [timeDict['weekday']],
        'location' : None
        })
    df.to_csv('elderlyHabits.csv', mode='a', index=False, header=False)

def returnDuration():
    data = pd.read_csv("elderlyHabits.csv")
    year =int(data["year"].tail(1))
    month =int(data["month"].tail(1))
    day =int(data["day"].tail(1))
    hour =int(data["hour"].tail(1))
    minute =int(data["minute"].tail(1))

    startTime = datetime.datetime(year, month, day, hour, minute, 0)
    durationDelta = datetime.datetime.now() - startTime
    durationDeltaSeconds = durationDelta.total_seconds()
    duration = durationDeltaSeconds/(60)
    #unit = minute
    return duration



print('program start')
while True:
    try:
        ser_bytes = ser.read()
        if ser_bytes == b'e':
            print('Close')
            ser.close()
            break

        # elif ser_bytes != b'e' and ser_bytes != b'':
        #     print(ser_bytes) 

        elif ser_bytes == b't':
            elderly, personCount = returnLocation
            if elderly and personCount == 0:
                updateLastMovement('toilet')
                if returnLocation != 'toilet':
                    elderlyHabitUpdate('toilet')

        elif ser_bytes == b'b':
            elderly, personCount = returnLocation
            if elderly and personCount == 0:
                updateLastMovement('bedroom')
                if returnLocation != 'bedroom':
                    elderlyHabitUpdate('bedroom')

        elif ser_bytes == b'k':
            elderly, personCount = returnLocation
            if elderly and personCount == 0:
                updateLastMovement('kitchen')
                if returnLocation != 'kitchen':
                    elderlyHabitUpdate('kitchen')

        elif ser_bytes == b'l':
            elderly, personCount = returnLocation
            if elderly and personCount == 0:
                updateLastMovement('living room')
                if returnLocation != 'living room':
                    elderlyHabitUpdate('living room')

        elif ser_bytes == b'f':
            firstTrigger = True
            print(1)
            if secondTrigger:
                print('leave')
                firstTrigger = False
                secondTrigger = False
                elderly,stranger = returnPerson()
                if stranger > 0:
                    strangerLeave()
                else:
                    elderlyLeave()
                    elderlyHabitUpdate('outside')

        elif ser_bytes == b's':
            secondTrigger = True
            print(2)
            if firstTrigger:
                print('enter')
                firstTrigger = False
                secondTrigger = False

                #image recognition code
                file_name_created = TakeSnapshotAndSave()

                person = Face_Recognition(file_name_created)
        
                time.sleep(5)  
                #return stranger/elderly
                if person == 'elderly':
                    elderlyEnter()
                elif person == 'stranger':
                    strangerEnter()

    except Exception as e:
        ser.close()
        print(e)
        print("Program stopped")
        break
