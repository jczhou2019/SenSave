import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import datetime
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
from tele_notification import send_alert_abnormal, send_alert_not_moving, send_alert_elderleave, send_alert_strangerleave

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

locationIDDict = {
    'bedroom' : 1,
    'kitchen' : 2,
    'toilet' : 3,
    'living room' : 4,
    'outside' : 0}

IDLocationDict = {v: k for k, v in locationIDDict.items()}

# print(IDLocationDict)

data = pd.read_csv("elderlyHabits.csv")

if data["duration"].isna().sum() > 0:

    lasttime = datetime.datetime(data["year"].loc[data.index[-1]],
     data["month"].loc[data.index[-1]],
     data["day"].loc[data.index[-1]],
     data["hour"].loc[data.index[-1]], 
     data["minute"].loc[data.index[-1]],
     data["second"].loc[data.index[-1]])

    duration = datetime.datetime.now() - lasttime
    durationDeltaSeconds = duration.total_seconds()
    duration = durationDeltaSeconds/(60*60)
    data.fillna(duration, inplace=True)

resultlist= list()

for i in range(len(data.index)):
    encodeLocation =locationIDDict[data["location"].loc[i]]

    hour = data["hour"].loc[i]
    minute = data["minute"].loc[i]
    seconds = data["second"].loc[i]

    basebin = int(hour)*6 + int(minute)//10 
    multiple = int(data["duration"].loc[i]*6//1)
    #print(multiple)
    dayweek = data["weekday"].loc[i]
    count = 0

    for i in range(multiple):
        bin = (basebin + count) % 144
        tempweekday = dayweek + (basebin + count) // 144
        weekday = tempweekday % 7 
        
        resultlist.append([bin, encodeLocation,weekday])
        count += 1


# print(resultlist)

df_x = pd.DataFrame(resultlist)
df_x.rename({0:'bin', 1:'encoded_location', 2:'encoded_day_of_week'}, inplace=True, axis=1)
x = df_x.drop('encoded_location', axis=1)
y = df_x['encoded_location']
clf = RandomForestClassifier(max_depth=15, random_state=6969)
clf.fit(x.values, y)
# print(clf.predict([[6,2]]))
# print(clf.predict([[147,2]]))
# print(clf.predict([[49,2]]))
# print(clf.predict([[120,2]]))
# print(int(clf.predict([[60,3]])))

#model training ends

startCSV()

ser = serial.Serial('COM4', 115200)

firstTrigger = False
secondTrigger = False

def returnPerson():
    data = pd.read_csv("ownerVisitor.csv")
    personCount =int(data["personCount"].tail(1))
    elderly = data["elderly"].tail(1).bool()
    return elderly, personCount

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
    data = pd.read_csv("elderlyHabits.csv")
    location =data["location"].tail(1).item()
    return location

def elderlyHabitUpdate(location):

    data = pd.read_csv("elderlyHabits.csv")
    year =int(data["year"].tail(1))
    month =int(data["month"].tail(1))
    day =int(data["day"].tail(1))
    hour =int(data["hour"].tail(1))
    minute =int(data["minute"].tail(1))
    second =int(data["second"].tail(1))

    startTime = datetime.datetime(year, month, day, hour, minute, second)
    durationDelta = datetime.datetime.now() - startTime
    durationDeltaSeconds = durationDelta.total_seconds()
    duration = durationDeltaSeconds/(60*60)

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
        'location' : location
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

checkInterval = datetime.timedelta(minutes=10)
timePreviousCheck = datetime.datetime.now()
next_time = timePreviousCheck + checkInterval

lastMove = datetime.datetime.now()


alertedCount = 0
abnormalTriggerTime = 30
noMoveTriggerTime = 30

elderlyHome = True


print('program start')
while True:
    try:
        ser_bytes = ser.read()
        now = datetime.datetime.now()
        if next_time <= now:
            timePreviousCheck = now
            tempTime = getTimeDict()
            tempbin = tempTime["hour"]*6 + tempTime["minute"]//10
            tempbin = tempTime["hour"]*6 + tempTime["minute"]//10
            predictedLocation = IDLocationDict[int(clf.predict([[tempbin,tempTime["weekday"]]]))]
            currentLocation = returnLocation()
            if currentLocation != predictedLocation:
                alertedCount += 1
                if alertedCount >= (abnormalTriggerTime/10):
                    send_alert_abnormal(predictedLocation, currentLocation, abnormalTriggerTime)
            else:
                alertedCount = 0

            minutePassed = (now - lastMove).total_seconds()/60
            if elderlyHome:
                if minutePassed >= noMoveTriggerTime:
                    send_alert_not_moving(currentLocation, noMoveTriggerTime)

        if ser_bytes == b'e':
            print('Close')
            ser.close()
            break

        elif ser_bytes == b't':
            elderly, personCount = returnPerson()
            lastMove = datetime.datetime.now()
            if elderly and personCount == 0:
                updateLastMovement('toilet')
                if returnLocation != 'toilet':
                    elderlyHabitUpdate('toilet')

        elif ser_bytes == b'b':
            # personList = returnPerson()
            elderly, personCount = returnPerson()
            lastMove = datetime.datetime.now()
            if elderly and personCount == 0:
                updateLastMovement('bedroom')
                if returnLocation != 'bedroom':
                    elderlyHabitUpdate('bedroom')

        elif ser_bytes == b'k':
            elderly, personCount = returnPerson()
            lastMove = datetime.datetime.now()
            if elderly and personCount == 0:
                updateLastMovement('kitchen')
                if returnLocation != 'kitchen':
                    elderlyHabitUpdate('kitchen')

        elif ser_bytes == b'l':
            elderly, personCount = returnPerson()
            lastMove = datetime.datetime.now()
            if elderly and personCount == 0:
                updateLastMovement('living room')
                if returnLocation != 'living room':
                    elderlyHabitUpdate('living room')

        elif ser_bytes == b'f':
            firstTrigger = True
            if secondTrigger:
                print('leave')
                firstTrigger = False
                secondTrigger = False
                elderly,stranger = returnPerson()
                if stranger > 0:
                    strangerLeave()
                    send_alert_strangerleave()
                else:
                    elderlyLeave()
                    elderlyHabitUpdate('outside')
                    send_alert_elderleave()
                    elderlyHome = False

        elif ser_bytes == b's':
            secondTrigger = True
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
                    elderlyEnter = True
                elif person == 'stranger':
                    strangerEnter()

        if ser_bytes != b'':
            print(ser_bytes) 

    except Exception as e:
        ser.close()
        print(e)
        print("Program stopped")
        break
