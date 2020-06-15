"""Analysis tools"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from IPython.display import display

"""Paths need to be revistited after I close pycharm."""
os.chdir('../..')

df = pd.read_csv("output/data/1999-pokemon-game-charizard-holo.csv", parse_dates=["date"])

grade = 9
show_data = False

if show_data is True:
    display(df)
else:
    pass


def _unusual_grades_msg(df, grade):
    """Print the number of unusual grades."""
    grades = np.arange(0, 10.5, 0.5).astype(float)
    catch_grades = []
    for item in df['grade']:
        try:
            if float(item) not in grades:
                catch_grades.append(item)
        except ValueError:
            catch_grades.append(item)

    print(f'Over all grades, {len(catch_grades)} of {len(df)} cards do not receive standard grades.'
          f' These grades are {set(catch_grades)}')


def _n_grade_msg(df, grade):
    """Print the number of cards with grade `grade`."""
    n_cards = len(df)
    n_grade = len(df[(df['grade']) == str(grade)])
    perc = round((n_grade / n_cards) * 100, 2)

    print(f'The number of cards with grade {grade} is {n_grade} of {n_cards} cards. That is {perc}%.')


def _filter_grade_data(df, grade):
    """Reduce df to data and price data for cards with grade `grade`."""
    df = df[(df['grade']) == str(grade)]
    df = df[["date", "prize"]]

    return df

def _avg_ann_growth_msg(df):
    """Compute annual growth."""
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['avg_prize_in_year'] = df.groupby('year')['prize'].transform('mean')

    # Create pd.DataFrame for annual average prizes
    years = df['year'].drop_duplicates()
    prizes = df['avg_prize_in_year'].drop_duplicates()
    avg_df = pd.DataFrame({'year': years, 'prize': prizes})
    avg_df['perc_change'] = avg_df['prize'].pct_change(-1)

    # Compute average annual growth rate in percent
    g = avg_df["perc_change"].dropna().mean() * 100

    print(f'The annual average growth rate is {g}% from {min(years)} to {max(years)}.')

df.head()
_unusual_grades_msg(df, grade)

_n_grade_msg(df, grade)

df = _filter_grade_data(df, grade)

_avg_ann_growth_msg(df)





x = mdates.date2num(df['date'])
y = df['prize']

fig, ax = plt.subplots()

ax.scatter(df["date"], y)

# Draw red trend line
fit = np.polyfit(x, y, deg=4)
p = np.poly1d(fit)
ax.plot(x, p(x), 'r--')

## Rotate date labels automatically
fig.autofmt_xdate()

plt.show()
