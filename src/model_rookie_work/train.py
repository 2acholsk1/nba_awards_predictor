#!/usr/bin/env python3

import pickle
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, log_loss
from src.config_func import load_config

def main():
    label_encoder = LabelEncoder()
    label_encoder_pos = LabelEncoder()
    label_encoder_tm = LabelEncoder()
    label_encoder_test = LabelEncoder()
    label_encoder_pos_test = LabelEncoder()

    config = load_config("configs/prediction_config.yaml")

    start_year = config.get("start_year")
    end_year = config.get("end_year")
    params_name = config.get("params_name_rook")
    model_name = config.get("model_name_rook")
    drop_features = config.get("drop_features_rook")
    data = []

    end_year -= 1

    with open('model/params/'+str(params_name)+'.pkl', 'rb') as f:
        best_params = pickle.load(f)

    while end_year > start_year:
        data_con = pd.read_csv("data/final_data/rookie_final_" + str(end_year-1) + "_" + str(end_year) + ".csv")
        data.append(data_con)
        end_year -= 1

    data = pd.concat(data)
    data = data.dropna()
    data = data.drop(columns=drop_features)

    encoded_players = label_encoder.fit_transform(data['Player'])
    encoded_pos = label_encoder_pos.fit_transform(data['Pos'])
    encoded_tm = label_encoder_tm.fit_transform(data['Tm'])

    data.insert(0, "Player_Encoded", encoded_players)
    data.insert(0, "Pos_encoded",  encoded_pos)
    data.insert(0, "Tm_encoded",  encoded_tm)
    data = data.drop(columns=['Player', 'Pos', 'Rk', 'Tm'])
    data.to_csv("model/rookie_example_for_columns_data.csv", index=False)

    features = data.iloc[:, :-1].values
    labels = data.iloc[:, -1].values

    data_test = pd.read_csv("data/final_data/rookie_final_2023_2024.csv")
    data_test = data_test.dropna()
    data_test = data_test.drop(columns=drop_features)

    encoded_players_test = label_encoder_test.fit_transform(data_test['Player'])
    encoded_pos_test = label_encoder_pos_test.fit_transform(data_test['Pos'])
    encoded_tm_test = label_encoder_pos_test.fit_transform(data_test['Pos'])

    data_test.insert(0, "Player_Encoded", encoded_players_test)
    data_test.insert(0, "Pos_encoded",  encoded_pos_test)
    data_test.insert(0, "Tm_encoded",  encoded_tm_test)
    data_test = data_test.drop(columns=['Player', 'Pos', 'Rk', 'Tm'])

    features_test = data_test.iloc[:, :-1].values
    labels_test = data_test.iloc[:, -1].values

    model = xgb.XGBClassifier(**best_params)

    model.fit(features, labels)

    y_pred_prob = model.predict_proba(features_test)

    y_pred = np.argmax(y_pred_prob, axis=1)

    decoded_players = label_encoder_test.inverse_transform(encoded_players_test)
    data_test['Player_Decoded'] = decoded_players

    for i, class_name in enumerate(['None', '1st', '2nd']):
        class_prob = y_pred_prob[:, i]
        data_test[f'Prob_{class_name}'] = class_prob

    for class_name in ['1st', '2nd']:
        top_10 = data_test.nlargest(10, f'Prob_{class_name}')
        print(f"Top 10 players for {class_name} rookie NBA Team:")
        print(top_10[['Player_Decoded', f'Prob_{class_name}']])
        

    print(classification_report(labels_test, y_pred))
    print(f'Accuracy: {accuracy_score(labels_test, y_pred)}')
    print(f'Log Loss: {log_loss(labels_test, y_pred_prob)}')

    with open('model/'+str(model_name)+'.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    main()
