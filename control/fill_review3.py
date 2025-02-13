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
TABLE1_NAME = "tbl1NOKv4Lhc2D8jt"  # Primay Whop table
TABLE2_NAME = "tbl7DG24ddGYLjHZL"  # FAQ Whop table

"""Fetches data from Table1 based on a record ID."""
try:
    table1 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE1_NAME)
    table2 = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE2_NAME)
    records1 = table1.all() #primary table
    records2 = table2.all() #faq table
    k = 0
    for record1 in records1:
        k += 1
        if k < 3000:
            continue
        id = record1['fields']['Unique Record ID']
        matching_review = []
        for record2 in records2:
            try:
                faq_uuid = record2['fields']['Record ID']
                faq_id = record2['id']
                if id == faq_uuid:
                    matching_review.append(faq_id)
            except Exception as e:
                print(f"Error processing record: {e}")
                continue
                
        if not matching_review:
            continue
        record_data = {
                "Reviews_Whop": matching_review,
            }

        try:
            response = table1.update(record1['id'], record_data)
            print(f"Record updated successfully")
        except Exception as e:
            print(f"Error creating record: {e}")
            pass
        print(f"---------------{k}---------------")
except Exception as e:
    print(f"Error fetching data from Table: {e}")
