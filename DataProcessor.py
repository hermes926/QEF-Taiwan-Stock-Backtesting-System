import csv
import pandas as pd

rawdata = pd.read_csv('../pricevol.csv')

print(rawdata["id"])

