import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import datetime
start_time = [datetime.datetime(2022, 3, 6, 22, 0, 0), datetime.datetime(2022, 3, 7, 6, 0, 0), datetime.datetime(2022, 3, 7, 6, 10, 0), datetime.datetime(2022, 3, 7, 6, 30, 0), datetime.datetime(2022, 3, 7, 12, 30, 0), datetime.datetime(2022, 3, 7, 15, 30, 0), datetime.datetime(2022, 3, 7, 19, 30, 0), datetime.datetime(2022, 3, 7, 21, 30, 0), datetime.datetime(2022, 3, 7, 21, 40, 0), datetime.datetime(2022, 3, 7, 22, 0, 0), datetime.datetime(2022, 3, 7, 22, 1, 0)]
location = ['bedroom', 'living room', 'bathroom', 'living room', 'bedroom', 'living room', 'outside', 'living room', 'bathroom', 'living room', 'bedroom']
encoded_location = [1, 2, 3, 2, 1, 2, 0, 2, 3, 2, 1]
duration = [8, 1/60*10, 1/60*20, 6, 3, 4, 2, 1/60*10, 1/60*20, 1/60, 8]
day_of_week = ['Sunday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday','Monday','Monday', 'Monday', 'Monday']
encoded_day_of_week = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

resultlist= list()

for i in range(len(start_time)):
    encodeLocation = encoded_location[i]
    timing = str(start_time[i].time())
    hour, minute, seconds = timing.split(":")
    basebin = int(hour)*6 + int(minute)//10 
    multiple = int(duration[i]*6//1)
    dayweek = encoded_day_of_week[i]
    for i in range(multiple):
        resultlist.append([basebin, encodeLocation,dayweek])
        basebin+=1
        if basebin == 144:
            dayweek += 1
            dayweek = dayweek % 7

        basebin = basebin % 144

df_x = pd.DataFrame(resultlist)
df_x.rename({0:'bin', 1:'encoded_location', 2:'encoded_day_of_week'}, inplace=True, axis=1)
x = df_x.drop('encoded_location', axis=1)
y = df_x['encoded_location']
clf = RandomForestClassifier(max_depth=15, random_state=4378)
clf.fit(x, y)
print(clf.predict([[6,1]]))
print(clf.predict([[147,1]]))
print(clf.predict([[49,1]]))
print(clf.predict([[120,1]]))