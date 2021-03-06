import pandas as pd
import os.path
from pandas.core import series
import matplotlib.pyplot as plt

series = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
asset = [ [2000, "-1", 0] for i in range(50)]
neg_asset = [ [-2000, "-1", 0] for i in range(50)]


rawdata = pd.read_csv('../mapping.csv')
rawdata = rawdata["ticker"].array[130:1085]
# Select more static stocks
mapped = { i: 0 for i in rawdata}
# read in data

cnt = 0
earning = [[]]
last = pd.DataFrame()
vol_threshold = 250000.
transaction_cost = .999
turnover = 0

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
            sum += neg_asset[i][0]
        earning.append([index, sum])
        # update for the plot

        time_data = pd.read_csv("./ProcessedData\\" + time + ".csv")
        time_data = time_data.loc[time_data.volume_ > vol_threshold]
        for i in range(50):
            if asset[i][1] == "-1":
                for j in rawdata:
                    today = time_data.loc[time_data['identifier'] == j]
                    yest = last.loc[last['identifier'] == j]
                    if mapped[j] == 0 and not today.empty and not yest.empty and today['MA_5'].values[0] > today['MA_20'].values[0] and yest['MA_20'].values[0] > yest['MA_5'].values[0]:
                        mapped[j] = 1
                        asset[i][1] = j
                        asset[i][0] *= transaction_cost
                        asset[i][2] = asset[i][0] / today['adj_close_'].values[0]
                        turnover += 1
                        break 
            # Long and No holding
            
            else:
                today = time_data.loc[time_data['identifier'] == asset[i][1]]
                if not today.empty:
                    asset[i][0] = asset[i][2] * today['adj_close_'].values[0] * transaction_cost   

                yest = last.loc[last['identifier'] == asset[i][1]]
                if not today.empty and not yest.empty and today['MA_5'].values[0] < today['MA_20'].values[0] and yest['MA_20'].values[0] < yest['MA_5'].values[0]:
                    mapped[asset[i][1]] = 0
                    asset[i][1] = "-1"
                    asset[i][2] = 0
                    turnover += 1
            # Long Holding 
        
            if neg_asset[i][1] == "-1":
                for j in rawdata:
                    today = time_data.loc[time_data['identifier'] == j]
                    yest = last.loc[last['identifier'] == j]
                    if mapped[j] == 0 and not today.empty and not yest.empty and today['MA_5'].values[0] < today['MA_20'].values[0] and yest['MA_20'].values[0] < yest['MA_5'].values[0]:
                        mapped[j] = 1
                        neg_asset[i][1] = j
                        neg_asset[i][0] *= transaction_cost
                        neg_asset[i][2] = neg_asset[i][0] / today['adj_close_'].values[0]
                        turnover += 1
                        break 
            # Short and no holding
            
            else:
                today = time_data.loc[time_data['identifier'] == neg_asset[i][1]]
                if not today.empty:
                    neg_asset[i][0] = neg_asset[i][2] * today['adj_close_'].values[0] * transaction_cost 

                yest = last.loc[last['identifier'] == neg_asset[i][1]]
                if not today.empty and not yest.empty and today['MA_5'].values[0] > today['MA_20'].values[0] and yest['MA_20'].values[0] > yest['MA_5'].values[0]:
                    mapped[neg_asset[i][1]] = 0
                    neg_asset[i][1] = "-1"
                    neg_asset[i][2] = 0
                    turnover += 1
            # Short and Holding 
        


        last = time_data

series = pd.DataFrame(earning, columns =['date', 'earning'])
series['date'] = pd.to_datetime(series['date'])
plt.plot(series['date'], series['earning'])
plt.xlabel('Date')
plt.ylabel('Money')
plt.title('MA 5, 20 cross, 50 portion, stock earning')
plt.legend(['Earning'])

plt.savefig('./Result/plot_tc_01.jpg', dpi=300, bbox_inches='tight')
print(turnover)


        


