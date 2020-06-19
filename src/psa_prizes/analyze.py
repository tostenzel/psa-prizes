"""Analysis tools."""
import os
from typing import Any, List, Union

from IPython import display
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze(grades: List[Union[float, int]], show_data: bool = False) -> None:
    """Print info messages and plot prize timeline."""
    # Create output folder for pictures
    if not os.path.exists("output/img"):
        os.makedirs("output/img")

    # Read in urls from urls.txt
    if not os.path.exists("input/urls.txt"):
        raise ValueError("no input url passed and 'urls.txt' not found")
    with open("input/urls.txt") as f:
        urls = [n for n in f.read().split("\n") if n]

    for url in urls:
        # Get card_name from urls
        card_name = _get_card_name(url)

        df = pd.read_csv(f"output/data/{card_name}.csv", parse_dates=["date"])

        # Important: Parse col as str because one str may convert the whole col to str
        df["grade"] = df["grade"].astype(str)
        grades_str: List[str] = [str(float(g)) for g in grades]

        if show_data is True:
            display(df)
        else:
            pass

        for g in grades_str:
            _msg_unusual_grades(df, g)

            _msg_n_grade(df, g)

            df_filt = _filter_grade_data(df, g)

            _msg_comp_ann_g(df_filt)

            _scatter_prize_time(df_filt, f"{card_name}-grade-{g}")

            path = f"output/img/{card_name}-grade-{g}.png"
            print(f"– Find the graph for the above info in {path}")

            plt.savefig(path)
            plt.show()


def _msg_unusual_grades(df: pd.DataFrame, grade: str) -> None:
    """Print the number of unusual grades."""
    grades = np.arange(0, 10.5, 0.5).astype(float)
    catch_grades = []
    for item in df["grade"]:
        try:
            if float(item) not in grades:
                catch_grades.append(item)
        except ValueError:
            catch_grades.append(item)

    print(
        f"– Over all grades, {len(catch_grades)} of {len(df)} cards do not receive"
        f" standard grades. These grades are in {set(catch_grades)}"
    )


def _msg_n_grade(df: pd.DataFrame, grade: str) -> None:
    """Print the number of cards with grade `grade`."""
    n_cards = len(df)
    n_grade = len(df[(df["grade"]) == grade])
    perc = round((n_grade / n_cards) * 100, 2)

    print(
        f"– The number of cards with grade {grade} is {n_grade} "
        f"of {n_cards} cards. That is {perc}%."
    )


def _filter_grade_data(df: pd.DataFrame, grade: str) -> pd.DataFrame:
    """Reduce df to date and price data for cards with grade `grade`."""
    df = df[(df["grade"]) == grade]
    df = df[["date", "prize"]]

    return df


def _msg_comp_ann_g(df: pd.DataFrame) -> None:

    """Print the average annual prize growth."""
    df["year"] = pd.DatetimeIndex(df["date"]).year
    df["avg_prize_in_year"] = df.groupby("year")["prize"].transform("mean")

    # Create pd.DataFrame for annual average prizes
    years = df["year"].drop_duplicates()
    prizes = df["avg_prize_in_year"].drop_duplicates()
    avg_df = pd.DataFrame({"year": years, "prize": prizes})

    # cagr = (1 + R) ** (1 / n) - 1
    t_0 = min(avg_df["year"])
    t_T = max(avg_df["year"])
    p_0 = avg_df[t_0 == avg_df['year']]['prize'].iloc[0]
    p_T = avg_df[t_T == avg_df['year']]['prize'].iloc[0]
    R = p_T / p_0
    n = t_T - t_0
    cagr = (1 + R) ** (1 / n) - 1

    # Compute compound annual growth rate in percent
    cagr = round(cagr * 100, 2)

    if np.isnan(cagr):
        print(
            "– Cannot compute compound annual growth rate. "
            "Perhaps not enough observations."
        )
    else:
        print(
            f"– The compound annual growth rate from {min(years)} "
            f"to {max(years)} is {cagr}%."
        )


def _get_card_name(card_url: str) -> str:  # noqa: D102
    c_name = card_url.split("-cards/")[1].split("/values")[0].replace("/", "-")
    return c_name


def _scatter_prize_time(df: pd.DataFrame, title: str) -> Any:
    x = mdates.date2num(df["date"])
    y = df["prize"]

    fig, ax = plt.subplots(figsize=(12, 9))

    ax.scatter(df["date"], y, alpha=0.66)

    # Draw red trend line
    fit = np.polyfit(x, y, deg=3)

    p = np.poly1d(fit)
    ax.plot(x, p(x), "r--")

    # Rotate date labels
    fig.autofmt_xdate()

    ax.grid(linestyle="-", color="black", alpha=0.25)
    ax.tick_params(length=6, width=2, labelsize=20)
    ax.set_title(title, fontsize=22)
    ax.set_xlabel(xlabel="Date", size=26, labelpad=14)
    ax.set_ylabel(ylabel="Prize in $", size=26, labelpad=14)

    fig.tight_layout()

    return fig


