# #!/usr/bin/env python3

# import pandas as pd
# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.metrics import classification_report, accuracy_score
# import xgboost as xgb
# from sklearn.ensemble import GradientBoostingClassifier
# import numpy as np
# from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sns

# def main():
#     label_encoder = LabelEncoder()
#     label_encoder_pos = LabelEncoder()
#     label_encoder_test = LabelEncoder()
#     label_encoder_pos_test = LabelEncoder()

#     eyear = 2023
#     year = 1999
#     data = None

#     while eyear > year:

#         data_con = pd.read_csv("data/final_data/all_nba_final_"+str(eyear-1)+"_"+str(eyear)+".csv")
#         data = pd.concat([data, data_con])

#         eyear -= 1

#     data = data.dropna()

#     encoded_players = label_encoder.fit_transform(data['Player'])
#     encoded_pos = label_encoder_pos.fit_transform(data['Pos'])

#     data.insert(0, "Player_Encoded", encoded_players)
#     data.insert(0, "Pos_encoded",  encoded_pos)
#     data = data.drop(columns=['Player', 'Pos', 'Rk'])

#     features = data.iloc[:, :-1].values
#     labels = data.iloc[:, -1].values

#     data_test = pd.read_csv("data/final_data/all_nba_final_2023_2024.csv")
#     data_test = data_test.dropna()

#     encoded_players_test = label_encoder_test.fit_transform(data_test['Player'])
#     encoded_pos_test = label_encoder_pos_test.fit_transform(data_test['Pos'])

#     data_test.insert(0, "Player_Encoded", encoded_players_test)
#     data_test.insert(0, "Pos_encoded",  encoded_pos_test)
#     data_test = data_test.drop(columns=['Player', 'Pos', 'Rk'])

#     features_test = data_test.iloc[:, :-1].values
#     labels_test = data_test.iloc[:, -1].values

#     dtrain = xgb.DMatrix(features, label=labels)
#     dtest = xgb.DMatrix(features_test, label=labels_test)

#     # X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.0, random_state=42)

#     model = xgb.XGBClassifier(objective='multi:softmax', num_class=4, random_state=42)


#     params = {
#         'learning_rate': [0.1],
#         'max_depth': [6],
#         'min_child_weight': [1],
#         'subsample': [0.6],
#         'colsample_bytree': [0.6],
#         'n_estimators': [100]
#     }

#     grid_search = GridSearchCV(estimator=model, param_grid=params, cv=3, scoring='accuracy', verbose=1, n_jobs=-1)
#     grid_search.fit(features, labels)

#     best_params = grid_search.best_params_
#     print(f"Best parameters found: {best_params}")

#     best_model = grid_search.best_estimator_
#     best_model.fit(features, labels)

#     # Predykcja na zbiorze testowym
#     y_pred = best_model.predict(features_test)

#     print(classification_report(labels_test, y_pred))
#     print(f'Accuracy: {accuracy_score(labels_test, y_pred)}')
#     print(type(y_pred))

#     decoded_players = label_encoder_test.inverse_transform(encoded_players_test)
#     data_test['Player_Decoded'] = decoded_players
#     index = np.where(y_pred == 1.0)
#     print(f"1 ; {index}")
#     print(data_test.iloc[index])
#     index = np.where(y_pred == 2.0)
#     print(f"2 ; {index}")
#     print(data_test.iloc[index])
#     index = np.where(y_pred == 3.0)
#     print(f"3 ; {index}")
#     print(data_test.iloc[index])

#     cm = confusion_matrix(labels_test, y_pred)
#     plt.figure(figsize=(8, 6))
#     sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", annot_kws={"size": 16})
#     plt.xlabel('Predicted labels')
#     plt.ylabel('True labels')
#     plt.title('Confusion Matrix')
#     plt.show()


# if __name__ == '__main__':
#     main()



#!/usr/bin/env python3

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, log_loss, confusion_matrix
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    label_encoder = LabelEncoder()
    label_encoder_pos = LabelEncoder()
    label_encoder_test = LabelEncoder()
    label_encoder_pos_test = LabelEncoder()

    eyear = 2023
    year = 1999
    data = []

    while eyear > year:
        data_con = pd.read_csv("data/final_data/all_nba_final_" + str(eyear-1) + "_" + str(eyear) + ".csv")
        data.append(data_con)
        eyear -= 1

    data = pd.concat(data)
    data = data.dropna()

    encoded_players = label_encoder.fit_transform(data['Player'])
    encoded_pos = label_encoder_pos.fit_transform(data['Pos'])

    data.insert(0, "Player_Encoded", encoded_players)
    data.insert(0, "Pos_encoded",  encoded_pos)
    data = data.drop(columns=['Player', 'Pos', 'Rk'])

    features = data.iloc[:, :-1].values
    labels = data.iloc[:, -1].values

    data_test = pd.read_csv("data/final_data/all_nba_final_2023_2024.csv")
    data_test = data_test.dropna()

    encoded_players_test = label_encoder_test.fit_transform(data_test['Player'])
    encoded_pos_test = label_encoder_pos_test.fit_transform(data_test['Pos'])

    data_test.insert(0, "Player_Encoded", encoded_players_test)
    data_test.insert(0, "Pos_encoded",  encoded_pos_test)
    data_test = data_test.drop(columns=['Player', 'Pos', 'Rk'])

    features_test = data_test.iloc[:, :-1].values
    labels_test = data_test.iloc[:, -1].values

    # Dostosowanie modelu XGBoost do przewidywania prawdopodobieństw
    model = xgb.XGBClassifier(objective='multi:softprob', 
                              colsample_bytree=0.6, 
                              learning_rate=0.1, 
                              max_depth=6, 
                              min_child_weight=1, 
                              n_estimators=100, 
                              subsample=0.6,
                              random_state=42)

    # Trenowanie modelu z najlepszymi parametrami
    model.fit(features, labels)

    # Predykcja prawdopodobieństw na zbiorze testowym
    y_pred_prob = model.predict_proba(features_test)

    # Zamiana prawdopodobieństw na etykiety
    y_pred = np.argmax(y_pred_prob, axis=1)

    # Ocena modelu
    print(classification_report(labels_test, y_pred))
    print(f'Accuracy: {accuracy_score(labels_test, y_pred)}')
    print(f'Log Loss: {log_loss(labels_test, y_pred_prob)}')

    decoded_players = label_encoder_test.inverse_transform(encoded_players_test)
    data_test['Player_Decoded'] = decoded_players

    # Wyświetlanie prawdopodobieństw przynależności do danych klas
    for i, class_name in enumerate(['None', '1st', '2nd', '3rd']):
        class_prob = y_pred_prob[:, i]
        data_test[f'Prob_{class_name}'] = class_prob

    # Wyświetlanie 5 graczy z największym prawdopodobieństwem przynależności do każdej klasy
    for class_name in ['1st', '2nd', '3rd']:
        top_5 = data_test.nlargest(5, f'Prob_{class_name}')
        print(f"Top 5 players for {class_name} NBA Team:")
        print(top_5[['Player_Decoded', f'Prob_{class_name}']])
        print()

    cm = confusion_matrix(labels_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", annot_kws={"size": 16})
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.show()

if __name__ == '__main__':
    main()
