import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://www.alphaquery.com/stock/TSLA/earnings-history'

res = requests.get(url)

scraped_html = BeautifulSoup(res.text, 'html')
table = scraped_html.find('table')
print(table)

header_row = table.find_all('th')
headers = [th.text.strip() for th in header_row]
print(headers)

earnings_df = pd.DataFrame(columns=headers)

rows = table.find_all('tr')
print(rows)
for row in rows[1:]:
    cells = row.find_all('td')
    data = [cell.text.strip() for cell in cells]
    print(data)
    df_len = len(earnings_df)
    earnings_df.loc[df_len] = data

earnings_df[['Estimated EPS', 'Actual EPS']] = earnings_df[['Estimated EPS', 'Actual EPS']].applymap(lambda x:float(x.replace('$', '')))

print(earnings_df)
print(earnings_df.info(), earnings_df.describe())
    
# Connect to sqlite db

conn = sqlite3.connect('earnings.db')
cursor_obj = conn.cursor()

earnings_df.to_sql("tesla_earnings", conn, if_exists='replace')

conn.close()