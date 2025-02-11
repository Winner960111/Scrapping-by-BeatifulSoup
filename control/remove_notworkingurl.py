from pyairtable import Table
import pandas as pd
import requests, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

# Airtable API credentials
BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY")

# Table names
TABLE_NAME = os.getenv("TABLE_NAME")  # Table linked to Table1

# Field name in Table2 that contains the linked record ID from Table1

db = pd.read_excel("./Whop Table.xlsx")
# print(db.iloc[0]['Community Name'])

"""Fetches data from Table1 based on a record ID."""
try:
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME)
    records = table.all()
    k = 0
    for record in records:
        try:
            k +=1
            # print(f"------{k}------")
            link = record['fields']['Whop Link']
            print(link)
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
            }
            page = requests.get(link, headers=headers)
            if page.status_code == 200:
                page_contents = page.text
                soup = BeautifulSoup(page.text, 'html.parser')
                try:
                    text = soup.find('h2', class_='fui-Heading mt-2 max-w-[380px] text-balance text-center fui-r-size-7 fui-r-weight-bold').text.strip()
                except Exception as e:
                    text = ""
                if text == "":
                    try:
                        response = table.delete(record['id'])
                        print(f"Record {record['fields']['Whop Link']} deleted successfully: {response}")
                    except Exception as e:
                        print(f"Error deleting record {record['fields']['Whop Link']}: {e}")
                    
            else:
                continue
        except Exception as e:
            print("this is error--->", e)
            pass

except Exception as e:
    print(f"Error fetching data from Table1: {e}")
