import requests, csv, re, json, uuid
from bs4 import BeautifulSoup
import pandas as pd
def get_page_contents(url):
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

    page = requests.get(url, headers=headers)
    with open("output.html", "w", encoding="utf-8-sig") as f:
        f.write(page.text)
    if page.status_code == 200:
        return page.text
    return None

df = pd.read_excel("source.xlsx")
items = df.values.tolist()
k=0
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
        'whop_review_value' : "",
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
    # salary = item.select_one('span.h-max.rounded-full.fui-r-size-1.fui-variant-soft').text.strip()
    # link = "https://whop.com" + item.select_one('a').get('href')
    # if salary == "Free":
    #     continue
    data['link'] = item[0]
    # if item[0] == "https://whop.com/marketplace/atumtrades/":
    #     continue
    k += 1
    print(k,"---------", item[0])
    try:
        item_page_contents = get_page_contents(item[0])
        item_soup = BeautifulSoup(item_page_contents, 'html.parser')
    except:
        print("Failed to retrieve page content.")
        continue
    # with open("item.html", "w", encoding="utf-8-sig") as f:
    #     f.write(soup.prettify())
    try:

        imgs = item_soup.find_all('img', class_='h-full w-full object-contain object-center')
        main_img_flag = False
        for img in imgs:
            if main_img_flag:
                data['other_imgs'] += img.get('src') + ", "
            else:
                data['main_img'] = img.get('src')
                main_img_flag = True
    except:
        pass
    try:
        com_name = item_soup.find('h1', class_='fui-Heading font-[600] fui-r-size-3 fui-r-weight-bold').text.strip()
        data['com_name'] = com_name
    except:
        pass
    try:
        whop_header = item_soup.find('h2', class_='fui-Heading mt-2 max-w-[380px] text-balance text-center fui-r-size-7 fui-r-weight-bold').text.strip()
        data['whop_header'] = whop_header
        whop_subheader = item_soup.find('p', class_='fui-Text mt-2 max-w-[380px] text-pretty text-center fui-r-size-3 fui-r-weight-regular').text.strip()
        data['whop_subheader'] = whop_subheader
    except Exception as e:
        # print(f"header or subheader--->: {e}")
        # print(data['link'])
        # print("\n")
        pass

    try:
        member_cnt = item_soup.find('span', class_='fui-Text fui-r-size-3 fui-r-weight-bold').text.strip()
        if member_cnt:
            member_cnt = member_cnt.split(" ")[1]  
            data['member_cnt'] = member_cnt
    except Exception as e:
        # print(f"member count-->: {e}")
        # print(data['link'])
        # print("\n")
        pass

    try:
        rank_review = item_soup.find('span', class_='fui-Text text-amber-a10 fui-r-size-1 fui-r-weight-medium').text.strip()
        whop_review_value = rank_review.split(" ")[0]
        whop_review_ctn = rank_review.split(" ")[2].split("(")[1].split(")")[0]
        data['whop_review_value'] = whop_review_value
        data['whop_review_ctn'] = whop_review_ctn
    except Exception as e:
        # print(f"rank or review ctn---->: {e}")
        # print(data['link'])
        # print("\n")
        pass
    
    try:
        ranking = item_soup.find('span', class_='fui-Badge @2xl:mb-11 mb-8 h-auto gap-1.5 rounded-full px-2.5 py-1.5 font-medium fui-r-size-1 fui-variant-soft').text.strip()
        data['whop_rank'] = ranking.split('#')[1].split(" ")[0]
    except Exception as e:
        # print(f"ranking---->: {e}")
        # print(data['link'])
        # print("\n")
        pass

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
            except Exception as e:
                # print(f"offer price--->: {e}")
                # print(data['link'])
                # print("\n")
                pass
            try:
                offer_details = offer.find('a').find('ul').find_all('li')
                for detail in offer_details:
                    offer_detail = detail.find('span', class_='fui-Text min-w-0 break-words fui-r-size-3 fui-r-weight-medium').text.strip()
                    offer_info['offer_details'] += "-" + offer_detail + ",   "
            except Exception as e:
                # print(f"offer detail--->: {e}")
                # print(data['link'])
                # print("\n")
                pass
            with open("Whop Offers.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(offer_info.values())
    except Exception as e:
        # print(f"Offer item --->: {e}")
        # print(data['link'])
        # print("\n")
        pass
    
    # End offer information

    # Extraction Review information
    try:
        script_tag = item_soup.find_all('script')
        for script in script_tag:
            script_text = script.text.strip()
            if 'self.__next_f.push([1,"11:[[' in script_text:
                script_text = script_text.replace('\"', "").replace("\\", "")
                reviews_pattern = r'featuredReviews:\[.*?\}]'
                match = re.search(reviews_pattern, script_text, re.DOTALL)
                # Extract individual review data
                if match:
                    reviews = match.group(0)
                    users = re.findall(r'name:(.*?),', match.group(0))
                    review = re.findall(r'description:(.*?),joinedAt', match.group(0))
                    # Print Q&A pairs
                    dates_ul = item_soup.find('ul', class_='mt-[22px] flex flex-col gap-4 @2xl:grid @2xl:mt-6 grid-cols-2')
                    dates = dates_ul.find_all('span', class_='fui-Text fui-r-size-2')
                    for u, r, d in zip(users, review, dates):
                        review_info = {
                            'record_id':data['review_id'],
                            'review_name':"",
                            'review':"",
                            'review_date':"",
                            'community_name':data['com_name']
                        }
                        d1 = d.text.strip().split(" ")[1]
                        d2 = d.text.strip().split(" ")[2]
                        d3 = d.text.strip().split(" ")[3].split(",")[0]
                        review_info['review_date'] = d1 + " " + d2 + " " + d3
                        review_info['review_name'] = u.strip()
                        review_info['review'] = r.strip()
                        with open("Whop Reviews.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(review_info.values())

    except Exception as e:
        # print(f"Script tag for review--->: {e}")
        # print(data['link'])
        # print("\n")
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
        try:
            you_get_name = you_get.find('span', class_='fui-Text line-clamp-2 fui-r-weight-bold').text.strip()
            you_get_info['you_get_name'] = you_get_name
            you_get_details = you_get.find('span', class_='fui-Text text-gray-10 line-clamp-2 text-[15px]').text.strip()
            you_get_info['you_get_details'] = you_get_details
            with open("Whop you-get.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(you_get_info.values())
        except Exception as e:
            # print(f"you_Get-->: {e}")
            # print(data['link'])
            # print("\n")
            pass

    # End you get information
    try:

        trading_mentor = item_soup.find('span', class_='fui-Text [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-7 fui-r-weight-bold').text.strip()
        data['trading_mentor'] = trading_mentor
    except Exception as e:
        # print(f"Trading mentor--->: {e}")
        # print(data['link'])
        # print("\n")
        pass
    try:

        joined_date_temp = item_soup.find('span', class_='fui-Text text-gray-10 [[data-blend]_&]:mix-blend-plus-lighter fui-r-size-2').text.strip()
        joined_date = joined_date_temp.split("Joined")[1].strip()
        data['joined_date'] = joined_date
    except Exception as e:
        # print(f"Joined date--->: {e}")
        # print(data['link'])
        # print("\n")
        pass
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
        # print(f"Social Link--->: {e}")
        # print(data['link'])
        # print("\n")
        pass
    # End Extraction social links

    try:
        bio = item_soup.select('p.fui-Text.text-pretty.text-center.fui-r-weight-bold')
        if bio:
            data['bio'] = bio[0].text.strip()
    except Exception as e:
        # print(f"bio---->: {e}")
        # print(data['link'])
        # print("\n")
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
                with open("Whop who.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(who_info.values())
            except Exception as e:
                # print(f"who info--->: {e}")
                # print(data['link'])
                # print("\n")
                pass

    except Exception as e:
        # print(f"who item---->: {e}")
        # print(data['link'])
        # print("\n")
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
                with open("Whop FAQs.csv", "a", encoding="utf-8-sig", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(faq_info.values())

    # End Extraction FAQs
    
    try:
        affiliate_percentage = item_soup.find('span', class_='bg-panel-solid border-gray-a3 dark:bg-gray-a3 dark:border-gray-a5 text-success-11 -mt-[13px] flex h-10 origin-center -rotate-[2deg] items-center rounded-xl border px-3 font-[600] dark:border dark:outline dark:outline-[0.5px] dark:outline-black dark:backdrop-blur-md dark:backdrop-saturate-150').text.strip()
    except Exception as e:
        # print(f"percent---->: {e}")
        # print(data['link'])
        # print("\n")
        pass

    data['affiliate_percentage'] = affiliate_percentage
    
    with open('Whop Table.csv', 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data.values())

# print(f"********************Scraped {i+1} pages**************************")
    