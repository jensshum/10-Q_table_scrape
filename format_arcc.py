#cik = 1287750


def fill_columns(df,col):
    """
    Takes a dataframe and column index as arguments, fills any hierarchical data with the previous input
    """
    print("zilco")
    col0_data = df[f"col{col}"]
    col_data = col0_data[0]
    temp_data = col_data
    for index, data in enumerate(col0_data):
        if str(col_data) != "nan":
            temp_data = col_data
        col_data = data
        if str(data) == "nan":
            df.at[index, f"col{col}"] = temp_data
    

def format_arcc(df):

    # For ARCC
    cols_to_fill = ["0","2"]
    for col in cols_to_fill:
        fill_columns(df,col)
    
    return df