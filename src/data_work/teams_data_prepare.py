#!/usr/bin/env python3
"""Script to prepare features and team data

Returns:
    _type_: None
"""

import pandas as pd

from src.config_func import load_config


def team_data_droping(data:pd.DataFrame) -> pd.DataFrame:
    """Keeping only data about team and their overall result

    Args:
        data (pd.DataFrame): Statistics of team

    Returns:
        pd.DataFrame: Data only with Rank, Team and their overall score
    """

    return data[['Rk', 'Team', 'Overall']]


def team_result_feature(data_teams:pd.DataFrame) -> None:

    def calculate_balance(row):
        parts = row.split('-')
        wins, loses = parts
        return float(wins) / (float(wins) + float(loses))
    
    data_teams['Balance'] = data_teams['Overall'].apply(calculate_balance)


def replace_team_names(data_teams: pd.DataFrame, team_mapping: dict) -> pd.DataFrame:
    """Function to replace full  team names to shortcuts

    Args:
        data (pd.DataFrame): Data to replace
        team_mapping (dict): Mapping of shortcuts

    Returns:
        pd.DataFrame: Data with replaced Team Names to shortcuts
    """
    data_teams['Team'] = data_teams['Team'].map(team_mapping)
    data_teams = data_teams.rename(columns={'Team': "Tm"})
    return data_teams


def main():
    """Main function to preparing team data to converting other data
    """

    config = load_config("configs/data_config.yaml")
    team_names = load_config("configs/teams_shortcuts.yaml")

    start_year = config.get("start_year")
    end_year = config.get("end_year")
    team_long = team_names.get("teams_long")

    while end_year > start_year:
        data_teams = pd.read_csv("data/teams_data_raw/teams_data_"+str(end_year-1)+"_"+str(end_year)+".csv")

        data_teams = team_data_droping(data_teams)
        team_result_feature(data_teams)

        data_teams = replace_team_names(data_teams, team_long)

        data_teams.to_csv("data/teams_data/teams_data_"+str(end_year-1)+"_"+str(end_year)+"_updated.csv", index=False)

        end_year -= 1
    


if __name__ == '__main__':
    main()
