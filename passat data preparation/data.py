import datetime
import re
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt

df1 = pd.read_csv('passat.csv')
df2 = pd.read_csv('passat2.csv')

data = pd.concat([df1, df2])
data = data[data['price'] < 60000]
data = data[data['price'] > 1000]


data.drop(columns=['Generacja'], inplace=True)

important_columns = {'Rok produkcji', 'Przebieg', 'price'}

data = data[important_columns]
data.drop_duplicates(inplace=True)


data.dropna(subset=important_columns, inplace=True)
data['Przebieg'] = data['Przebieg'].str.replace(' km', '').str.replace(' ', '')
for col in ['Rok produkcji', 'Przebieg']:
    data[col] = pd.to_numeric(data[col])

numeric_columns = []
numeric_columns.extend(list(data.dtypes[data.dtypes == np.int64].index))
numeric_columns.extend(list(data.dtypes[data.dtypes == np.float64].index))
numeric_columns = set(numeric_columns) & important_columns
non_numeric_columns = important_columns - numeric_columns

data = data.reset_index()
data.drop(columns=['index'], inplace=True)

pd.DataFrame(data).to_csv('data.csv')