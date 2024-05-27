#!/usr/bin/env python3
"""Generate figure with features importance
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.config_func import load_config



def main():
    """Ploting features importance
    """

    config = load_config("configs/prediction_config.yaml")
    model_name = config.get("model_name_rook")
    
    with open('model/'+str(model_name)+'.pkl', 'rb') as f:
        model = pickle.load(f)

    data_example = pd.read_csv("model/rookie_example_for_columns_data.csv")
    print(data_example.columns[:-1])
    feature_importance = model.feature_importances_
    feature_names = data_example.columns[:-1]
    
    feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importance})
    feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(12, 10))
    sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
    plt.title('Feature Importance')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.show()

if __name__ == '__main__':
    main()