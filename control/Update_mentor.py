from pyairtable import Table
import pandas as pd

from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

# Table names
TABLE1_NAME = "tbl5y34xVeXTl00vM"  # "Mentor" table
TABLE2_NAME = "tbl1NOKv4Lhc2D8jt"  # "whop primary" Table1

# Field name in Table2 that contains the linked record ID from Table1
LINKED_RECORD_FIELD_NAME = "Community Name" #<-- REPLACE THIS

db = pd.read_excel("./Whop Table.xlsx")
# print(db.iloc[0]['Community Name'])

"""Fetches data from Table1 based on a record ID."""
try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE2_NAME)
    records1 = table1.all()
    records2 = table2.all()
    num = 0
    for record2 in records2:
        print(f"-------{num}---------")
        try:
            url = record2['fields']['Whop Link']
            name_id = record2['fields']['Community Name']
            for i in range(0, 478):
                if db.iloc[i]['Whop Link'] == url:
                    trader2 = db.iloc[i]['Trading Mentor(s)']
                    break
            if trader2:
                flag = False
                for record1 in records1:
                    trader1 = record1['fields']['Trader Name']
                    if trader1 == trader2:
                        flag = True
                        break
                if not flag:
                    new_record_data = {
                    "Trader Name": trader2,
                    "Community Name(s)": name_id,
                    }
                    try:
                        response = table1.create(new_record_data)
                        print(f"Record updated successfully: {response}")
                    except Exception as e:
                        print(f"Error creating record: {e}")
                        pass
            num += 1
        except Exception as e:
            print("Here---->", e)
            pass
except Exception as e:
    print(f"Error fetching data from Table1: {e}")
