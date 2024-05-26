import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# Tworzenie instancji obiektu LabelEncoder
label_encoder = LabelEncoder()
label_encoder_pos = LabelEncoder()

eyear = 2022
year = 1999
data = None


while eyear > year:

    data2 = pd.read_csv("data/final_data/all_nba_final_"+str(eyear-1)+"_"+str(eyear)+".csv")
    data = pd.concat([data, data2])

    eyear -= 1


encoded_players = label_encoder.fit_transform(data['Player'])
encoded_pos = label_encoder_pos.fit_transform(data['Pos'])

data.insert(0, "Player_Encoded", encoded_players)
data.insert(0, "Pos_encoded",  encoded_pos)
data = data.drop(columns=['Player', 'Pos'])
shape = data.shape

# Wyświetlanie kształtu
print("Liczba wierszy:", shape[0])
print("Liczba kolumn:", shape[1])




label_encoder_y = LabelEncoder()
label_encoder_pos_y = LabelEncoder()

data1 = pd.read_csv("data/final_data/all_nba_final_2022_2023.csv")




encoded_players = label_encoder_y.fit_transform(data1['Player'])
encoded_pos = label_encoder_pos_y.fit_transform(data1['Pos'])

data1.insert(0, "Player_Encoded", encoded_players)
data1.insert(0, "Pos_encoded",  encoded_pos)
data1 = data1.drop(columns=['Player', 'Pos'])
print(data1.head())

data = data.dropna()
data1 = data1.dropna()


features1 = data1.iloc[:, :-2].values
labels1 = data1.iloc[:, -2:].values
print(labels1)
print("+++++++++++++++++++++++++++++++++++++++++++++")

# print(data[['Player', 'Player_Encoded']])

# Dekodowanie zakodowanych danych


# # Dodanie zdekodowanych danych do oryginalnego DataFrame

features = data.iloc[:, :-2].values
labels = data.iloc[:, -2].values

# pipe_svm_std = Pipeline(steps=[('std', StandardScaler()), ('cf', SVC(kernel='rbf', gamma='scale'))])
# pipe_svm_std.fit(features, labels)
# print(f'\nTotal score for SVM: {pipe_svm_std.score(features1,labels1)}\n')
# y_predict = pipe_svm_std.predict(features1)
# print(y_predict)

print("+++++++++++++++++++++++++++++++++++++++++++++")

pipe_random_forest_std = Pipeline(steps=[('cf', RandomForestClassifier())])
pipe_random_forest_std.fit(features, labels)
print(f'\nTotal score for RandomForestClassifier: {pipe_random_forest_std.score(features1,labels1)}\n')
y_predict1 = pipe_random_forest_std.predict(features1)
print(y_predict1)



# decoded_players = label_encoder.inverse_transform(encoded_players)
# data['Player_Decoded'] = decoded_players

# # Wyświetlenie wyników
# print(data[['Player_Encoded', 'Player_Decoded']])
