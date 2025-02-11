from pyairtable import Table
import os
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Airtable API credentials
BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY")

# Table names
TABLE1_NAME = "tbl1NOKv4Lhc2D8jt"  # Original "Community Name" table
TABLE2_NAME = "tblvUOiIOBlutJBP2"  # Table linked to Table1
TABLE3_NAME = "tbllSCkJsMFRLKBl5"

"""Fetches data from Table1 based on a record ID."""
try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE2_NAME)
    table3 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE3_NAME)
    records1 = table1.all() #primary table
    records2 = table2.all() #faq table
    records3 = table3.all() #communities table

    for record1 in records1:
        id = record1['fields']['Community Name']
        community_name = table3.get(id[0])['fields']['Community Name'].lower().replace(" ", "")
        matching_youget = []
        for record2 in records2:
            try:
                whop_community = record2['fields']['Whop Community']
                faq_id = record2['id']
                temp = whop_community.lower().replace(" ", "")
                if community_name == temp[0:len(community_name)]:
                    matching_youget.append(faq_id)
            except Exception as e:
                print(f"Error processing record: {e}")
                continue
                
        if matching_youget:
            record_data = {
                "What You'll Get_Whop": matching_youget,
            }
        try:
            response = table2.update(record1['id'], record_data)
            print(f"Record updated successfully: {response}")
        except Exception as e:
            print(f"Error creating record: {e}")
            pass
except Exception as e:
    print(f"Error fetching data from Table: {e}")
