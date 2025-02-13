from pyairtable import Table
import pandas as pd

from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

# Table names
TABLE_NAME = "tblx0IegM2Yr3Xy0W"  # "Mentor" table

try:
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME)
    records = table.all()
    compare = ""
    for index, record in enumerate(records):
        try:
            if record['fields']['Whop Community'] == compare:
                continue
            compare = record['fields']['Whop Community']
            
            flag = False
            for ind, item in enumerate(records):
                if ind < index:
                    continue
                if compare != item['fields']['Whop Community']:
                    flag = True
                if flag == True and compare == item['fields']['Whop Community']:
                    print(f"Duplicate found: {compare}")
                    table.delete(item['id'])
                    print(f"Deleted record with ID: {item['id']}")
            print(f"-------------{index}-----------")
        except Exception as e:
            print("here---->",e)
            pass
except Exception as e:
    print(f"Error fetching data from Table1: {e}")
