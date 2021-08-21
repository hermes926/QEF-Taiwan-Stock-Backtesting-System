import pandas as pd

rawdata = pd.read_csv('../pricevol.csv')
rawdata = rawdata[["identifier", "date_", "open_","close_"]]
rawdata["date_"] = pd.to_datetime(rawdata["date_"])

series = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')

for index in series:
    nowdata = rawdata.loc[rawdata["date_"] == index]
    if not nowdata.empty:   
        time = index.strftime("%Y%m%d")
        nowdata.to_csv("C:\MyFile_new\Others\QEF\QEF-project\ProcessedData\\" + time + ".csv", index=False)
