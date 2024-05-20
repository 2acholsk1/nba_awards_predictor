#!/usr/bin/env python3
"""Script for formating data of results from Basketball Reference
"""

import pandas as pd
from src.config_func import load_config

def main():
    """Main function of formating results CSV file
    """

    config = load_config("configs/data_config.yaml")

    start_year = config.get("start_year")
    end_year = config.get("end_year")

    data_all_nba = pd.read_csv("data/results/all_nba_results_raw.csv")
    data_rookie = pd.read_csv("data/results/rookie_results_raw.csv")

    data_all_nba = data_all_nba.drop(columns=["Lg", "Voting"])
    data_rookie = data_rookie.drop(columns=["Lg"])

    for i in range(5):
        data_all_nba.iloc[:, -(i+1)] = data_all_nba.iloc[:, -(i+1)].str[:-2]
        data_rookie.iloc[:, -(i+1)] = data_rookie.iloc[:, -(i+1)]

    while end_year > start_year:
        season_rename = str(end_year-1)+"_"+str(end_year)
        data_all_nba.loc[data_all_nba["Season"] == str(end_year-1)+"-"+str(end_year)[2:], "Season"] = season_rename
        data_rookie.loc[data_rookie["Season"] == str(end_year-1)+"-"+str(end_year)[2:], "Season"] = season_rename

        end_year -= 1

    data_all_nba.to_csv("data/results/all_nba_results.csv")
    data_rookie.to_csv("data/results/rookie_results.csv")

if __name__ == '__main__':
    main()