# import csv

# header = ['Record ID', 'Get Name', 'Get content', 'Whop Community Name']
# with open("Whop You Get-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(header)

import uuid

# Generate a UUID version 1
uuid1 = uuid.uuid1()
print(f"UUID version 1: {uuid1}")

uuid2 = uuid.uuid1()
print(f"UUID version 1: {uuid2}")