from pyairtable import Table
import pandas as pd

import requests
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

def get_page_contents(url):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

    page = requests.get(url, headers=headers)
    with open("output.html", "w", encoding="utf-8-sig") as f:
        f.write(page.text)
    if page.status_code == 200:
        return page.text
    return None


BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

# Table names
TABLE1_NAME = "tbllSCkJsMFRLKBl5"  # Original "Community Name" table
TABLE2_NAME = "tbl1NOKv4Lhc2D8jt"  # Table linked to Table1

# Field name in Table2 that contains the linked record ID from Table1
LINKED_RECORD_FIELD_NAME = "Community Name" #<-- REPLACE THIS

db = pd.read_excel("./Whop Table.xlsx")
# print(db.iloc[0]['Community Name'])

"""Fetches data from Table1 based on a record ID."""
try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE2_NAME)
    records = table2.all()
    for record in records:
        try:
            table2_id = record['fields']['Community Name']
            community_name = table1.get(table2_id[0])['fields']['Community Name']
            for i in range(0, 3884):
                compare = str(db.iloc[i]['Community Name'])[0:len(community_name)]
                com1 = str(db.iloc[i]['Whop Link'])
                com2 = record['fields']['Whop Link']
                if compare == community_name and com1 != com2:
                    soup1= BeautifulSoup(get_page_contents(com1), "html.parser")
                    soup2= BeautifulSoup(get_page_contents(com2), "html.parser")
                    trading_mentor1 = soup1.find('span', class_='fui-Text [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-7 fui-r-weight-bold').text.strip()
                    trading_mentor2 = soup2.find('span', class_='fui-Text [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-7 fui-r-weight-bold').text.strip()
                    

                    if trading_mentor1 == trading_mentor2 and com1 != com2:
                        print(db.iloc[i]['Whop Link'])
                        print(record['fields']['Whop Link'])
                        print("\n")
                        new_record_data = {
                            "Whop Link": db.iloc[i]['Whop Link'], #Example field
                        }
                        try:
                            response = table2.update(record['id'], new_record_data)
                            print(f"Record updated successfully: {response}")
                        except Exception as e:
                            print(f"Error creating record: {e}")
                        break
        except:
            pass
except Exception as e:
    print(f"Error fetching data from Table1: {e}")
