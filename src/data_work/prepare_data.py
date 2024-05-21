#!/usr/bin/env python3
"""Script used for work on data

Returns:
    bool: 1 if any error, 0 if everrything okay
"""
import pandas as pd
import numpy as np

from src.config_func import load_config


def import_raw_data(year:int=2024) -> np.array:
    """Function to import data from Basketball Reference and connect regular data with advanced

    Args:
        year (int, optional): Year of when regular season ends. Defaults to 2024.

    Returns:
        np.array: Connected regular and advanced data in specific season
    """
        
    down_value_str = str(year-1)
    up_value_str = str(year)

    importing_string = "data/raw_data/rs_"+down_value_str+"_"+up_value_str+".csv"
    importing_string_advance = "data/raw_data/rs_"+down_value_str+"_"+up_value_str+"_advanced.csv"

    data = pd.read_csv(importing_string)
    data_advance = pd.read_csv(importing_string_advance)
    result = pd.concat([data, data_advance], axis='columns')   

    return result.loc[:, ~result.columns.duplicated()]


def droping_cols(data:pd.DataFrame, list_of_cols:list) -> pd.DataFrame:
    """Droping data from given DataFrame

    Args:
        data (pd.DataFrame): Your DataFrame
        list_of_cols (np.array): Columns to erease, given as elements in list

    Returns:
        pd.DataFrame: Data after erease specific columns
    """
    return data.drop(columns=list_of_cols)


def droping_rows(data:pd.DataFrame, index_lst:list) -> pd.DataFrame:
    """Droping rows from given DataFrame

    Args:
        data (pd.DataFrame): Your DataFrame
        index_lst (list): Index of rows to erease, given as elements in list

    Returns:
        pd.DataFrame: Data after erease specific rows
    """
    return data.drop(index=index_lst)


def rookie_list_creator(data:pd.DataFrame, year:int) -> pd.DataFrame:
    """Function for creating rookie list from connected regular and advanced data,
        based on read data about drafted player in specific year.

    Args:
        data (pd.DataFrame): Regulard + advanced data frame
        year (int): Year of end season

    Returns:
        pd.DataFrame: Dataframe of rookie players for specific year
    """

    draft_path = "data/rookie_data_raw/draft_"+str(year-1)+".csv"
    rookie_data_check = pd.read_csv(draft_path)
    rookie_data_check = rookie_data_check.pop("Player")

    is_rookie = data["Player"].isin(rookie_data_check)
    return data[is_rookie]

    

def main():
    """Working on data: importing from raw files, eareasing NaN columns, eareasing not neccesary data
    """

    config = load_config("configs/data_config.yaml")

    start_year = config.get("start_year")
    end_year = config.get("end_year")
    drop_cols = config.get("drop_cols")

    while end_year > start_year:
        data = import_raw_data(end_year)
        data = droping_cols(data, ["Unnamed: 19",
                                   "Unnamed: 24",
                                   "Player-additional"])
        data = droping_cols(data, drop_cols)

        data_rookie = rookie_list_creator(data, end_year)
        data_rookie.to_csv("data/rookie_data/rookie_"+str(end_year-1)+"_"+str(end_year)+".csv", index=False)

        if end_year == 2024:
            games_less_82 = data.loc[data["G"] < 65].index
            data_all_nba = droping_rows(data, games_less_82)
        else:
            data_all_nba = data

        data_all_nba.to_csv("data/all_nba_data/rs_"+str(end_year-1)+"_"+str(end_year)+"_full.csv", index=False)
        end_year -= 1

if __name__ == '__main__':
    main()
