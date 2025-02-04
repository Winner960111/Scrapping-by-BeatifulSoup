import requests
from bs4 import BeautifulSoup

def get_page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return page.text
    return None

# for i in range(0, 965):
    
url = f"https://whop.com/discover/c/trading/p/0/" # Replace with the URL you want to scrape
page_contents = get_page_contents(url)
if page_contents is None:
    print("Failed to retrieve page content.")
    exit()

soup = BeautifulSoup(page_contents, 'html.parser')
# with open("output.html", "w", encoding="utf-8") as f:
#     f.write(soup.prettify())
items = soup.select("div.rounded-xl.border.border-gray-a3")
for item in items:
    salary = item.select_one('span.h-max.rounded-full.fui-r-size-1.fui-variant-soft').text.strip()
    link = "https://whop.com" + item.select_one('a').get('href')

    if salary == "Free":
        continue
    
    item_page_contents = get_page_contents(link)
    if item_page_contents is None:
        print("Failed to retrieve page content.")
        exit()
    soup = BeautifulSoup(item_page_contents, 'html.parser')
    # with open("item.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())
    
