import pandas as pd
import numpy as np

rawdata = pd.read_csv('../pricevol.csv')
rawdata = rawdata[["identifier", "date_", "adj_close_","close_", "volume_"]]
ids = pd.unique(rawdata["identifier"])

newdata = pd.DataFrame()
for index in ids:
    print(index)
    nowdata = rawdata.loc[rawdata["identifier"] == index]
    # for i in range(0,nowdata.shape[0]-4):
    nowdata['MA_5'] = nowdata.iloc[:,2].rolling(window=5).mean()
    nowdata['MA_20'] = nowdata.iloc[:,2].rolling(window=20).mean()
    if newdata.empty:   
        newdata = nowdata
    else:
        newdata = pd.concat([newdata, nowdata])



newdata["date_"] = pd.to_datetime(newdata["date_"])

series = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')

for index in series:
    nowdata = newdata.loc[newdata["date_"] == index]
    print(index)
    if not nowdata.empty:   
        # print(nowdata)
        # break
        time = index.strftime("%Y%m%d")
        nowdata.to_csv(".\ProcessedData\\" + time + ".csv", index=False)
