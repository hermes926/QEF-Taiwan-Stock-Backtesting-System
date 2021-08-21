import pandas as pd
import os.path
import csv

series = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
header = [['date', 'identifier']]

cnt = 0
for index in series:
    time = index.strftime("%Y%m%d")
    if os.path.isfile("./ProcessedData\\" + time + ".csv"):    
        time_data = pd.read_csv("./ProcessedData\\" + time + ".csv")
        rand = time_data.sample()
        iden = rand.values[0][0]
        date = rand.values[0][1]
        header.append([date, iden])

file = csv.writer(open('./Strategies/s_1.csv', 'w', newline=''), delimiter=',')
file.writerows(header)


        


