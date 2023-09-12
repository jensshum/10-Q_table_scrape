#cik = 1287750
import time
import numpy as np
import pandas as pd

def replace_money_sign(row):
    """
    Replaces any cells filled with a "?" with the value in the adjacent cell.
    """
    if "$" in str(row['col15']):
        return row['col16']
    else:
        return row['col15']

def move_misplaced_values(df):
    """
    Some values are offset by one cell. Moves those values into their correct column. 
    """
    # df['col18'] = df['col17']
    df['col18'].fillna(df['col17'], inplace=True)
    df['col21'].fillna(df['col20'], inplace=True)
    df['col23'].fillna(df['col22'], inplace=True)
    

    df['col15'] = df.apply(replace_money_sign, axis=1)

    return df

def drop_unnecessary_columns(df):
    """
    Removes any irrelevant columns.
    """
    df.drop(["col9","col11","col13","col17","col20","col22"],axis=1,inplace=True)
    return df


def drop_totals(df):
    """
    Drops any rows containing totals.
    """
    df = df.applymap(lambda x: None if len(str(x)) == 0 else x)
    mask = df.count(axis=1) > 4
    # print(mask)
    filtered_df = df[mask]
    return filtered_df


def fill_columns(df,col):
    """
    Takes a dataframe and column index as arguments, fills any hierarchical data with the previous input
    """
    col0_data = df[f"col{col}"]
    col_data = col0_data[0]
    temp_data = col_data
    for index, data in enumerate(col0_data):
        if len(str(col_data)) != 0:
            temp_data = col_data
        col_data = data
        if len(str(data)) == 0 or str(data) == "nan":
            df.at[index, f"col{col}"] = temp_data
    

def format_arcc(df):
    # For ARCC
    cols_to_fill = ["0","2"]
    for col in cols_to_fill:
        fill_columns(df,col)
    df = drop_totals(df)
    df = move_misplaced_values(df)
    df = drop_unnecessary_columns(df)

    
    return df