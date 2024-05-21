#!/usr/bin/env python3
import pandas as pd
from src.config_func import load_config
import numpy as np

def is_all_nba(data:pd.DataFrame, results:pd.DataFrame, year, players) -> None:
    """Function to check that player were in all nba team

    Args:
        data (pd.DataFrame): Data of players
        results (pd.DataFrame): Results of all NBA teams
        year (_type_): Upper year of season
        players (_type_): List of players
    """

    year_col = str(year-1)+"_"+str(year)
    target_index_1st = results[(results["Season"] == year_col) & (results["Tm"] == "1st")].index
    target_index_2nd = results[(results["Season"] == year_col) & (results["Tm"] == "2nd")].index
    target_index_3rd = results[(results["Season"] == year_col) & (results["Tm"] == "3rd")].index
    for player in players:
        for i in range(5):
            if player in results.loc[target_index_1st, ["Unnamed: "+str(i+4)]].values:
                data.loc[data["Player"] == player, "all_nba"] = 1.0
            if player in results.loc[target_index_2nd, ["Unnamed: "+str(i+4)]].values:
                data.loc[data["Player"] == player, "all_nba"] = 2.0
            if player in results.loc[target_index_3rd, ["Unnamed: "+str(i+4)]].values:
                data.loc[data["Player"] == player, "all_nba"] = 3.0
    

def is_all_rookie(data:pd.DataFrame, results:pd.DataFrame, year, players) -> None:
    """Function to check that player were in rookie all nba team

    Args:
        data (pd.DataFrame): Data of players
        results (pd.DataFrame): Results of all NBA teams
        year (_type_): Upper year of season
        players (_type_): List of players
    """

    year_col = str(year-1)+"_"+str(year)
    target_index_1st = results[(results["Season"] == year_col) & (results["Tm"] == "1st")].index
    target_index_2nd = results[(results["Season"] == year_col) & (results["Tm"] == "2nd")].index
    for player in players:
        for i in range(5):
            if player in results.loc[target_index_1st, ["Unnamed: "+str(i+3)]].values:
                data.loc[data["Player"] == player, "all_rookie"] = 1.0
            if player in results.loc[target_index_2nd, ["Unnamed: "+str(i+3)]].values:
                data.loc[data["Player"] == player, "all_rookie"] = 2.0


def main():
    """Main function of linking data
    """

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

        is_all_nba(data_all_nba, data_all_nba_results, end_year, data_all_nba["Player"])
        is_all_rookie(data_rookie, data_rookie_results, end_year, data_rookie["Player"])

        data_all_nba.to_csv("data/final_data/all_nba_final_"+str(end_year-1)+"_"+str(end_year)+".csv", index=False)
        data_rookie.to_csv("data/final_data/rookie_final_"+str(end_year-1)+"_"+str(end_year)+".csv", index=False)

        end_year -= 1




if __name__ == '__main__':
    main()
