import datetime
start_time = [datetime.datetime(2022, 3, 6, 22, 0, 0), datetime.datetime(2022, 3, 7, 6, 0, 0), datetime.datetime(2022, 3, 7, 6, 12, 0), datetime.datetime(2022, 3, 7, 6, 30, 0), datetime.datetime(2022, 3, 7, 12, 30, 0), datetime.datetime(2022, 3, 7, 15, 30, 0), datetime.datetime(2022, 3, 7, 19, 30, 0), datetime.datetime(2022, 3, 7, 21, 30, 0), datetime.datetime(2022, 3, 7, 21, 40, 0), datetime.datetime(2022, 3, 7, 22, 0, 0), datetime.datetime(2022, 3, 7, 22, 1, 0)]
location = ['bedroom', 'living room', 'bathroom', 'living room', 'bedroom', 'living room', 'outside', 'living room', 'bathroom', 'living room', 'bedroom']
encoded_location = [1, 2, 3, 2, 1, 2, 0, 2, 3, 2, 1]
duration = [8, 1/60*10, 1/60*20, 6, 3, 4, 2, 1/60*10, 1/60*20, 1/60, 8]
day_of_week = ['Sunday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday', 'Monday','Monday','Monday', 'Monday', 'Monday']
encoded_day_of_week = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# X = []
# for i in range(len(start_time)):
#     X.append([start_time[i], encoded_location[i], duration[i], encoded_day_of_week[i]])
# df_x = pd.DataFrame(X)
# df_x.rename({0:'start_time', 1:'encoded_location', 2:'duration', 3:'encoded_day_of_week'}, inplace=True, axis=1)

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

print(resultlist)
print(len(resultlist))
