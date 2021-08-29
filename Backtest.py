
import pandas as pd
from pandas.core import series
import matplotlib.pyplot as plt

print("Enter the strategy file name")
filename = input()

strategy = pd.read_csv('./Strategies/' + filename)
strategy['date'] = pd.to_datetime(strategy['date'])

init = 100000
earning = [[]]


for index, row in strategy.iterrows():
    earning.append([row['date'], init])
    datename = row['date'].strftime("%Y%m%d")
    datedata = pd.read_csv('./ProcessedData/' + datename + '.csv')
    foundrow = datedata.loc[datedata['identifier'] == row['identifier']]
    if not foundrow.empty:
        init /= foundrow['open_'].values[0]
        init *= foundrow['close_'].values[0]

series = pd.DataFrame(earning, columns =['date', 'earning'])
series['date'] = pd.to_datetime(series['date'])
plt.plot(series['date'], series['earning'])
plt.xlabel('Date')
plt.ylabel('Money')
plt.title('Random Buying Stock earning')
plt.legend(['Earning'])

plt.savefig('./Result/plot_'+ filename + '.jpg', dpi=300, bbox_inches='tight')

