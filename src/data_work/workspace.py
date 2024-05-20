import pandas as pd
# from src.data_work.prepare_data import import_raw_data
# from src.data_work.prepare_data import droping_unnecessary_data

draft_path = "data/rookie_data_raw/draft_"+str(2022)+".csv"
rs_path = "data/raw_data/rs_2022_2023.csv"
rookie_data = pd.read_csv(draft_path)
data = pd.read_csv(rs_path)
# rookie_data = rookie_data.pop("Player")
rookie_data = rookie_data.pop("Player")

is_rookie = data["Player"].isin(rookie_data)

data = data[is_rookie]



print(data)