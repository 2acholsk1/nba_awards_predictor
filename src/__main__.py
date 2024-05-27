#!/usr/bin/env python3

import sys
import pickle
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from src.config_func import load_config


prediction_path = sys.argv[1]

def main():
    

    config = load_config("configs/prediction_config.yaml")
    model_name = config.get("prediction_model")
    model_name_rook = config.get("prediction_model_rook")
    drop_features = config.get("drop_features")
    drop_features_rook = config.get("drop_features_rook")

    with open("model/"+str(model_name)+".pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/"+str(model_name_rook)+".pkl", "rb") as f:
        model_rook = pickle.load(f)

    label_encoder_test = LabelEncoder()
    label_encoder_pos_test = LabelEncoder()
    label_encoder_tm_test = LabelEncoder()
    label_encoder_test_rook = LabelEncoder()
    label_encoder_pos_test_rook = LabelEncoder()
    label_encoder_tm_test_rook = LabelEncoder()

    data_test = pd.read_csv("data/final_data/all_nba_final_2023_2024.csv")
    data_test = data_test.dropna()
    data_test = data_test.drop(columns=drop_features)
    data_test_rook = pd.read_csv("data/final_data/rookie_final_2023_2024.csv")
    data_test_rook = data_test_rook.dropna()
    data_test_rook = data_test_rook.drop(columns=drop_features_rook)

    encoded_players_test = label_encoder_test.fit_transform(data_test['Player'])
    encoded_pos_test = label_encoder_pos_test.fit_transform(data_test['Pos'])
    encoded_tm_test = label_encoder_tm_test.fit_transform(data_test['Tm'])
    encoded_players_test_rook = label_encoder_test_rook.fit_transform(data_test_rook['Player'])
    encoded_pos_test_rook = label_encoder_pos_test_rook.fit_transform(data_test_rook['Pos'])
    encoded_tm_test_rook = label_encoder_tm_test_rook.fit_transform(data_test_rook['Tm'])

    data_test.insert(0, "Player_Encoded", encoded_players_test)
    data_test.insert(0, "Pos_encoded",  encoded_pos_test)
    data_test.insert(0, "Tm_encoded",  encoded_tm_test)
    data_test = data_test.drop(columns=['Player', 'Pos', 'Rk', 'Tm'])
    data_test_rook.insert(0, "Player_Encoded", encoded_players_test_rook)
    data_test_rook.insert(0, "Pos_encoded",  encoded_pos_test_rook)
    data_test_rook.insert(0, "Tm_encoded",  encoded_tm_test_rook)
    data_test_rook = data_test_rook.drop(columns=['Player', 'Pos', 'Rk', 'Tm'])

    features_test = data_test.iloc[:, :-1].values
    features_test_rook = data_test_rook.iloc[:, :-1].values
    
    y_pred_prob = model.predict_proba(features_test)
    y_pred_prob_rook = model_rook.predict_proba(features_test_rook)

    decoded_players = label_encoder_test.inverse_transform(encoded_players_test)
    data_test['Player_Decoded'] = decoded_players
    decoded_players_rook = label_encoder_test_rook.inverse_transform(encoded_players_test_rook)
    data_test_rook['Player_Decoded'] = decoded_players_rook

    for i, class_name in enumerate(['None', '1st', '2nd', '3rd']):
        class_prob = y_pred_prob[:, i]
        data_test[f'Prob_{class_name}'] = class_prob
    for i, class_name in enumerate(['None', '1st', '2nd']):
        class_prob_rook = y_pred_prob_rook[:, i]
        data_test_rook[f'Prob_{class_name}'] = class_prob_rook

    selected_players = set()

    first_team = data_test.nlargest(5, 'Prob_1st')
    selected_players.update(first_team['Player_Decoded'])
    data_test = data_test[~data_test['Player_Decoded'].isin(selected_players)]

    second_team = data_test.nlargest(5, 'Prob_2nd')
    selected_players.update(second_team['Player_Decoded'])
    data_test = data_test[~data_test['Player_Decoded'].isin(selected_players)]

    third_team = data_test.nlargest(5, 'Prob_3rd')
    selected_players.update(third_team['Player_Decoded'])
    data_test = data_test[~data_test['Player_Decoded'].isin(selected_players)]

    first_rookie_team = data_test_rook.nlargest(5, 'Prob_1st')
    selected_players.update(first_rookie_team['Player_Decoded'])
    data_test_rook = data_test_rook[~data_test_rook['Player_Decoded'].isin(selected_players)]

    second_rookie_team = data_test_rook.nlargest(5, 'Prob_2nd')
    selected_players.update(second_rookie_team['Player_Decoded'])
    data_test_rook = data_test_rook[~data_test_rook['Player_Decoded'].isin(selected_players)]

    teams = {
        "first all-nba team": first_team['Player_Decoded'].tolist(),
        "second all-nba team": second_team['Player_Decoded'].tolist(),
        "third all-nba team": third_team['Player_Decoded'].tolist(),
        "first rookie all-nba team": first_rookie_team['Player_Decoded'].tolist(),
        "second rookie all-nba team": second_rookie_team['Player_Decoded'].tolist(),
    }

    with open(prediction_path+'.json', 'w', encoding='utf-8') as f:
        json.dump(teams, f, indent=2)


if __name__ == '__main__':
    main()