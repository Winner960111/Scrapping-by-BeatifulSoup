from pyairtable import Table
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
API_KEY = os.getenv("API_KEY") 

TABLE_NAME = "tbl1NOKv4Lhc2D8jt"

db = pd.read_excel("./add.xlsx")

try:
    table = Table(api_key=API_KEY, base_id=BASE_ID, table_name=TABLE_NAME)
    records = table.all()
    k = 0
    flag = False
    for record in records:
        k += 1
        # if k < 355:
        #     continue
        try:
                
            table_link = record['fields']['Whop Link']
            for i in range(0, 4):
                
                if table_link == db.iloc[i]['Whop Link']:
                    flag = True
                    if pd.isna(db.iloc[i]['Main Whop Page Image']):
                        item1 = None
                    else:
                        item1 = db.iloc[i]['Main Whop Page Image']
                    if pd.isna(db.iloc[i]['Other Page Images']):
                        item2 = None
                    else:
                        item2 = db.iloc[i]['Other Page Images']
                    if pd.isna(db.iloc[i]['Whop Page Header Text']):
                        item3 = None
                    else:
                        item3 = db.iloc[i]['Whop Page Header Text']
                    if pd.isna(db.iloc[i]['Whop Page Sub-header Text']):
                        item4 = None
                    else:
                        item4 = db.iloc[i]['Whop Page Sub-header Text']
                    if pd.isna(db.iloc[i]['Number of Whop Reviews']):
                        item5 = None
                    else:
                        item5 = db.iloc[i]['Number of Whop Reviews']
                    if pd.isna(db.iloc[i]['Whop review value']):
                        item6 = None 
                    else:
                        item6 = db.iloc[i]['Whop review value']

                    if pd.isna(db.iloc[i]['Whop Ranking']):
                        item7 = None
                    else:
                        item7 = db.iloc[i]['Whop Ranking']
                        
                    if pd.isna(db.iloc[i]['About This Seller/Mentor Bio']):
                        item8 = None
                    else:
                        item8 = db.iloc[i]['About This Seller/Mentor Bio']
                    if pd.isna(db.iloc[i]['X Link']):
                        item9 = None
                    else:
                        item9 = db.iloc[i]['X Link']
                    if pd.isna(db.iloc[i]['YouTube Link']):
                        item10 = None
                    else:
                        item10 = db.iloc[i]['YouTube Link']
                    if pd.isna(db.iloc[i]['Facebook Link']):
                        item11 = None
                    else:
                        item11 = db.iloc[i]['Facebook Link']
                    if pd.isna(db.iloc[i]['Instagram Link']):
                        item12 = None
                    else:
                        item12 = db.iloc[i]['Instagram Link']
                    if pd.isna(db.iloc[i]['Discord Link']):
                        item13 = None
                    else:
                        item13 = db.iloc[i]['Discord Link']
                    if pd.isna(db.iloc[i]['Tik Tok Link']):
                        item14 = None
                    else:
                        item14 = db.iloc[i]['Tik Tok Link']
                    if pd.isna(db.iloc[i]['Telegram Link']):
                        item15 = None
                    else:
                        item15 = db.iloc[i]['Telegram Link']
                    if pd.isna(db.iloc[i]['Linkedin Link']):
                        item16 = None
                    else:
                        item16 = db.iloc[i]['Linkedin Link']
                    if pd.isna(db.iloc[i]['Community Website (from Community Name)']):
                        item17 = None
                    else:
                        item17 = db.iloc[i]['Community Website (from Community Name)']
                    if pd.isna(db.iloc[i]['# of Community Members']):
                        item18 = None
                    else:
                        try:
                            item18 = int(db.iloc[i]['# of Community Members'])
                        except:
                            item18 = None
                    if pd.isna(db.iloc[i]['Joined Date']):
                        item19 = None
                    else:
                        item19 = db.iloc[i]['Joined Date']
                    if pd.isna(db.iloc[i]['Affiliate Percentage']):
                        item20 = None
                    else:
                        item20 = db.iloc[i]['Affiliate Percentage']

                    new_record_data = {
                        "Main Whop Page Image": item1,
                        "Other Page Images": item2,
                        "Whop Page Header Text": item3,
                        "Whop Page Sub-header Text": item4,
                        "Number of Whop Reviews": item5,
                        "Average Review value": item6,
                        "Whop Ranking": item7,
                        "About This Seller/Mentor Bio": item8,
                        "X Link": item9,
                        "YouTube Link": item10,
                        "Facebook Link": item11,
                        "Instagram Link": item12,
                        "Discord Link": item13,
                        "Tik Tok Link": item14,
                        "Telegram Link": item15,
                        "Linkedin Link": item16,
                        "Website URL": item17,
                        "# of Community Members": item18,
                        "Joined Date": str(item19),
                        "Affiliate Percentage": item20
                    }

                    try:
                        response = table.update(record['id'], new_record_data)
                        print(f"Record updated successfully")
                    except Exception as e:
                        print(f"Error creating record: {e}")
                    break
                else:
                    flag = False
            if flag == False:
                print(f"--------Don't match---{k}----")
        except:
            pass
except Exception as e:
    print(f"Error fetching data from Table1: {e}")
