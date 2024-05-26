#!/usr/bin/env python3

import pickle
import xgboost as xgb
import pandas as pd
from scipy.stats import uniform, randint
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import RandomizedSearchCV
from src.config_func import load_config

def main():
    
    config = load_config("configs/prediction_config.yaml")
    drop_features = config.get("drop_features")
    params_name = config.get("params_name")
    start_year = config.get("start_year")
    end_year = config.get("end_year")
    end_year -= 1
    data = []


    label_encoder = LabelEncoder()
    label_encoder_pos = LabelEncoder()
    label_encoder_tm = LabelEncoder()

    
    

    while end_year > start_year:
        data_con = pd.read_csv("data/final_data/all_nba_final_" + str(end_year-1) + "_" + str(end_year) + ".csv")
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

    features = data.iloc[:, :-1].values
    labels = data.iloc[:, -1].values

    model = xgb.XGBClassifier(objective='multi:softprob')

    param_dist = {
        'learning_rate': uniform(0.01, 0.3),
        'max_depth': randint(1, 10),
        'min_child_weight': randint(1, 10),
        'subsample': uniform(0.5, 0.5),
        'colsample_bytree': uniform(0.5, 0.5),
        'gamma': uniform(0, 0.5),
        'reg_alpha': uniform(0, 1),
        'reg_lambda': uniform(0, 1),
        'n_estimators': randint(50, 200)
    }

    random_search_xgb = RandomizedSearchCV(model, param_distributions=param_dist, n_iter=100, cv=5, verbose=2, random_state=42, n_jobs=-1)
    random_search_xgb.fit(features, labels)

    print(f"Best parameters found by Randomized Search:{random_search_xgb.best_params_}")
    with open('model/params/'+str(params_name)+'.pkl', 'wb') as f:
        pickle.dump(random_search_xgb.cv_results_, f)
    

if __name__ == '__main__':
    main()
