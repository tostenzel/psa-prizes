"""Analysis tools"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""Paths need to be revistited after I close pycharm."""
os.chdir('../..')

"""
def _clean_data(
    df : pd.Dataframe,
    grade : Union[int, float],
    print_df : bool,
    
    return df, info_dict

"""
print_df = True




grade = 9

df = pd.read_csv("output/data/1999-pokemon-game-charizard-holo.csv", parse_dates=["date"])

print(df.to_string())



grades = np.arange(0,10.5,0.5).astype(float)
catch_grades = []
for item in df['grade']:
    try:
        if float(item) not in grades:
            catch_grades.append(item)
    except ValueError:
        catch_grades.append(item)

print(catch_grades) # for info_dict

df = df[(df['grade']) == str(grade)]

df = df[["date", "grade"]]

n_cards = len(df) # for info_dict

"""def scatterplot(df):"""