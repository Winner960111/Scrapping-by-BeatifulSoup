from pyairtable import Table
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

db = pd.read_excel("./Whop Table.xlsx")

TABLE_NAME1 = "tbllSCkJsMFRLKBl5" # communities table
TABLE_NAME2 = "tbl1NOKv4Lhc2D8jt" # Primary table

try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME1)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME2)
    records1 = table1.all()
    records2 = table2.all()
    k = 0
    for record2 in records2:
        k += 1
        if k < 809:
            continue
        table2_link = record2['fields']['Whop Link']
        table2_community_name = ""
        for i in range(0, 3883):
            if table2_link == db.iloc[i]['Whop Link']:
                table2_community_name = str(db.iloc[i]['Community Name'])
                break
        
        if table2_community_name == "":
            continue

        for record1 in records1:
            if table2_community_name == record1['fields']['Community Name']:
                new_record_data = {
                    "Community Name": [record1['id']],
                }
                try:
                    response = table2.update(record2['id'], new_record_data)
                    print(f"Record updated successfully")
                except Exception as e:
                    print(f"Error creating record: {e}")
                break
    
        print(f"---------------{k}---------------")

except Exception as e:
    print(f"Error fetching data from Table1: {e}")
