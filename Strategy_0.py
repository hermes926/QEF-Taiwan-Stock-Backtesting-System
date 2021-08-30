import pandas as pd
import os.path
from pandas.core import series
import matplotlib.pyplot as plt

series = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
asset = [ [2000, "-1", 0] for i in range(50)]
rawdata = pd.read_csv('../mapping.csv')
rawdata = rawdata["ticker"].array[127:1085]
mapped = { i: 0 for i in rawdata}
# read in data

cnt = 0
earning = [[]]
# earning_single = [[]] * 10
last = pd.DataFrame()

for index in series:
    print(index)
    time = index.strftime("%Y%m%d")
    if last.empty:
        if os.path.isfile("./ProcessedData\\" + time + ".csv"):    
            last = pd.read_csv("./ProcessedData\\" + time + ".csv")
    # initialize
    
    elif os.path.isfile("./ProcessedData\\" + time + ".csv"):    
 
        sum = 0
        for i in range(50):
            sum += asset[i][0]
        earning.append([index, sum])
        # update for the plot

        time_data = pd.read_csv("./ProcessedData\\" + time + ".csv")
        for i in range(50):
            if asset[i][1] == "-1":
                for j in rawdata:
                    today = time_data.loc[time_data['identifier'] == j]
                    yest = last.loc[last['identifier'] == j]
                    if mapped[j] == 0 and not today.empty and not yest.empty and today['MA_5'].values[0] > today['MA_20'].values[0] and yest['MA_20'].values[0] > yest['MA_5'].values[0]:
                        mapped[j] = 1
                        asset[i][1] = j
                        asset[i][2] = asset[i][0] / today['open_'].values[0]
                        break 
            # No holding
            
            else:
                today = time_data.loc[time_data['identifier'] == asset[i][1]]
                if not today.empty:
                    asset[i][0] = asset[i][2] * today['open_'].values[0]    

                yest = last.loc[last['identifier'] == asset[i][1]]
                if not today.empty and not yest.empty and today['MA_5'].values[0] < today['MA_20'].values[0] and yest['MA_20'].values[0] < yest['MA_5'].values[0]:
                    mapped[asset[i][1]] = 0
                    asset[i][1] = "-1"
                    asset[i][2] = 0
            # Holding 
        
        last = time_data

# print(earning)
series = pd.DataFrame(earning, columns =['date', 'earning'])
series['date'] = pd.to_datetime(series['date'])
plt.plot(series['date'], series['earning'])
plt.xlabel('Date')
plt.ylabel('Money')
plt.title('MA 5, 20 cross, 50 portion, stock earning')
plt.legend(['Earning'])

plt.savefig('./Result/plot_new1.jpg', dpi=300, bbox_inches='tight')



        


