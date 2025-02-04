import requests, csv
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
    data = {
        'record_id': "",
        'link':"",
        'main_img':"",
        'other_imgs':"",
        'com_name':"",
        'whop_header':"",
        'whop_subheader':"",
        'member_cnt':"",
        'whop_rank' : "",
        'whop_review_ctn' : "",

    }
    salary = item.select_one('span.h-max.rounded-full.fui-r-size-1.fui-variant-soft').text.strip()
    link = "https://whop.com" + item.select_one('a').get('href')
    if salary == "Free":
        continue
    data['link'] = link
    
    item_page_contents = get_page_contents(link)
    if item_page_contents is None:
        print("Failed to retrieve page content.")
        exit()
    item_soup = BeautifulSoup(item_page_contents, 'html.parser')
    # with open("item.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())
    imgs = item_soup.select("img.h-full.w-full.object-contain.object-center")
    main_img_flag = False
    for img in imgs:
        if main_img_flag:
            data['other_imgs'] += img.get('src') + ", "
        else:
            data['main_img'] = img.get('src')
            main_img_flag = True

    com_name = item_soup.find('h1', class_='fui-Heading font-[600] fui-r-size-3 fui-r-weight-bold').text.strip()
    data['com_name'] = com_name
    whop_header = item_soup.find('h2', class_='fui-Heading mt-2 max-w-[380px] text-balance text-center fui-r-size-7 fui-r-weight-bold').text.strip()
    data['whop_header'] = whop_header
    whop_subheader = item_soup.find('p', class_='fui-Text mt-2 max-w-[380px] text-pretty text-center fui-r-size-3 fui-r-weight-regular').text.strip()
    data['whop_subheader'] = whop_subheader
    try:
        member_cnt = item_soup.find('span', class_='fui-Text fui-r-size-3 fui-r-weight-bold').text.strip()
    except:
        member_cnt = ""
    try:
        rank_review = item_soup.find('span', class_='fui-Text text-amber-a10 fui-r-size-1 fui-r-weight-medium').text.strip()
        whop_rank = rank_review.split(" ")[0]
        whop_review_ctn = rank_review.split(" ")[2].split("(")[1].split(")")[0]
    except:
        whop_rank = ""
        whop_review_ctn = ""
    data['whop_rank'] = whop_rank
    data['whop_review_ctn'] = whop_review_ctn

    # Extraction offer information
    try:
        offers = item_soup.select("li.bg-panel-solid.border-gray-a3.flex.h-full.flex-col.rounded-2xl.border.shadow-md")
        for offer in offers:
            offer_info = {
                'record_id':data['record_id'],
                'offer_name':"",
                'offer_type':"",
                'offer_details':"",
                'offer_price':"",
                'community_name':data['com_name']
            }
            offer_name = offer.find('a').find('span', class_='fui-Text fui-r-size-5 fui-r-weight-bold').text.strip()
            offer_info['offer_name'] = offer_name
            offer_type = offer.find('a').find('div', class_='flex flex-col').find('span', class_='fui-Text text-gray-10 mt-3 fui-r-size-3').text.strip()
            offer_info['offer_type'] = offer_type
            try:
                offer_price = offer.find('a').find('div', class_='flex flex-col').find('span', class_='flex flex-wrap items-center gap-1').find('span').text.strip()
                offer_info['offer_price'] = offer_price
            except:
                pass
            try:
                offer_details = offer.find('a').find('ul').find_all('li')
                for detail in offer_details:
                    offer_detail = detail.find('span', class_='fui-Text min-w-0 break-words fui-r-size-3 fui-r-weight-medium').text.strip()
                    offer_info['offer_details'] += "-" + offer_detail + ",   "
            except:
                pass
            with open("Whop Offers-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(offer_info.values())
    except Exception as e:
        print(e)
        pass
    
    # End offer information

    # Extraction Review information
    try:
        reviews = item_soup.find('ul', class_='mt-[22px] flex flex-col gap-4 @2xl:grid @2xl:mt-6 grid-cols-2').find_all('li')
        for review in reviews:
            review_info = {
                'record_id':data['record_id'],
                'review_name':"",
                'review':"",
                'review_date':"",
                'community_name':data['com_name']
            }
            try:
                review_name = review.find('span', class_='fui-Text line-clamp-1 cursor-pointer text-left fui-r-size-3 fui-r-weight-medium').text.strip()
                review_info['review_name'] = review_name
            except:
                pass

            review_txt = review.find('p', class_='fui-Text whitespace-pre-line fui-r-size-3 fui-r-weight-regular').text.strip()
            review_info['review'] = review_txt
            review_date = review.find('span', class_= 'fui-Text fui-r-size-2').text.strip()
            review_info['review_date'] = review_date
            with open("Whop Reviews-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(review_info.values())

    except Exception as e:
        print(e)
        pass
    # End review information

    
    # print(f"{whop_header},    {whop_subheader}")