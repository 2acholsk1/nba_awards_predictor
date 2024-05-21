#!/usr/bin/env python3
import pandas as pd
from src.config_func import load_config
import numpy as np

def is_all_nba(data:pd.DataFrame, results:pd.DataFrame, year, player):

    year_col = str(year-1)+"_"+str(year)
    target_index = results[(results["Season"] == year_col) & (results["Tm"] == "1st")].index

    if (results.loc[target_index] == player).any():
        player_index = data[(data["Player"] == player)].index
        data[player_index] 


def main():

    config = load_config("configs/data_config.yaml")

    start_year = config.get("start_year")
    end_year = config.get("end_year")

    while end_year > start_year:
        data_all_nba = pd.read_csv("data/all_nba_data/rs_"+str(end_year-1)+"_"+str(end_year)+"_full.csv")
        data_all_nba_results = pd.read_csv("data/results/all_nba_results.csv")
        data_rookie = pd.read_csv("data/rookie_data/rookie_"+str(end_year-1)+"_"+str(end_year)+".csv")
        data_rookie_results = pd.read_csv("data/results/rookie_results.csv")
        
        data_all_nba['all_nba'] = np.zeros(len(data_all_nba))
        data_rookie['all_rookie'] = np.zeros(len(data_rookie))

        is_all_nba(data_all_nba_results, end_year, "1st")

        data_all_nba.to_csv("data/final_data/all_nba_final_"+str(end_year-1)+"_"+str(end_year)+".csv")
        data_rookie.to_csv("data/final_data/rookie_final_"+str(end_year-1)+"_"+str(end_year)+".csv")

        end_year -= 1




if __name__ == '__main__':
    main()
