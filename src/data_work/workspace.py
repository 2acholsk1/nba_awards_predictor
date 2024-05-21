import pandas as pd
# from src.data_work.prepare_data import import_raw_data
# from src.data_work.prepare_data import droping_unnecessary_data

year = 2020
data = pd.read_csv("data/all_nba_data/rs_"+str(year-1)+"_"+str(year)+"_full.csv")
results = pd.read_csv("data/results/all_nba_results.csv")
        
year_col = str(year-1)+"_"+str(year)
target_index = results[(results["Season"] == year_col) & (results["Tm"] == "1st")].index

print(results.loc[target_index])
print(results.loc[target_index, "Unnamed: 6"])

player = "LeBron James"

print((results.loc[target_index, ["Unnamed: 6", "Unnamed: 7"]] == player))

# if results.loc(results[target_index].any() == player):
#     player_index = data[(data["Player"] == player)].index
#     print(data[player_index])"Unnamed: 6"