"""Analysis tools"""
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from IPython.display import display
"""Overall problem: cols with strings seem to be entirely converted to strings"""

# Iterate over all urls
def _msg_unusual_grades(df, grade):
    """Print the number of unusual grades."""
    grades = np.arange(0, 10.5, 0.5).astype(float)
    catch_grades = []
    for item in df['grade']:
        try:
            if float(item) not in grades:
                catch_grades.append(item)
        except ValueError:
            catch_grades.append(item)

    print(f'– Over all grades, {len(catch_grades)} of {len(df)} cards do not receive standard grades.'
          f' These grades are in {set(catch_grades)}')


def _msg_n_grade(df, grade):
    """Print the number of cards with grade `grade`."""
    n_cards = len(df)
    n_grade = len(df[(df['grade']) == grade])
    perc = round((n_grade / n_cards) * 100, 2)

    print(f'– The number of cards with grade {grade} is {n_grade} of {n_cards} cards. That is {perc}%.')


def _filter_grade_data(df, grade):
    """Reduce df to date and price data for cards with grade `grade`."""
    df = df[(df['grade']) == grade]
    df = df[["date", "prize"]]

    return df


def _msg_avg_ann_growth(df):
    """Print the average annual prize growth."""
    df['year'] = pd.DatetimeIndex(df['date']).year
    df['avg_prize_in_year'] = df.groupby('year')['prize'].transform('mean')

    # Create pd.DataFrame for annual average prizes
    years = df['year'].drop_duplicates()
    prizes = df['avg_prize_in_year'].drop_duplicates()
    avg_df = pd.DataFrame({'year': years, 'prize': prizes})
    avg_df['perc_change'] = avg_df['prize'].pct_change(-1)

    # Delete first year to allow for NaNs if not enough obs
    avg_df = avg_df[avg_df['year'] != min(avg_df['year'])]

    # Compute average annual growth rate in percent
    g = round(avg_df["perc_change"].mean() * 100, 2)

    if np.isnan(g):
        print('– Cannot compute average annual prize growth rate. Perhaps not enough observations.')
    else:
        print(f'– The average annual prize growth rate from {min(years)} to {max(years)} is {g}%.')


def _get_card_name(card_url: str) -> str:  # noqa: D102
    c_name = card_url.split("-cards/")[1].split("/values")[0].replace("/", "-")
    return c_name


def _scatter_prize_time(df, title):
    x = mdates.date2num(df['date'])
    y = df['prize']

    fig, ax = plt.subplots(figsize=(12, 9))

    ax.scatter(df["date"], y, alpha=0.66)

    # Draw red trend line
    fit = np.polyfit(x, y, deg=4)
    p = np.poly1d(fit)
    ax.plot(x, p(x), 'r--')

    ## Rotate date labels automatically
    fig.autofmt_xdate()
    ax.grid(linestyle="-", color='black', alpha=0.25)
    ax.set_title(title, fontsize=28)
    ax.set_xlabel(xlabel='Date', size=26, labelpad=14)
    ax.set_ylabel(ylabel='Prize in $', size=26, labelpad=14)
    ax.grid(linestyle="-", color='black', alpha=0.25)
    ax.tick_params(length=6, width=2, labelsize=20)

    fig.tight_layout()

    plt.show()


"""Paths need to be revisited after I close pycharm."""
os.chdir('../..')




# df = pd.read_csv("output/data/1999-pokemon-game-charizard-holo.csv", parse_dates=["date"])
# df = pd.read_csv("output/data/2000-pokemon-rocket-dark-charizard-holo.csv", parse_dates=["date"])
# df = pd.read_csv("output/data/2002-nintendo-pokemon-neo-destiny-shining-charizard-1st-edition.csv", parse_dates=["date"])








grade = [str(9.0)]
show_data = False




# Read in urls from urls.txt
if not os.path.exists("input/urls.txt"):
    raise ValueError("no input url passed and 'urls.txt' not found")
with open("input/urls.txt") as f:
    urls = [n for n in f.read().split("\n") if n]
 
for url in urls:
    card_name = _get_card_name(url)
    df = pd.read_csv(f'output/data/{card_name}.csv', parse_dates=["date"])

    # Parse grade col. If some grades are string, the whole col is converted to str.
    df["grade"] = df["grade"].astype(str)

    if show_data is True:
        display(df)
    else:
        pass

    for g in grade:

        _msg_unusual_grades(df, g)

        _msg_n_grade(df, g)

        df = _filter_grade_data(df, g)

        _msg_avg_ann_growth(df)

        # ToDo: add grade to title
        _scatter_prize_time(df, card_name)
