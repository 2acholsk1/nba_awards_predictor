import pandas as pd

data = pd.read_csv("data/raw_data/rs_2005_2006_advanced.csv")
data1 = pd.read_csv("data/raw_data/rs_2005_2006.csv")
# data1 = data1.drop(["Rk", "Player", "Pos", "Age", "Tm", "G", "MP", "Player-additional"], axis='columns')

result = pd.concat([data, data1], axis='columns')
# result = result.loc[:, ~result.columns.duplicated()]
result = result.loc[:, ~result.columns.duplicated()]
# print(data.head())
# print(data1.head())
# print(result.head())
print(data.columns)
print(data1.columns)
print(result.columns)