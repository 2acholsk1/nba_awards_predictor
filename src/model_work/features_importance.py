#!/usr/bin/env python3
"""Generate figure with features importance
"""

import sys
import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


model_name = sys.argv[1]
model_path = 'model/' + model_name

if not os.path.isfile(model_path):
    print("Model does not exist.")
    sys.exit(1)

def main():
    """Ploting features importance
    """
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    data_example = pd.read_csv("model/example_for_columns_data.csv")
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