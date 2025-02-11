from pyairtable import Table
import pandas as pd

from dotenv import load_dotenv
import os
load_dotenv()

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
        table2_id = record['fields']['Community Name']
        community_name = table1.get(table2_id[0])['fields']['Community Name']
        for i in range(0, 3884):
            if community_name == db.iloc[i]['Community Name']:
                print("This is com name--->", community_name)
                print(db.iloc[i]['Whop Link'])
                new_record_data = {
                    "Whop Link": db.iloc[i]['Whop Link'], #Example field
                }
                try:
                    response = table2.update(record['id'], new_record_data)
                    print(f"Record updated successfully: {response}")
                except Exception as e:
                    print(f"Error creating record: {e}")
                break

except Exception as e:
    print(f"Error fetching data from Table1: {e}")
