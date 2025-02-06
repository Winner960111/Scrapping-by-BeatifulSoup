import requests, csv, re, json, uuid
from bs4 import BeautifulSoup

def get_page_contents(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    if page.status_code == 200:
        return page.text
    return None

for i in range(0, 972):
        
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
        record_id = uuid.uuid4()
        data = {
            'record_id': record_id,
            'link':"",
            'com_name':"",
            'trading_mentor':"",
            'main_img':"",
            'other_imgs':"",
            'Whop_sub_category':"",
            'whop_header':"",
            'whop_subheader':"",
            'who_id':record_id,
            'you_get_id':record_id,
            'whop_review_ctn' : "",
            'whop_rank' : "",
            'bio':"",
            'x_link':"",
            'youtube_link':"",
            'instagram_link':"",
            'facebook_link':"",
            'discord_link':"",
            'tiktok_link':"",
            'telegram_link':"",
            'community_link':"",
            'linkedin_link':"",
            'faq_id':record_id,
            'review_id':record_id,
            'member_cnt':"",
            'joined_date':"",
            'language':'English',
            'affiliate_percentage':"",
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
        data['member_cnt'] = member_cnt

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
                    'record_id':data['review_id'],
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

        # Extraction you get information

        you_gets = item_soup.find_all('li', class_='@2xl:p-6 @2xl:rounded-3xl flex items-center gap-4 @2xl:bg-gray-2')
        for you_get in you_gets:
            you_get_info = {
                'record_id':data['you_get_id'], 
                'you_get_name':"",
                'you_get_details':"",
                'community_name':data['com_name']
            }
            you_get_name = you_get.find('span', class_='fui-Text line-clamp-2 fui-r-weight-bold').text.strip()
            you_get_info['you_get_name'] = you_get_name
            you_get_details = you_get.find('span', class_='fui-Text text-gray-10 line-clamp-2 text-[15px]').text.strip()
            you_get_info['you_get_details'] = you_get_details
            with open("Whop You Get-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(you_get_info.values())

        trading_mentor = item_soup.find('span', class_='fui-Text [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-7 fui-r-weight-bold').text.strip()
        data['trading_mentor'] = trading_mentor

        joined_date_temp = item_soup.find('span', class_='fui-Text text-gray-10 [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-2').text.strip()
        joined_date = joined_date_temp.split("Joined")[1].strip()
        data['joined_date'] = joined_date

        # Extraction social links
        try:
            social_links = item_soup.find_all('a', class_='hover:bg-gray-a3 flex items-center justify-between rounded-full p-2 [[data-blend]_&]:mix-blend-plus-lighter')
            for link in social_links:
                social_link = link.get('href')
                social_name = link.get('aria-label').split("/")[0]
                match social_name:
                    case "x.com":
                        data['x_link'] = social_link
                    case "youtube.com":
                        data['youtube_link'] = social_link
                    case "instagram.com":
                        data['instagram_link'] = social_link
                    case "facebook.com":
                        data['facebook_link'] = social_link
                    case "tiktok.com":
                        data['tiktok_link'] = social_link
                    case "linkedin.com":
                        data['linkedin_link'] = social_link
                    case "discord.com":
                        data['discord_link'] = social_link
                    case "telegram.org":
                        data['telegram_link'] = social_link
                    case _:
                        data['community_link'] = social_link
        except Exception as e:
            print(e)
            pass
        # End Extraction social links

        try:
            bio = item_soup.find('p', class_='fui-Text max-w-[478px] text-pretty text-center')
            data['bio'] = bio
        except Exception as e:
            print(e)
            pass

        # Extraction who is this for
        try:
            for_who = item_soup.find_all('li', class_='flex h-full w-full flex-col items-center justify-start gap-2 rounded-2xl px-6 py-8 bg-gray-2')
            for who in for_who:
                who_info = {
                    'record_id':data['who_id'],
                    'who_name':"",
                    'who_content':"",
                    'community_name':data['com_name']
                }
                try:
                    who_info['who_name'] = who.find('span', class_='fui-Text w-full min-w-0 text-balance break-words text-center fui-r-weight-bold').text.strip()
                    who_info['who_content'] = who.find('span', class_='fui-Text text-gray-10 w-full min-w-0 text-pretty break-words text-center fui-r-size-2').text.strip()
                    with open("Whop Who-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(who_info.values())
                except Exception as e:
                    print(e)
                    pass

        except Exception as e:
            print(e)
            pass

        # End Extraction who is this for
        
        # Extraction FAQs
        
        script_tag = item_soup.find_all('script')
        for script in script_tag:
            script_text = script.text.strip()
            if 'self.__next_f.push([1,"11:[[' in script_text:
                script_text = script_text.replace('\"', "").replace("\\", "")
                pattern = r'faq:\[(.*?)\]'
                match = re.search(pattern, script_text, re.DOTALL)
                # Extract questions
                questions = re.findall(r'question:(.*?),', match.group(1))

                # Extract answers
                answers = re.findall(r'answer:(.*?)[,}]', match.group(1))

                # Print Q&A pairs
                for q, a in zip(questions, answers):
                    faq_info = {
                        'record_id':data['faq_id'],
                        'community_name':data['com_name'],
                        'question':"",
                        'answer':"",
                    }
                    faq_info['question'] = q.strip()
                    faq_info['answer'] = a.strip()
                    with open("Whop FAQs-Grid view.csv", "a", encoding="utf-8", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(faq_info.values())

        # End Extraction FAQs
        
        try:
            affiliate_percentage = item_soup.find('span', class_='bg-panel-solid border-gray-a3 dark:bg-gray-a3 dark:border-gray-a5 text-success-11 -mt-[13px] flex h-10 origin-center -rotate-[2deg] items-center rounded-xl border px-3 font-[600] dark:border dark:outline dark:outline-[0.5px] dark:outline-black dark:backdrop-blur-md dark:backdrop-saturate-150').text.strip()
        except Exception as e:
            print(e)
            pass

        data['affiliate_percentage'] = affiliate_percentage
        
        with open('Whop Table.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.values())


        