from pyairtable import Table
import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Airtable API credentials
BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY")

db = pd.read_excel("Whop Table.xlsx")
# Table names
TABLE1_NAME = "tbl1NOKv4Lhc2D8jt"  # primary table

"""Fetches data from Table1 based on a record ID."""
try:
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    records = table.all() #primary table
    num = 0
    for record in records:
        num += 1
        print(f"--------------------{num}------------------")
        # if num > 1000:
        #     exit()
        length = 0
        try:
            length = len(record['fields']['Unique Record ID'])
        except:
            table.delete(record['id'])
            print(f"deleted------------{num}")
            pass

        if length != 0:
            continue

        # for i in range(0, 4171):
        #     if record['fields']['Whop Link'] == db.iloc[i]['Whop Link']:
        #         data = {
        #             "Unique Record ID": db.iloc[i]['Record ID']
        #         }
        #         try:
        #             table.update(record['id'], data)
        #             print(f"Successfully updated-------{num}")
        #             break
        #         except Exception as e:
        #             print("error", e)
        #             pass
except Exception as e:
    print(f"Error fetching data from Table: {e}")
