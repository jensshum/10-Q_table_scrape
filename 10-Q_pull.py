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
from ixbrlparse import IXBRL

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
# print(companyData[:1])

company_data_dict = companyData.set_index('ticker')['cik_str'].to_dict()

# print(company_data_dict)
# with open("file.txt",'w') as f:
#     f.write(str(company_data_dict))
# sys.exit()

cik = company_data_dict['ARCC']

# print(cik)

# # get company specific filing metadata
filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )

# review json 
# print(filingMetadata.json().keys())
filingMetadata.json()['filings']
filingMetadata.json()['filings'].keys()
filingMetadata.json()['filings']['recent']
filingMetadata.json()['filings']['recent'].keys()

# dictionary to dataframe
allForms = pd.DataFrame.from_dict(
             filingMetadata.json()['filings']['recent']
             )

# review columns
allForms.columns
allForms[['accessionNumber', 'reportDate', 'form']].head(80)

# 10-Q metadata
allForms.iloc[11]
thing = allForms[allForms['form'] == '10-Q'].reset_index(drop = True)

accession_number = []
html = thing["primaryDocument"]
for number in thing["accessionNumber"]:
    accession_number.append(number.replace("-",""))

url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number[0]}/{html[0]}"

response = requests.get(url, headers=headers)
html_content = response.text

# with open("file.html", 'w') as f:
#     f.write(str(html_content))
# print(response)

l = html_content.split("CONSOLIDATED SCHEDULE OF INVESTMENTS</span>")


tables = []
df = pd.DataFrame()
for table_text in l[1:]:
    

    values = []
    soup = BeautifulSoup(table_text, 'html.parser')
    table = soup.find('table')
    row_num = 0

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        row_data = {}
        for col in columns:
            cell_text = col.get_text(strip=True)
            if cell_text == "":
                continue
            column_index = len(row_data) + 1
            row_data[f'col{column_index}'] = cell_text
        values.append(row_data)

    # for row in table.find_all('tr'):
    #     columns = row.find_all('td')
    #     for col in columns:
    #         cell_text = col.get_text(strip=True)
    #             # print("Gotcha")
    #         if cell_text == "":
    #             continue
    #         values.append(cell_text + " ")

    # with open("flkj.html", "w") as f:
    #     f.write(str(table))
    df_to_append = pd.DataFrame(values)
    df = pd.concat([df, df_to_append], ignore_index=True)

df.to_csv("Newtest.csv")

    

    #         column_index = len(row_data) + 1
    #         row_data[f'col{column_index}'] = cell_text
    #     values.append(row_data)
    # tables.append(values)  
            # values = [{"col1":"val1","col2":"val1"},{"col1" :"val2","col2":"val2"}]
            # >>> df = pd.DataFrame(values)
            # >>> df
            # col1  col2
            # 0  val1  val1
            # 1  val2  val2
        
    # break

    
            
            




# values = [
#     {"col1": value1, "col2", value2, etc.} # each td -> "colx": valuex
# ]

# for element in soup.find_all(attrs={'style': True}):
#     element.attrs['style'] = ''
# tables = soup.find_all('table')
# new_soup = BeautifulSoup(tables[9], 'html.parser')
# ix_elements = soup.find_all('ix:nonfraction')

# xbrl_content = '\n'.join(str(element) for element in ix_elements)

# Create an IXBRL object to parse the XBRL content


# # Extract data from parsed XBRL content
# data = []
# for element in xbrl.data:
#     if element.name == "us-gaap:RealizedAndUnrealizedGainLossInvestmentDerivativeAndForeignCurrencyTransactionPriceChangeOperatingAfterTax":
#         data.append(element.value)

 
# with open("testie.txt", "w") as f:
#     f.write(str(data))

# xbrl = IXBRL("testtable.xml")

# df = pd.read_html(tables[8])


# df.to_csv("table.csv")



# thing.to_csv("blingoblongo.csv")

# https://www.sec.gov/Archives/edgar/data/1287750/000128775023000036/arcc-20230630.htm