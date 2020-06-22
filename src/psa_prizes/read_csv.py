print('hello')
import os

import pandas as pd

os.chdir('../..')

df = pd.read_csv('input/input.csv', sep=';')

import ast

# Convert string to List[Union[float,int]]
df['grades (list)'] = df['grades (list)'].apply(ast.literal_eval)

print(df)

a = df.iloc[1,1]

print(a)
