from pyairtable import Table
import pandas as pd

from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

# Table names
TABLE1_NAME = "tbl5y34xVeXTl00vM"  # "Mentor" table
TABLE2_NAME = "tbllSCkJsMFRLKBl5"  # "communities" Table1
db = pd.read_excel("./Whop Table.xlsx")

try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE2_NAME)
    records1 = table1.all()
    records2 = table2.all()
    num = 0
    for record1 in records1:
        num += 1
        if num < 2805:
            continue
        mentor = record1['fields']['Trader Name']
        for i in range(0, 3883):
            if mentor == db.iloc[i]['Trading Mentor(s)']:
                table2_community_name = str(db.iloc[i]['Community Name'])
                break
        if table2_community_name == "":
            continue
        
        for record2 in records2:
            if table2_community_name == record2['fields']['Community Name']:
                new_record_data = {
                    "Community Name(s)": [record2['id']],
                }
                try:
                    response = table1.update(record1['id'], new_record_data)
                    print(f"Record updated successfully")
                except Exception as e:
                    print(f"Error creating record: {e}")
                break
        print(f"---------------{num}---------------")
except Exception as e:
    print(f"Error fetching data from Table1: {e}")
