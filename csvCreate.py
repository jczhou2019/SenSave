import serial
import csv
from currentTime import getTimeDict
import pandas as pd
import datetime

def startCSV():
    file0 = open('lastMovement.csv', 'a+')

    file1 = open('elderlyHabits.csv', 'a+')

    file2 = open('ownerVisitor.csv', 'a+')

    try:  
        df = pd.read_csv('lastMovement.csv')
    except pd.errors.EmptyDataError:
        df0 = pd.DataFrame({
            'year' : 0,
            'month' : 0,
            'day' : 0,
            'hour' : 0,
            'minute' : 0,
            'second' : 0,
            'location': ['living room']
            })
        df0.to_csv('lastMovement.csv', mode='a', index=False, header=True)

    try:  
        df = pd.read_csv('elderlyHabits.csv')
    except pd.errors.EmptyDataError:
        df1 = pd.DataFrame({
            'year' : 0,
            'month' : 0,
            'day' : 0,
            'hour' : 0,
            'minute' : 0,
            'second' : 0,
            'weekday' : 0,
            'duration': [1],
            'location' : ['living room']
            })
        df1.to_csv('elderlyHabits.csv', mode='a', index=False, header=True)

    try:  
        df = pd.read_csv('ownerVisitor.csv')
    except pd.errors.EmptyDataError:
        df2 = pd.DataFrame({
            'year' : 0,
            'month' : 0,
            'day' : 0,
            'hour' : 0,
            'minute' : 0,
            'second' : 0,
            'personCount': [1],
            'elderly' : [True]
            })
        df2.to_csv('ownerVisitor.csv', mode='a', index=False, header=True)



# file0 = open('lastMovement.csv', 'a+')

# file1 = open('elderlyHabits.csv', 'a+')

# file2 = open('ownerVisitor.csv', 'a+')

# try:  
#     df = pd.read_csv('ownerVisitor.csv')
# except pd.errors.EmptyDataError:
#     # with open('ownerVisitor.csv', 'w') as file:
#     #     csvwriter = csv.writer(file)
#     #     csvwriter.writerow(['year',
#     #     'month',
#     #     'day',
#     #     'hour',
#     #     'minute',
#     #     'second',
#     #     'personCount',
#     #     'elderly'])
#     dfa = pd.DataFrame({
#         'year' : 0,
#         'month' : 0,
#         'day' : 0,
#         'hour' : 0,
#         'minute' : 0,
#         'second' : 0,
#         'personCount': [1],
#         'elderly' : [True]
#         })
#     dfa.to_csv('ownerVisitor.csv', mode='a', index=False, header=True)
# else:
#     print(df.head())


    # datadict = getTimeDict()
    # data = pd.read_csv("ownerVisitor.csv")
    # personCount = data["personCount"].tail(1)
    # elderly = data["elderly"].tail(1)

    # df = pd.DataFrame(datadict)
    # df.to_csv('ownerVisitor.csv', mode='a', index=False, header=False)



# startCSV()

# location = 'duelzone'

# data = pd.read_csv("elderlyHabits.csv")
# year =int(data["year"].tail(1))
# month =int(data["month"].tail(1))
# day =int(data["day"].tail(1))
# hour =int(data["hour"].tail(1))
# minute =int(data["minute"].tail(1))

# startTime = datetime.datetime(year, month, day, hour, minute, 0)
# durationDelta = datetime.datetime.now() - startTime
# durationDeltaSeconds = durationDelta.total_seconds()
# duration = durationDeltaSeconds/(60*60)

# data.loc[data.index[-1] ,['location']] = location
# data.loc[data.index[-1], ['duration']] = duration
# data.to_csv('elderlyHabits.csv', index=False, header=True)

# timeDict = getTimeDict()
# df = pd.DataFrame({
#     'year' : [timeDict['year']],
#     'month' : [timeDict['month']],
#     'day' : [timeDict['day']],
#     'hour' : [timeDict['hour']],
#     'minute' : [timeDict['minute']],
#     'second' : [timeDict['second']],
#     'weekday' : [timeDict['weekday']],
#     'location' : None
#     })
# df.to_csv('elderlyHabits.csv', mode='a', index=False, header=False)