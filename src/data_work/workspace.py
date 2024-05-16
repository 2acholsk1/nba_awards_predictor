import pandas as pd
from src.data_work.prepare_data import import_raw_data
from src.data_work.prepare_data import droping_unnecessary_data

data = import_raw_data(2002)
data = droping_unnecessary_data(data)

print(data.head())