# a) Your Python code should create three predictors (Distance, Obstacle_Type, Angle_Approach) and one output variable (Time_Collision)

import os
import typing as t

from collections import namedtuple


import numpy as np
import pandas as pd

glass_df = pd.read_csv(os.path.join("data", "Group2_1.csv"))
concrete_df = pd.read_csv(os.path.join("data", "Group2_2.csv"))

# the only usecase for zip lol
for df, obs_type in zip([glass_df, concrete_df], ["Glass", "Concrete"]):
    # df.set_index("Time", drop=True, inplace=True)
    # df.reindex().sort_index(ascending=False, inplace=True)
    df["Obstacle_type"] = obs_type
    df["Angle_Approach"] = (10 if obs_type == "Concrete" else 0) + np.random.uniform(
        -5, 5, df.shape[0]
    )
    df["Time_Collision"] = df["Value"] / 24


# b) Your team can trim a few seconds of last rows of data where the same distance “Value” column in the datasets is exactly repeated.


def strip_similar_rows(
    df: pd.DataFrame,
    columns: str | list[str],
    side: t.Literal["start", "end", "both"] = "end",
    thresh=0.1,
) -> None:
    """
    THIS MUTATES THE DF

    strips the rows that are similar to the last row (acc to `tresh`),
    but it leaves the last row

    expects the dataframe to have an integer index


    args:
        - df (DataFrame): the dataframe to operate on
        - columns (str | list[str]): column(s) of the values to compare
        - side ("start", "end", "both"): where to strip rows, default "end"
        - tresh (float): +/- val to consider \n
    returns:
        - None

    """
    Row = namedtuple("Row", ["index", "series"])

    # WTF WAS THIS
    last = df["Value"].iloc[-1]
    if side == "both":
        side = "end"
        strip_similar_rows(df, columns, "start", thresh)
    # iterrows() is a bad idea but whatever
    rows_since_dupe = 0
    to_drop: list[Row] = []
    for i, row in (df[::-1] if side == "end" else df).iterrows():
        if rows_since_dupe > 1:
            break
        if not (last - thresh <= row[columns] <= last + thresh):
            rows_since_dupe += 1
            continue
        to_drop.append(Row(i, row))
    df.drop(index=[i.index for i in to_drop], inplace=True)
    df.loc[len(df)] = to_drop[-1].series


strip_similar_rows(glass_df, "Value", "end", 0.2)
strip_similar_rows(concrete_df, "Value", "end", 0.4)


print()
