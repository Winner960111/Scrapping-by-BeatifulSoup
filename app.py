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

text = get_page_contents("https://whop.com/discover/crystal-academy/")
soup = BeautifulSoup(text, 'html.parser')

with open("item.html", "w", encoding = "utf-8") as f:
    f.write(soup.prettify())