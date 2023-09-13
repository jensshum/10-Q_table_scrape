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
        
def replace_money_sign_2(row):
    """
    Replaces any cells filled with a "?" with the value in the adjacent cell.
    """
    if "$" in str(row['col19']):
        return row['col21']
    else:
        return row['col18']
    
def replace_money_sign_3(row):
    """
    Replaces any cells filled with a "?" with the value in the adjacent cell.
    """
    if "$" in str(row['col23']):
        return row['col24']
    else:
        return row['col21']

def move_misplaced_values(df):
    """
    Some values are offset by one cell. Moves those values into their correct column. 
    """
    # df['col18'] = df['col17']
    df['col18'].fillna(df['col17'], inplace=True)
    df['col21'].fillna(df['col20'], inplace=True)
    df['col23'].fillna(df['col22'], inplace=True)

    df['col15'] = df.apply(replace_money_sign, axis=1)
    df['col18'] = df.apply(replace_money_sign_2, axis=1)
    df['col21'] = df.apply(replace_money_sign_3, axis=1)

    return df

def drop_unnecessary_columns(df):
    """
    Removes any unnecessary columns.
    """
    df.drop(["col1","col3","col5","col9","col11","col13","col14","col16","col17","col19","col20","col22","col23"],axis=1,inplace=True)
    for col in df.columns:
        if int(col[3:]) > 23:
            df.drop(col,axis=1,inplace=True)

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


def rename_columns(df):
    """
    Renames the columns to the proper names.
    """
    col_mapping = {"col0": "Company Name", "col2": "Industry", "col4": "Security", "col6": "Interest Rate", "col7": "Reference Rate", "col8": "Spread", "col10": "Investment Date", "col12": "Maturity Date", "col15": "Principal", "col18": "Amortized Cost", "col21" : "Fair Value"}

    df = df.rename(columns=col_mapping)
    return df

def reorganize_columns(df):
    """
    Reorganizes the columns according to the correct order.
    """
    column_order = ["Company Name", "Industry", "Security", "Reference Rate", "Spread", "Interest Rate", "Maturity Date", "Fair Value", "Principal", "Amortized Cost", "Investment Date"]
    df = df[column_order]
    return df

def format_arcc(df):
    # For ARCC
    cols_to_fill = ["0","2"]
    for col in cols_to_fill:
        fill_columns(df,col)
    df = drop_totals(df)
    # df = move_misplaced_values(df)
    # df = drop_unnecessary_columns(df)
    # df = rename_columns(df)
    # df = reorganize_columns(df)

    
    return df