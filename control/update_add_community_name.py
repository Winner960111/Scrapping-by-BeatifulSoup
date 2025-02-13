from pyairtable import Table
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 


TABLE_NAME = "tbllSCkJsMFRLKBl5"

db = pd.read_excel("./Whop Table.xlsx")

try:
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME)
    records = table.all()
    for i in range(0, 3883):
        
        flag = False
        # if i < 1441:
        #     continue
        
        for record in records:
            table_link = record['fields']['Community Name']
            if str(db.iloc[i]['Community Name']) == table_link:
                flag = True
                break
        
        if flag == True:
            continue
        
        new_record_data = {
            "Community Name": str(db.iloc[i]['Community Name']),
        }

        try:
            response = table.create(new_record_data)
            print(f"Record updated successfully")
        except Exception as e:
            print(f"Error creating record: {e}")
            break
        print(f"---------------{i}---------------")

except Exception as e:
    print(f"Error fetching data from Table1: {e}")
