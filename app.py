import csv

header = ["Record ID","Get Name","Get content","Whop Community Name"]
with open("Whop you-get.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
