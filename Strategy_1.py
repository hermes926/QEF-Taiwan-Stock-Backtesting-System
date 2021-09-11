import pandas as pd
import os.path
from pandas.core import series
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import statistics

series = pd.date_range(start='2020-01-09', end='2020-12-31', freq='D')


rawdata = pd.read_csv('../mapping.csv')
rawdata = rawdata["ticker"].array[130:1085]
# Select more static stocks
mapped = { i: -1 for i in rawdata}
my_asset_long = [[-1] for i in range(10)]
my_asset_short = [[-1] for i in range(10)]
my_asset_sum = 1
# read in data

cnt = 0
earning = [[]]
turnover_plot = [[]]
last = pd.DataFrame()
vol_threshold = 1000000
transaction_cost = .999
turnover = 0

for index in series:
    print(index)
    time = index.strftime("%Y%m%d")
    if last.empty:
        if os.path.isfile("./ProcessedData\\" + time + ".csv"):    
            last = pd.read_csv("./ProcessedData\\" + time + ".csv")
    
    elif os.path.isfile("./ProcessedData\\" + time + ".csv"):     
        
        time_data = pd.read_csv('./ProcessedData\\' + time + ".csv")
        time_data = time_data.loc[time_data.volume_ * time_data.adj_close_ > vol_threshold]
        
        
        if my_asset_long[0][0] != -1:
            sum = 0
            for i in range(10):
                t = time_data.loc[time_data['identifier'] == my_asset_long[i][0]]
                y = last.loc[last['identifier'] == my_asset_long[i][0]]
                if not t.empty and not y.empty:
                    sum +=  (10 - i) / 110 *  my_asset_sum * t['adj_close_'].values[0] / y['adj_close_'].values[0]
                else:
                    sum +=  (10 - i) / 110 * my_asset_sum
            
            for i in range(10):
                t = time_data.loc[time_data['identifier'] == my_asset_short[i][0]]
                y = last.loc[last['identifier'] == my_asset_short[i][0]]
                if not t.empty and not y.empty:
                    sum +=  (i + 1) / 110 *  my_asset_sum * y['adj_close_'].values[0] / t['adj_close_'].values[0]
                else:
                    sum +=  (i + 1) / 110 * my_asset_sum
            my_asset_sum = sum 
            # print(my_asset_sum, my_asset_long, my_asset_short) 
            earning.append([index, sum])
        
        
        
        
        
        cntt = 0
        past = index
        while cntt != 5:
            past -= timedelta(days=1)
            pasttime = past.strftime("%Y%m%d")
            if os.path.isfile('./ProcessedData\\' + pasttime + ".csv"):
                cntt += 1
        
        pasttime = past.strftime("%Y%m%d")
        last_data = pd.read_csv('./ProcessedData\\' + pasttime + ".csv")
        last_data = last_data.loc[last_data.volume_ * last_data.adj_close_ > vol_threshold]


        for i in rawdata:
            today = time_data.loc[time_data['identifier'] == i]
            yest = last_data.loc[last_data['identifier'] == i]
            if not today.empty and not yest.empty:
                mapped[i] = today['adj_close_'].values[0] / yest['adj_close_'].values[0]
            else: 
                mapped[i] = -1
        
        mapped = {k: v for k, v in sorted(mapped.items(), key=lambda item: item[1])}

        map_list = list(mapped.items())
        while map_list[0][1] == -1:
            map_list.pop(0)

        temp_long = map_list[:10]
        temp_short = map_list[-10:]
        now_th = 0
        for j in range(10):
            single_thres = j
            for k in range(10):
                if temp_long[j][0] == my_asset_long[k][0]:
                    single_thres = abs(j - k) 
                    break
            now_th += single_thres

        for j in range(10):
            single_thres = j
            for k in range(10):
                if temp_short[j][0] == my_asset_short[k][0]:
                    single_thres = abs(j - k) 
                    break
            now_th += single_thres
        
        turnover_plot.append([index, now_th / 110])


        my_asset_long = map_list[:10] 
        my_asset_short = map_list[-10:]
        last = time_data

sharpe = earning[-1][1] / statistics.stdev(earning[:][1])

series = pd.DataFrame(earning, columns =['date', 'earning'])
series['date'] = pd.to_datetime(series['date'])
plt.plot(series['date'], series['earning'])
plt.xlabel('Date')
plt.ylabel('Money')
plt.title('Mean reversal, stock earning')
plt.legend(['Earning'])

plt.savefig('./Result/plot_mr_01.jpg', dpi=300, bbox_inches='tight')


series_t = pd.DataFrame(turnover_plot, columns =['date', 'turnover'])
series_t['date'] = pd.to_datetime(series_t['date'])
plt.plot(series_t['date'], series_t['turnover'])
plt.xlabel('Date')
plt.ylabel('Turnover')
plt.title('Mean reversal, Turnover')
plt.legend(['Turnover'])

plt.savefig('./Result/plot_mr_turnover_01.jpg', dpi=300, bbox_inches='tight')
print(sharpe)


        


