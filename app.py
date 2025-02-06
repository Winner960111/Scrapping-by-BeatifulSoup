# import csv

# header = ["Record ID",
# "Whop Link",
# "Community Name",
# "Trading Mentor(s)",
# "Main Whop Page Image",
# "Other Page Images",
# "Whop Sub-Category",
# "Whop Page Header Text",
# "Whop Page Sub-header Text",
# "Who Is This For",
# "What You'll Get",
# "Number of Whop Reviews",
# "Whop Ranking",
# "About This Seller/Mentor Bio",
# "X Link",
# "YouTube Link",
# "Instagram Link",
# "Facebook Link",
# "Discord Link",
# "Tik Tok Link",
# "Telegram Link",
# "Community Website (from Community Name)",
# "Linkedin Link",
# "Whop FAQs",
# "Whop Reviews",
# "# of Community Members",
# "Joined Date",
# "Language",
# "Affiliate Percentage"]
# with open("Whop Table.csv", "a", encoding="utf-8", newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(header)
import csv
with open("Whop Reviews-Grid view.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
   