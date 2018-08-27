#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging.handlers
import time
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection


class instagramCrawlerBot():

    def __init__(self):
        print('instagramCrawlerBot _ start')

global returnedValue_naverBlog
global hereWork

hereWork = 'Instagram'

currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

#logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

#fileHandler와 StreamHandler를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C:/python_project/log/' + hereWork + '_crawlerbot_logging_' + currTime, maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#Handler를 logging에 추가
logger.addHandler(fileHandler)

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data_soup_html = bs(driver.page_source, 'html.parser')
        #print(autoScrolled_data_soup_html)
    #return bs(autoScrolled_data, 'html.parser')
    return autoScrolled_data_soup_html


def bringContentBasicData(driver, userInstaURL):

    driver.get(userInstaURL)
    autoScroller(driver)
    contentHTMLpage = bs(driver.page_source, 'html.parser')

    if contentHTMLpage.find('html', attrs={'lang':'ko'}) is not None:
        instaPage_KO = True
    else:
        print('사용자의 인스타그램 페이지 언어가 한국어가 아닙니다.')

    userInstagramTextData = {}

    try:
        try:
            # 사용자 닉네임
            user_nickName = contentHTMLpage.select(
                '#react-root > section > main > article > header > section > div:nth-of-type(1) > h1')[0].text.replace(" ", "")
            print('사용자ID:', user_nickName)
            userInstagramTextData.update({'사용자ID': user_nickName})
        except Exception as e:
            print('구조가 변경됨')

            # 사용자 닉네임
            user_nickName = contentHTMLpage.select(
                '#react-root > section > main > div > header > section > div:nth-of-type(1) > h1')[0].text.replace(" ", "")
            print('사용자ID:', user_nickName)
            userInstagramTextData.update({'사용자ID': user_nickName})

    except Exception as e:
        print('user_nickName : ', e)

    #사용자 게시한 포스트 개수
    try:
        try:
            user_postCnt = contentHTMLpage.select(
                '#react-root > section > main > article > header > section > ul > li:nth-of-type(1) > span > span')[0].text.replace(" ", "").replace(",", "")
            if instaPage_KO == True:
                if '천' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('천')[0] + '000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '백만' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('백만')[0] + '000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '천만' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('천만')[0] + '0000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '억' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('억')[0] + '000000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                else:
                    user_postCnt_int = int(user_postCnt)
                    print('user_post_count : ', user_postCnt_int, '개')
            else:
                if 'k' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('k')[0] + '000')
                    print('user_post_count : ', user_postCnt_int)
                elif 'm' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('m')[0] + '000000')
                    print('user_post_count : ', user_postCnt_int)
                elif 'b' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('b')[0] + '000000000')
                    print('user_post_count : ', user_postCnt_int)
                else:
                    user_postCnt_int = int(user_postCnt)
                    print('user_post_count : ', user_postCnt_int)

            userInstagramTextData.update({'게시글수': user_postCnt_int})
        except Exception as e:
            print('구조가 변경됨')

            user_postCnt = contentHTMLpage.select(
                '#react-root > section > main > div > header > section > ul > li:nth-of-type(1) > span > span')[
                0].text.replace(" ", "").replace(",", "")
            if instaPage_KO == True:
                if '천' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('천')[0] + '000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '백만' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('백만')[0] + '000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '천만' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('천만')[0] + '0000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                elif '억' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('억')[0] + '000000000')
                    print('user_post_count : ', user_postCnt_int, '개')
                else:
                    user_postCnt_int = int(user_postCnt)
                    print('user_post_count : ', user_postCnt_int, '개')
            else:
                if 'k' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('k')[0] + '000')
                    print('user_post_count : ', user_postCnt_int)
                elif 'm' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('m')[0] + '000000')
                    print('user_post_count : ', user_postCnt_int)
                elif 'b' in user_postCnt:
                    user_postCnt_int = int(user_postCnt.split('b')[0] + '000000000')
                    print('user_post_count : ', user_postCnt_int)
                else:
                    user_postCnt_int = int(user_postCnt)
                    print('user_post_count : ', user_postCnt_int)

            userInstagramTextData.update({'게시글수': user_postCnt_int})


    except Exception as e:
        print('user_postCnt Error : ', e)


    #사용자를 팔로우 하는 사람들의 수
    try:
        try:
            user_followerCnt = contentHTMLpage.select(
                '#react-root > section > main > article > header > section > ul > li:nth-of-type(2) > span > span')[0].text.replace(" ", "").replace(",", "").replace(".", "")
            print('user_follower_count : ', user_followerCnt)

            #user_followerCnt_int = 0

            if instaPage_KO == True:
                if '천' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('천')[0] + '000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '백만' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('백만')[0] + '000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '천만' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('천만')[0] + '0000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '억' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('억')[0] + '000000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                else:
                    user_followerCnt_int = int(user_followerCnt)
                    print('user_follower_count : ', user_followerCnt_int, '명')
            else:
                if 'k' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('k')[0] + '000')
                    print('user_follower_count : ', user_followerCnt_int)
                elif 'm' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('m')[0] + '000000')
                    print('user_follower_count : ', user_followerCnt_int)
                elif 'b' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('b')[0] + '000000000')
                    print('user_follower_count : ', user_followerCnt_int)
                else:
                    user_followerCnt_int = int(user_followerCnt)
                    print('user_follower_count : ', user_followerCnt_int)

            userInstagramTextData.update({'팔로워수': user_followerCnt_int})
        except Exception as e:
            print('구조가 변경됨')

            user_followerCnt = contentHTMLpage.select(
                '#react-root > section > main > div > header > section > ul > li:nth-of-type(2) > a > span')[
                0].text.replace(" ", "").replace(",", "").replace(".", "")
            print('user_follower_count : ', user_followerCnt)

            if instaPage_KO == True:
                if '천' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('천')[0] + '000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '백만' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('백만')[0] + '000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '천만' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('천만')[0] + '0000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                elif '억' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('억')[0] + '000000000')
                    print('user_follower_count : ', user_followerCnt_int, '명')
                else:
                    user_followerCnt_int = int(user_followerCnt)
                    print('user_follower_count : ', user_followerCnt_int, '명')
            else:
                if 'k' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('k')[0] + '000')
                    print('user_follower_count : ', user_followerCnt_int)
                elif 'm' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('m')[0] + '000000')
                    print('user_follower_count : ', user_followerCnt_int)
                elif 'b' in user_followerCnt:
                    user_followerCnt_int = int(user_followerCnt.split('b')[0] + '000000000')
                    print('user_follower_count : ', user_followerCnt_int)
                else:
                    user_followerCnt_int = int(user_followerCnt)
                    print('user_follower_count : ', user_followerCnt_int)

            userInstagramTextData.update({'팔로워수': user_followerCnt_int})
    except Exception as e:
        print('user_followerCnt Error : ', e)


    #사용자가 팔로잉하는 사람들의 수
    try:
        try:
            user_followingCnt = contentHTMLpage.select(
                '#react-root > section > main > article > header > section > ul > li:nth-of-type(3) > span > span')[0].text.replace(" ", "").replace(",", "").replace(".", "")
            print('user_following_count :', user_followingCnt)

            #user_followingCnt_int = 0

            if instaPage_KO == True:
                if '천' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('천')[0] + '000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '백만' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('백만')[0] + '000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '천만' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('천만')[0] + '0000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '억' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('억')[0] + '000000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                else:
                    user_followingCnt_int = int(user_followingCnt)
                    print('user_follower_count : ', user_followingCnt_int, '명')
            else:
                if 'k' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('k')[0] + '000')
                    print('user_follower_count : ', user_followingCnt_int)
                elif 'm' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('m')[0] + '000000')
                    print('user_follower_count : ', user_followingCnt_int)
                elif 'b' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('b')[0] + '000000000')
                    print('user_follower_count : ', user_followingCnt_int)
                else:
                    user_followingCnt_int = int(user_followingCnt)
                    print('user_follower_count : ', user_followingCnt_int)

            userInstagramTextData.update({'팔로잉수': user_followingCnt_int})

        except Exception as e:
            print('구조가 변경됨')

            user_followingCnt = contentHTMLpage.select(
                '#react-root > section > main > div > header > section > ul > li:nth-of-type(3) > a > span')[
                0].text.replace(" ", "").replace(",", "").replace(".", "")
            print('user_following_count :', user_followingCnt)

            # user_followingCnt_int = 0

            if instaPage_KO == True:
                if '천' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('천')[0] + '000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '백만' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('백만')[0] + '000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '천만' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('천만')[0] + '0000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                elif '억' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('억')[0] + '000000000')
                    print('user_follower_count : ', user_followingCnt_int, '명')
                else:
                    user_followingCnt_int = int(user_followingCnt)
                    print('user_follower_count : ', user_followingCnt_int, '명')
            else:
                if 'k' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('k')[0] + '000')
                    print('user_follower_count : ', user_followingCnt_int)
                elif 'm' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('m')[0] + '000000')
                    print('user_follower_count : ', user_followingCnt_int)
                elif 'b' in user_followingCnt:
                    user_followingCnt_int = int(user_followingCnt.split('b')[0] + '000000000')
                    print('user_follower_count : ', user_followingCnt_int)
                else:
                    user_followingCnt_int = int(user_followingCnt)
                    print('user_follower_count : ', user_followingCnt_int)

            userInstagramTextData.update({'팔로잉수': user_followingCnt_int})


    except Exception as e:
        print('user_followingCnt Error : ', e)

    userInstagramTextData_List = []
    userInstagramHashTagData = []

    #Auto Scroll 한 만큼의 텍스트를 가져다가 출력
    for imgTextLength in contentHTMLpage.find_all('img', class_='FFVAD'):
        imgTagAltText = imgTextLength['alt'].replace(".", "").replace("\n", "").replace("️", "").replace("✔️", "")
        print('@imgTagAltText->', imgTagAltText)

        imgTagAltTextArray = imgTagAltText.split(" ")
        print('@imgTagAltTextArray->', imgTagAltTextArray)

        # 여기서부터 원하는 텍스트 정보 추출 가능
        #userInstagramTextData_List.append(imgTagAltTextArray)
        userInstagramTextData_List.extend(imgTagAltTextArray)

        #print('userInstagramTextData_List :', userInstagramTextData_List)

        if '#' in imgTagAltText:
            sharpLength = 0
            for sharpLength in range(len(imgTagAltText.split('#'))):
                sharpLength = sharpLength + 1

                if sharpLength < len(imgTagAltText.split('#')):
                    print('#tag: ', imgTagAltText.split('#')[sharpLength])
                    userInstagramHashTagData.append(imgTagAltText.split('#')[sharpLength])

                else:
                    print()
                    continue
        else:
            print('#-항목이 존재하지 않습니다.')

    print('userInstagramTextData_List :', userInstagramTextData_List, len(userInstagramTextData_List))
    print('total hash tag : ', userInstagramHashTagData, len(userInstagramHashTagData))

    userInstagramTextData['게시글내단어수'] = len(userInstagramTextData_List)
    userInstagramTextData['해쉬테그수'] = len(userInstagramHashTagData)

    userInstagramTextData.update({'parsedTextData': userInstagramTextData_List })

    return userInstagramTextData

