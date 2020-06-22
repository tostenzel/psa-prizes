"""Analysis tools."""
import ast
import json
import os
from typing import Any, Dict, Optional, Union

import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def analyze() -> None:
    """Return info messages as dict, plot prize timeline and save both.

    Notes
    -----
    For some cards, the grade data is of type `str` instead of `int` or `float`.
    pd.DataFrames assign the data-types column-wise by using the most compatible
    type. For example, the grade "Authentic" for only one card causes pandas
    to transform the whole column with grades in  {1.0, 1.5, ... 10.0} to be
    stored as `str`. Therefore, all grades are converted to `str` for a unified
    treatment. These strings are written like floats with one decimal place.

    """
    # Read grades. Delimeter has to be semicolon only.
    if not os.path.exists("input/input.csv"):
        raise ValueError("'input.csv' not found")
    df = pd.read_csv("input/input.csv", sep=";")

    # Convert List-String in input column to List[Union[float,int]].
    grades = df["grades (list)"].apply(ast.literal_eval).tolist()

    # Iterate over cards in input DataFrame.
    for row in range(len(df)):
        # Get card_name from urls
        card_name = _get_card_name(df.iloc[row, 0])

        # Important: Convert col to `str` as described in the notes.
        df_out = pd.read_csv(f"output/data/{card_name}.csv", parse_dates=["date"])
        df_out["grade"] = df_out["grade"].astype(str)

        # Iterate over grades per card.
        for g in grades[row]:

            # Parse grade as str due to reasons above.
            g = str(float(g))

            # Info on grades outside {1.0, 1.5, ... 10.0}.
            msg_grades = _str_unusual_grades(df_out)

            # Info on the share with this grade.
            msg_grades_n = _str_n_grade(df_out, g)

            # Drop rows with different grades.
            df_filt = _filter_grade_data(df_out, g)

            # Compute compund annual growth rate (CAGR).
            msg_return = _str_comp_ann_g(df_filt)

            # Store infos in dictionary and print.
            card_dict: Dict[str, Optional[str]] = {
                "ident": f"{card_name}-{g}",
                "compound annual growth": msg_return,
                "info grades number": msg_grades_n,
            }
            # Drop message if there are no unausual grades.
            if msg_grades_n is None:
                pass
            else:
                card_dict["info grades"] = msg_grades
            print(card_dict)

            # Save dictionary.
            if not os.path.exists("output/nmbrs"):
                os.makedirs("output/nmbrs")
            with open(f"output/nmbrs/{card_name}-grade-{g}.json", "w") as fp:
                json.dump(card_dict, fp)

            # Plot and save prize trend.
            _scatter_prize_time(df_filt, f"{card_name}-grade-{g}")


def _str_unusual_grades(df: pd.DataFrame) -> Union[str, None]:
    """Print the number of unusual grades."""
    grades = np.arange(0, 10.5, 0.5).astype(float)
    catch_grades = []
    for item in df["grade"]:
        try:
            if float(item) not in grades:
                catch_grades.append(item)
        except ValueError:
            catch_grades.append(item)

    if catch_grades == []:
        return None
    else:
        return (
            f"– Over all grades, {len(catch_grades)} of {len(df)} cards do not receive"
            f" standard grades. These grades are in {set(catch_grades)}"
        )


def _get_card_name(card_url: str) -> str:  # noqa: D102
    c_name = card_url.split("-cards/")[1].split("/values")[0].replace("/", "-")
    return c_name


def _str_n_grade(df: pd.DataFrame, grade: str) -> str:
    """Print the number of cards with grade `grade`."""
    n_cards = len(df)
    n_grade = len(df[(df["grade"]) == grade])
    perc = round((n_grade / n_cards) * 100, 2)

    return (
        f"– The number of cards with grade {grade} is {n_grade} "
        f"of {n_cards} cards. That is {perc}%."
    )


def _filter_grade_data(df: pd.DataFrame, grade: str) -> pd.DataFrame:
    """Reduce df to date and price data for cards with grade `grade`."""
    df = df[(df["grade"]) == grade]
    df = df[["date", "prize"]]

    return df


def _str_comp_ann_g(df: pd.DataFrame) -> str:
    """Print the average annual prize growth."""
    if df.empty is True:
        return "There is no prize data for this grade."
    else:
        df["year"] = pd.DatetimeIndex(df["date"]).year
        df["avg_prize_in_year"] = df.groupby("year")["prize"].transform("mean")

        # Create pd.DataFrame for annual average prizes.
        years = df["year"].drop_duplicates()
        prizes = df["avg_prize_in_year"].drop_duplicates()
        avg_df = pd.DataFrame({"year": years, "prize": prizes})

        # cagr = (1 + R) ** (1 / n) - 1
        t_0 = min(avg_df["year"])
        t_T = max(avg_df["year"])
        p_0 = avg_df[t_0 == avg_df["year"]]["prize"].iloc[0]
        p_T = avg_df[t_T == avg_df["year"]]["prize"].iloc[0]
        R = p_T / p_0
        n = t_T - t_0
        cagr = R ** (1 / n) - 1

        # Compute compound annual growth rate in percent.
        cagr = round(cagr * 100, 2)

        return (
            f"– The compound annual growth rate from {min(years)} "
            f"to {max(years)} is {cagr}%."
        )


def _scatter_prize_time(df: pd.DataFrame, title: str) -> Any:
    if df.empty is True:
        print("No prize data, no plot.")
    else:
        x = dates.date2num(df["date"])
        y = df["prize"]

        fig, ax = plt.subplots(figsize=(12, 9))

        ax.scatter(df["date"], y, alpha=0.66)

        # Draw red trend line.
        fit = np.polyfit(x, y, deg=3)
        p = np.poly1d(fit)
        ax.plot(x, p(x), "r--")

        # Rotate date labels.
        fig.autofmt_xdate()

        ax.grid(linestyle="-", color="black", alpha=0.25)
        ax.tick_params(length=6, width=2, labelsize=20)
        ax.set_title(title, fontsize=22)
        ax.set_xlabel(xlabel="Date", size=26, labelpad=14)
        ax.set_ylabel(ylabel="Prize in $", size=26, labelpad=14)

        fig.tight_layout()

        if not os.path.exists("output/img"):
            os.makedirs("output/img")

        plt.savefig(f"output/img/{title}.png")
        plt.show()

        return fig
