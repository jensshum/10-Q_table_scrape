def format_AB_private_investor(df):
    # corrected_cols = get_corrected_cols(cik)
    corrected_cols = ["Company Name","Industry","Security","Reference Rate","Spread","Interest Rate","Maturity Date","Fair", "Value", "Principal","Amortized Cost","Investment Date"]

    col_mapping = {"col0": "Company Name", "col2" : "Industry", "col4": "Security", "col6": "Interest", "col8": "Maturity Date", "col11": "Principal", "col15": "Amortized Cost", "col19": "Fair Value" }
    
    try:
        df = df.drop(["col1","col3","col5","col7","col9","col10","col12","col13","col14","col16","col17","col18","col20"],axis=1)
    except Exception:
        print("err")
        df.to_csv("Errr.csv")
    df = df.rename(columns=col_mapping)

    df = df[6:]
    df["Reference Rate"] = df['Interest'].apply(lambda x: str(x).replace("—","").split(' ')[0])
    df["Spread"] = df["Interest"].apply(lambda x: " ".join(str(x).replace("—","").replace("(","").split(" ")[1:4]) if 2 < len(str(x).split(" ")) <= 6 else " ".join(str(x).split(" ")[1:6]))
    df["Interest Rate"] = df["Interest"].apply(lambda x: " ".join(str(x).replace("—","").replace("(","").split(" ")[4:]) if 2 < len(str(x).split(" ")) <= 6 else " ".join(str(x).split(" ")[6:]))
    df = df.drop("Interest", axis=1)
    df = df[df.iloc[:, 0] != '']

    order_of_columns = ["Company Name","Industry","Security","Reference Rate","Spread","Interest Rate","Maturity Date","Fair Value","Principal","Amortized Cost"]

    df = df[order_of_columns]

    return df