def CrawlingByInstagramCrawlBot(userURL, username, fb_pageID):
    start_time_all = time.time()

    with requests.Session() as s:

        loginURL = 'https://www.instagram.com/accounts/login/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        response = requests.get(loginURL, headers=headers)
        print(response)

        print('Auto login start.')

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        prefs = {}
        prefs['profile.default_content_setting_values.notifications'] = 2
        chrome_options.add_experimental_option('prefs', prefs)
        driver_chrome = r"C:\python_project\chromedriver.exe"

        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)
        driver.get(loginURL)

        print('driver.current_url : ', driver.current_url)
        basic_url = 'https://www.instagram.com/'

        userInstaURL = basic_url + userURL+ '/?hl=ko'

        #Crawler 호출
        instagram_returnResult = bringContentBasicData(driver, userInstaURL)
        print('return Result : ', instagram_returnResult)

        '''
        '사용자ID': 'dasolmom_',
        '게시글수': 244, 
        '팔로워수': 545000, 
        '팔로잉수': 65, 
        '게시글내단어수': '938',
        '해쉬테그수': '239',
        '''
        instagram_T_Value = 0
        instagram_C_Value = 0
        instagram_M_Value = 0

        try:
            if instagram_returnResult['사용자ID'] is not None:
                if instagram_returnResult['사용자ID'] == username:
                    instagram_T_Value += 50
                else:
                    instagram_T_Value += 35
            else:
                print('불가능한 경우: 사용자ID 값이 없는 경우')
        except Exception as e:
            print()
        instagram_returnResult['insta_TSCORE'] = instagram_T_Value

        try:
            if instagram_returnResult['게시글수'] >= 500:
                instagram_C_Value += 50
            elif instagram_returnResult['게시글수'] < 500 and instagram_returnResult['게시글수'] >= 300:
                instagram_C_Value += 35
            else:
                instagram_C_Value += 15
        except Exception as e:
            print('게시글이 존재하지 않는 경우')

        try:
            if instagram_returnResult['팔로워수'] >= 100000:
                instagram_C_Value += 50
            elif instagram_returnResult['팔로워수'] < 100000 and instagram_returnResult['팔로워수'] >= 50000:
                instagram_C_Value += 40
            elif instagram_returnResult['팔로워수'] < 50000 and instagram_returnResult['팔로워수'] >= 10000:
                instagram_C_Value += 30
            elif instagram_returnResult['팔로워수'] < 10000 and instagram_returnResult['팔로워수'] >= 5000:
                instagram_C_Value += 20
            else:
                instagram_C_Value += 10
        except Exception as e:
            print('팔로워가 존재하지 않는 경우')

        try:
            if instagram_returnResult['팔로잉수'] >= 10000:
                instagram_C_Value += 50
            elif instagram_returnResult['팔로잉수'] < 10000 and instagram_returnResult['팔로잉수'] >= 5000:
                instagram_C_Value += 40
            elif instagram_returnResult['팔로잉수'] < 5000 and instagram_returnResult['팔로잉수'] >= 1000:
                instagram_C_Value += 30
            elif instagram_returnResult['팔로잉수'] < 1000 and instagram_returnResult['팔로잉수'] >= 500:
                instagram_C_Value += 20
            elif instagram_returnResult['팔로잉수'] < 500 and instagram_returnResult['팔로잉수'] >= 100:
                instagram_C_Value += 10
            else:
                instagram_C_Value += 5

        except Exception as e:
            print('팔로잉이 존재하지 않는 경우')
        instagram_returnResult['insta_CSCORE'] = instagram_C_Value

        try:
            if instagram_returnResult['게시글내단어수'] >= 1000:
                instagram_M_Value += 70
            elif instagram_returnResult['게시글내단어수'] < 1000 and instagram_returnResult['게시글내단어수'] >= 500:
                instagram_M_Value += 60
            elif instagram_returnResult['게시글내단어수'] < 500 and instagram_returnResult['게시글내단어수'] >= 100:
                instagram_M_Value += 50
            elif instagram_returnResult['게시글내단어수'] < 100 and instagram_returnResult['게시글내단어수'] >= 10:
                instagram_M_Value += 40
            else:
                instagram_M_Value += 30
        except Exception as e:
            print('게시글내단어수가 존재하지 않는 경우')

        try:
            if instagram_returnResult['해쉬테그수'] >= 500:
                instagram_M_Value += 70
            elif instagram_returnResult['해쉬테그수'] < 500 and instagram_returnResult['해쉬테그수'] >= 300:
                instagram_M_Value += 60
            elif instagram_returnResult['해쉬테그수'] < 300 and instagram_returnResult['해쉬테그수'] >= 100:
                instagram_M_Value += 50
            elif instagram_returnResult['해쉬테그수'] < 100 and instagram_returnResult['해쉬테그수'] >= 50:
                instagram_M_Value += 40
            elif instagram_returnResult['해쉬테그수'] < 50 and instagram_returnResult['해쉬테그수'] >= 10:
                instagram_M_Value += 30
            else:
                instagram_M_Value += 20

        except Exception as e:
            print('해쉬테그수가 존재하지 않는 경우')
        instagram_returnResult['insta_MSCORE'] = instagram_C_Value

        returnValue_instagram = True

        # DB Connection=======================================
        currDate = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(time.localtime().tm_mday) + '-' \
                   + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min) + '-' + str(time.localtime().tm_sec)
        print(currDate)

        end_time = time.time() - start_time_all
        print('데이터 기반 크롤링 총 구동 시간 :', end_time)

        try:
            # Server Connection to MySQL
            databaseConnection = mysqlConnection.DatabaseConnection_origin()
            databaseConnection.update_instagramRecord(
                str(instagram_returnResult['사용자ID'].replace(" ", "")),
                str(instagram_returnResult['게시글수']),
                str(instagram_returnResult['팔로워수']),
                str(instagram_returnResult['팔로잉수']),
                str(instagram_returnResult['게시글내단어수']),
                str(instagram_returnResult['해쉬테그수']),
                str(instagram_returnResult['insta_TSCORE']),
                str(instagram_returnResult['insta_CSCORE']),
                str(instagram_returnResult['insta_MSCORE']),
                fb_pageID
            )
        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

        instagram_returnResult['trueOrFalse'] = True


        driver.close()

        return instagram_returnResult