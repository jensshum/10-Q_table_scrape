# -*- coding: utf-8 -*-
"""

SEC Filing Scraper
@author: AdamGetbags

"""

# import modules
import requests
import pandas as pd
import sys
from bs4 import BeautifulSoup
import os
import openai

LLM = 'gpt-4'
# create request header
headers = {'User-Agent': "email@address.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

# review response / keys
# print(companyTickers.json().keys())

# format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']

# parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')

# add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(
                           str).str.zfill(10)

# review data

company_data_dict = companyData.set_index('cik_str')['ticker'].to_dict()


cik_tickers = ["1634452", "1578620","1278752","1287750","1633858","1655050",	"1379785","1326003","1370755","1736035","1490927","17313","1571329","1534254","1578348","1617896","1633336","878932", "1513363", "1495584","1701724","1501729",
"1637417","1525759","1579412","1422183","1509892","1143513","1321741", "1572694","1683074","1674760","1476765","1715268","1627515","1675033","1509470","1618697","1661306","1559909", "1280784","1535778","1487428","1550913","1396440",
"1490349","1512931","1742313","1099941","1496099","1588272","1414932","1577791", "1744179", "1487918","1297704", "1655888", "1655887", "1747777", "1259429", "1626899", "1383414","1504619", "1372807", "845385", "1287032","81955", "1653384", 
"1743415", "1523526", "1614173", "1418076",	"1508171", "1551901", "1702510", "1544206", "1603480", "1715933", "1577134", "1464963","1521945","1508655","1580345", "1717310", "1557424","1642862", "1552198"]

cik_tickers = [value.zfill(10) for value in cik_tickers]

# # get company specific filing metadata

html_links = []
for cik in cik_tickers:
    filingMetadata = requests.get(
        f'https://data.sec.gov/submissions/CIK{cik}.json',
        headers=headers
        )

    # review json 
    # print(filingMetadata.json().keys())
    # filingMetadata.json()['filings']
    # filingMetadata.json()['filings'].keys()
    # filingMetadata.json()['filings']['recent']
    # filingMetadata.json()['filings']['recent'].keys()

    # dictionary to dataframe
    allForms = pd.DataFrame.from_dict(
                filingMetadata.json()['filings']['recent'])

    # review columns
    allForms.columns
    allForms[['accessionNumber', 'reportDate', 'form']].head(100)

    # 10-Q metadata
    allForms.iloc[11]
    forms = allForms[allForms['form'] == '10-Q'].reset_index(drop = True)

    accession_numbers = forms.loc[forms["form"] == "10-Q", "accessionNumber"].tolist()
    html_caps = forms.loc[forms["form"] == "10-Q", "primaryDocument"].tolist()

    k = 1
    for html, num in zip(html_caps, accession_numbers):
        
        num = num.replace("-","")
        url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{num}/{html}"
        print(url)

        response = requests.get(url, headers=headers)
        html_content = response.text

        ## WORKING FOR AB Private Investor Corp -- 1634452 cik
        # if "1634452" in cik:
        corrected_cols = ["Company Name","Industry","Security","Reference Rate","Spread","Interest Rate","Maturity Date","Fair", "Value", "Principal","Amortized Cost","Investment Date"]
        investment_tables = html_content.lower().split("schedule of investments")
        if len(investment_tables) == 1:
            print("No schedule info")
            continue

        print(f"10-Q file num {k} of", len(accession_numbers), f"for {cik}")

        tables = []
        cols = []
        df = pd.DataFrame()
        for i, table_text in enumerate(investment_tables[1:]):
            if k > 5:
                continue
            values = []
            soup = BeautifulSoup(table_text, 'html.parser')
            table = soup.find('table')
            if table == None:
                continue

            row_num = 0

            for row in table.find_all('tr'):
                columns = row.find_all('td')
                row_data = {}
                for j, col in enumerate(columns):
                    cell_text = col.get_text(strip=True)
                    row_data[f'col{j}'] = cell_text
                values.append(row_data)
                
            df_to_append = pd.DataFrame(values)
            # print(df_to_append.columns)
            if i == 0:
                cols = [str(value).strip() for value in df_to_append.iloc[1]]
                print(cols)

            # df_to_append = df_to_append[2:]
            if len(df_to_append.columns) > 21:
                continue
            df = pd.concat([df, df_to_append], ignore_index=True)

            ## For ARCC
            # cols_to_fill = ["0","2"]
            # for col in cols_to_fill:
            #     col0_data = df[f"col{col}"]
            #     col_data = col0_data[0]
            #     temp_data = col_data
            #     for index, data in enumerate(col0_data):
            #         if str(col_data) != "nan":
            #             temp_data = col_data
            #         col_data = data
            #         if str(data) == "nan":
            #             df.at[index, f"col{col}"] = temp_data

            # try:
            # col_mapping = {"Company (1)": "Company Name", "Investment": "Security", "Par / Units": "Principal", "Amortized Cost(3)(4)": "Amortized Cost"}
            #     df = df.rename(columns = col_mapping)
            # except Exception:

        df.columns = corrected_cols
        df = df[6:]

        try:
            os.mkdir(f"CIK_{cik}")
        except Exception:
            pass
        df.to_csv(f"CIK_{cik}/CIK_{cik}_filenum_{k}_of_{len(accession_numbers)}_test.csv", index=False)
        k += 1
        break
    sys.exit()

    # Specific to Blue Owl Capital
    # df['Reference Rate'] = df['Interest'].apply(lambda x: x.split(' ')[0])
    # df['Spread'] = df['Interest'].apply(lambda x: x.split(' ')[1])
    # del df['Interest']



# https://www.sec.gov/Archives/edgar/data/1287750/000128775023000036/arcc-20230630.htm