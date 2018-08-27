#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging.handlers
import sys
import time

import http.client
import json
import requests
import self
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection


class kakaostoryCrawlerBot:

    global driver
    def __init__(self):
        print('kakaostoryCrawlerBot _ start')


global returnValue_kks_CSVData
global returnValue_kks_singleData
global hereWork

hereWork = 'KakaoStory'

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

def crawling_CSVdata_KakaoStoryCrawlerBot(fb_pageID):

    start_time_all = time.time()
    # Session 생성, with 구문 안에서 유지
    with requests.Session() as s:

        returnValue_kks_CSVData = False

        loginURL = 'https://accounts.kakao.com/login/kakaostory'
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

        adminEmailAddr = 'kimtheho@hanmail.net'
        adminPassword = '77882e2e'

        # 로그인
        driver.find_element_by_id('loginEmail').send_keys(adminEmailAddr)
        driver.find_element_by_id('loginPw').send_keys(adminPassword)
        driver.find_element_by_class_name('btn_login').click()

        # click 후 화면 전환까지 시간이 필요하여 time.sleep을 선언함.
        time.sleep(1)

        # =============================================================================
        print('driver.current_url : ', driver.current_url)  # https://story.kakao.com/

        user_kakaoStory_list = []

        with open('C:\\python_project\\aster879_project\\PycharmProjects\\' + hereWork + '_' + currTime +'.csv', 'r', encoding='utf-8') as csvCorpNameFile:
            # reader = csv.DictReader(csvCorpNameFile)
            reader = csv.reader(csvCorpNameFile)

            for row in reader:
                if row[12].replace(" ", "") == "":
                    # print('카카오 스토리 주소 정보가 없습니다.')
                    continue

                else:
                    user_kakaoStory_infos = {}
                    user_kakaoStory_infos.update({'user_name': row[0].replace(" ", "")})
                    user_kakaoStory_infos.update({'user_kakaoStory_URL': row[12].replace(" ", "")})
                    user_kakaoStory_list.append(user_kakaoStory_infos)

        # 20180509
        # 가공 데이터 CSV 파일화 작업
        currDate = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
            time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(
            time.localtime().tm_sec)
        with open("C:\\python_project\\aster879_project\\PycharmProjects\\CrawledData_kakaoStory_" + currDate + ".csv", "w", newline='') as kksFile:

            # user_kakaoStory_URL 리스트의 길이만큼, 즉 카카오스토리 주소가 있는 사람들의 수 만큼 반복
            for userlnth in range(len(user_kakaoStory_list)):
                start_time_per = time.time()

                userlnth += 1
                kakaoStory_userInfo = {}
                kakaoStory_userInfo['페이스북페이지ID'] = fb_pageID

                try:
                    driver.get(user_kakaoStory_list[userlnth]['user_kakaoStory_URL'].replace(" ", "") + '/profile')
                    kakaoStory_userInfo['카카오스토리페이지ID'] = user_kakaoStory_list[userlnth]['user_kakaoStory_URL'].replace(" ", "")

                    print(driver.current_url)
                    error_cnt = 0

                    while True:
                        try:
                            if driver.find_element_by_class_name('img_trans') != None:

                                # 페이지가 로딩된 다음 beautifulSoup을 이용하여 HTML 문서 값 가져옴.
                                kakaoStory_soup = bs(driver.page_source, 'html.parser')

                                if kakaoStory_soup.select(
                                        '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4.tit_collection')[
                                    0].text is not None:
                                    print()
                                    print(kakaoStory_soup.select(
                                        '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4')[
                                              0].text)

                                    # 기본 정보(이름, 생일, 성별, 뮤직, 직장정보, 거주지정보)
                                    # 아래의 영역 값들은 공개할 수도, 안할 수도 있는 것들임. 각각의 항목을 반드시 try except로 묶어 Exception에 의한 process 중단을 피해야 함.

                                    for dlLength in range(len(kakaoStory_soup.select(
                                            '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div[data-part-name=profileView] > dl'))):
                                        dlLength += 1

                                        try:
                                            user_info_span_title = kakaoStory_soup.select(
                                                '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div > dl:nth-of-type(' + str(
                                                    dlLength) + ') > dt > span')[0].text.strip(" ").replace(" ", "")

                                            userInfo_dl_value = kakaoStory_soup.select(
                                                '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div[data-part-name=profileView] > dl:nth-of-type(' + str(
                                                    dlLength) + ') > dd > div'
                                            )[0].text.strip(" ").replace(" ", "")

                                            print(user_info_span_title, ' : ', userInfo_dl_value)

                                            if user_info_span_title == '이름':
                                                if userInfo_dl_value == user_kakaoStory_list[userlnth]['user_name'].replace(
                                                        " ", ""):
                                                    print('사용자의 카카오 스토리 상의 이름과 데이터 상의 성명이 일치합니다.')
                                                    kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value.replace(
                                                        " ", "")
                                                    kakaoStory_userInfo[
                                                        user_info_span_title + '_kakaoStory_nickName'] = userInfo_dl_value.replace(
                                                        " ", "")
                                                    print('user_name :', userInfo_dl_value)

                                                else:
                                                    print('사용자의 카카오 스토리 상의 이름과 데이터 상의 성명이 \"불\"일치합니다.')
                                                    kakaoStory_userInfo[user_info_span_title] = \
                                                    user_kakaoStory_list[userlnth]['user_name'].replace(" ", "")
                                                    kakaoStory_userInfo[
                                                        user_info_span_title + '_kakaoStory_nickName'] = userInfo_dl_value.replace(
                                                        " ", "")

                                                    print('userName:', userInfo_dl_value.replace(" ", ""), ', ',
                                                          'userNickName :', userInfo_dl_value.replace(" ", ""))
                                            #20180712 elif --> if
                                            if user_info_span_title == '생일':
                                                kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value
                                                print('userBirth : ', userInfo_dl_value)
                                            else:
                                                kakaoStory_userInfo['생일'] = ''

                                            if user_info_span_title == '성별':
                                                kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value
                                                print('userSex : ', userInfo_dl_value)
                                            else:
                                                kakaoStory_userInfo['성별'] = ''

                                            if user_info_span_title == '한줄음악':
                                                kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value
                                                print('userMusic : ', userInfo_dl_value)
                                            else:
                                                kakaoStory_userInfo['한줄음악'] = '한줄음악정보없음'

                                            if user_info_span_title == '직장':
                                                kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value
                                                print('userWork :', userInfo_dl_value)
                                            else:
                                                kakaoStory_userInfo['직장'] = '직장정보없음'

                                            if user_info_span_title == '거주지':
                                                kakaoStory_userInfo[user_info_span_title] = userInfo_dl_value
                                                print('userHome :', userInfo_dl_value)
                                            else:
                                                kakaoStory_userInfo['거주지'] = ''

                                        except Exception as userSexException:
                                            print('사용자가 정보를 더이상 공개하지 않았습니다. ->', userSexException)

                                    print('기본정보 게시 항목 개수 :', str(dlLength), ' -> ', kakaoStory_userInfo)

                                    # 정보(스토리 개수, 출신 학교)
                                    if kakaoStory_soup.select(
                                            '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > h3')[
                                        0].text is not None:
                                        print()
                                        print(kakaoStory_soup.select(
                                            '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > h3')[
                                                  0].text)
                                        print('정보 항목의 개수 :', len(kakaoStory_soup.select(
                                            '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt')))

                                        for userInfoDTLength in range(len(kakaoStory_soup.select(
                                                '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt'))):
                                            userInfoDTLength += 1

                                            user_compctInfo_title = kakaoStory_soup.select(
                                                '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt:nth-of-type(' + str(
                                                    userInfoDTLength) + ') > span:nth-of-type(1)')[0].text
                                            user_compctInfo_value = kakaoStory_soup.select(
                                                '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dd:nth-of-type(' + str(
                                                    userInfoDTLength) + ')')[0].text

                                            kakaoStory_userInfo[user_compctInfo_title] = user_compctInfo_value

                                    # print('dic test:', kakaoStory_userInfo)
                                    # 검색 완료 후 while문 종료
                                    break

                                else:
                                    print(
                                        'kakaoStory_soup.select(\"#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4\")[0].text 값 없음')
                                    break
                            # 1st if END

                        except:
                            print('아직 프로필 페이지가 로딩되지 않았습니다.')
                            time.sleep(0.1)

                            error_cnt += 1

                            if error_cnt == 5:
                                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), ' 사용자의 페이지가 존재하지 않습니다.')
                                break
                            else:
                                continue
                        # try END
                    # while END

                except Exception as e:
                    print('더이상 크롤링 대상이 없습니다.--> ', e)
                    break
                # try END

                # 정보 제공량 별 점수 산출
                print('Confirm for Extracted Data :', kakaoStory_userInfo)
                print('기본적인 정보 추출이 완료되었습니다. -> 본 정보를 바탕으로 점수 산출을 진행하겠습니다.')
                time.sleep(1.5)
                kakaoStoryValue = 0
                kakaoStoryTValue = 0
                kakaoStoryCValue = 0
                kakaoStoryMValue = 0

                if '성별' in kakaoStory_userInfo:
                    if kakaoStory_userInfo['성별'] == '남성':
                        print('성별 남성 : 10점이 부여되었습니다.')
                        kakaoStoryTValue += 10

                    elif kakaoStory_userInfo['성별'] == '여성':
                        kakaoStoryTValue += 5
                        print('성별 여성 : 5점이 부여되었습니다.')
                else:
                    print('성별이 공개되지 않았습니다.')

                if '한줄음악' in kakaoStory_userInfo:
                    print('카카오 뮤직 공개 : 10점이 부여되었습니다.')
                    kakaoStoryCValue += 10
                else:
                    print('카카오 뮤직 비공개 : 0점이 부여되었습니다.')

                if '거주지' in kakaoStory_userInfo:
                    print('거주지 정보 공개')
                    if '서울' in kakaoStory_userInfo['거주지']:
                        print('거주지 정보- 서울 : 25점이 부여되었습니다.')
                        kakaoStoryTValue += 25
                    elif '경기' in kakaoStory_userInfo['거주지']:
                        print('거주지 정보- 경기 : 20점이 부여되었습니다.')
                        kakaoStoryTValue += 20
                    else:
                        print('거주지 정보- 비수도권 : 15점이 부여되었습니다.')
                        kakaoStoryTValue += 15
                else:
                    print('거주지 정보 비공개')

                if '스토리' in kakaoStory_userInfo:
                    print('게시 스토리 개수 공개')

                    try:
                        kstoryCount_str = kakaoStory_userInfo['스토리'].split('개')[0]
                        kstoryCount_int = int(kstoryCount_str.replace(",", ""))

                        kakaoStory_userInfo['카카오스토리개수'] = str(kstoryCount_int)

                        if kstoryCount_int >= 200:
                            print('게시 스토리 개수 200개 이상')
                            kakaoStoryMValue += 25
                        elif kstoryCount_int < 200:
                            print('게시 스토리 개수 200개 미만')
                            kakaoStoryMValue += 15

                    except Exception as ex:
                        print('스토리 개수 표시가 \"~개\" 로 표시되어 있지 않습니다. 단순 숫자로 표시')
                        if int(kakaoStory_userInfo['스토리']) >= 200:
                            print('게시 스토리 개수 200개 이상')
                            kakaoStoryMValue += 25
                        elif int(kakaoStory_userInfo['스토리']) < 200:
                            print('게시 스토리 개수 200개 미만')
                            kakaoStoryMValue += 15
                else:
                    print('게시 스토리 개수 비공개')

                if '학교' in kakaoStory_userInfo:
                    print(kakaoStory_userInfo['학교'])
                    print('학력 정보 공개')
                    univList = ['서울대학교', '중앙대학교', '덕성여자대학교', '건국대학교', '서울교육대학교', '홍익대학교', '이화여자대학교', '서울시립대학교', '동국대학교',
                                '서울여자대학교', '연세대학교', '명지대학교', '숙명여학교', '고려대학교', '상명대학교', '동덕여자대학교', '서강대학교', '삼육대학교',
                                '국민대학교', '서울과학기술대학교', '한국체육대학교', '성신여자대학교', '한국외국어대학교', '숭실대학교', '총신대학교', '세종대학교',
                                '한국종합예술학교', '한성대학교', '서경대학교', '성공회대학교']

                    user_edu_history = kakaoStory_userInfo['학교']
                    # print('@@', user_edu_history)

                    if user_edu_history in univList:
                        print('학력 정보- in 서울')
                        kakaoStoryTValue += 25

                    else:
                        print('학력 정보- not in 서울')
                        kakaoStoryTValue += 15
                else:
                    print('학력 정보 비공개')

                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), '님의 카카오스토리 총점 :', kakaoStoryValue)
                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), '님의 카카오스토리 Tscore 총점 :', kakaoStoryTValue)
                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), '님의 카카오스토리 Cscore 총점 :', kakaoStoryCValue)
                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), '님의 카카오스토리 Mscore 총점 :', kakaoStoryMValue)
                kakaoStory_userInfo['kk_TSCORE'] = str(kakaoStoryTValue)
                kakaoStory_userInfo['kk_CSCORE'] = str(kakaoStoryCValue)
                kakaoStory_userInfo['kk_MSCORE'] = str(kakaoStoryMValue)
                print(user_kakaoStory_list[userlnth]['user_name'].replace(" ", ""), '님의 카카오스토리 크롤링 결과', kakaoStory_userInfo)

                # DB insert
                try:
                    # Server Connection to MySQL:
                    databaseConnection = mysqlConnection.DatabaseConnection_origin()
                    databaseConnection.update_kakaoStoryRecord(
                        str(kakaoStory_userInfo['카카오스토리페이지ID'].replace(" ", "")),
                        str(kakaoStory_userInfo['이름_kakaoStory_nickName'].replace(" ", "")),
                        str(kakaoStory_userInfo['스토리'].replace(" ", "").replace("개", "")),
                        str(kakaoStory_userInfo['생일'].replace(" ", "")),
                        str(kakaoStory_userInfo['학교'].replace(" ", "")),
                        str(kakaoStory_userInfo['한줄음악'].replace(" ", "")),
                        str(kakaoStory_userInfo['거주지'].replace(" ", "")),
                        str(kakaoStory_userInfo['직장'].replace(" ", "")),
                        str(kakaoStory_userInfo['kk_TSCORE'].replace(" ", "")),
                        str(kakaoStory_userInfo['kk_CSCORE'].replace(" ", "")),
                        str(kakaoStory_userInfo['kk_MSCORE'].replace(" ", "")),
                        fb_pageID
                    )


                except Exception as e_maria:
                    logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

                returnedValue_TCMCountGen = True
                # kakaoStory_userInfo ==> dictionary type
                writer = csv.writer(kksFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [str(user_kakaoStory_list[userlnth]['user_name'].replace(" ", "") + '님의 카카오 스토리 관련 정보')])

                for key, val in kakaoStory_userInfo.items():
                    writer.writerow([key, val])
                writer.writerow([])

                end_time = time.time() - start_time_per
                print('현 단계 크롤러 구동 시간 :', end_time)
                print()
                returnValue_kks_CSVData = True

            end_time = time.time() - start_time_all
            print('데이터 기반 크롤링 총 구동 시간 :', end_time)
    driver.close()

    return returnValue_kks_CSVData, kakaoStory_userInfo


#CSV 파일이 아닌 개별 정보 제공시
def crawling_singleData_KakaoStoryCrawlerBot(userKakaoStory_pageID, username, userCellPhNum):

    global returnValue_kks_singleData

    start_time_all = time.time()
    with requests.Session() as s:

        returnValue_kks_singleData = False
        loginURL = 'https://accounts.kakao.com/login/kakaostory'
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

        adminEmailAddr = 'kimtheho@hanmail.net'
        adminPassword = '77882e2e'

        # 로그인
        driver.find_element_by_id('loginEmail').send_keys(adminEmailAddr)
        driver.find_element_by_id('loginPw').send_keys(adminPassword)
        driver.find_element_by_class_name('btn_login').click()

        #click 후 화면 전환까지 시간이 필요하여 time.sleep을 선언함.
        time.sleep(1)

        start_time_per = time.time()
        kakaoStory_userInfo = {}
        kakaoStory_userInfo['카카오스토리페이지ID'] = userKakaoStory_pageID

        # 20180509
        currDate = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
            time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(
            time.localtime().tm_sec)
        with open("C:\\python_project\\aster879_project\\PycharmProjects\\CrawledData_"+ hereWork +"_" + currDate + ".csv","w", newline='') as kksFile:

            try:
                driver.get('https://story.kakao.com/' + userKakaoStory_pageID + '/profile')
                print(driver.current_url)
                error_cnt = 0

                while True:
                    try:
                        if driver.find_element_by_class_name('img_trans') != None:

                            # 페이지가 로딩된 다음 beautifulSoup을 이용하여 HTML 문서 값 가져옴.
                            kakaoStory_soup = bs(driver.page_source, 'html.parser')

                            if kakaoStory_soup.select(
                                    '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4.tit_collection')[
                                0].text is not None:
                                print()
                                print(kakaoStory_soup.select(
                                    '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4')[0].text)

                                # 기본 정보(이름, 생일, 성별, 뮤직, 직장정보, 거주지정보)
                                # 아래의 영역 값들은 공개할 수도, 안할 수도 있는 것들임. 각각의 항목을 반드시 try except로 묶어 Exception에 의한 process 중단을 피해야 함.
                                for dlLength in range(len(kakaoStory_soup.select(
                                        '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div[data-part-name=profileView] > dl'))):
                                    dlLength += 1

                                    try:
                                        user_info_span_title = kakaoStory_soup.select(
                                            '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div > dl:nth-of-type(' + str(
                                                dlLength) + ') > dt > span')[0].text.strip(" ").replace(" ", "")

                                        userInfo_dl_value = kakaoStory_soup.select(
                                            '#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > div > div[data-part-name=profileView] > dl:nth-of-type(' + str(
                                                dlLength) + ') > dd > div'
                                        )[0].text.strip(" ").replace(" ", "")

                                        print(user_info_span_title, ' : ', userInfo_dl_value)

                                        if user_info_span_title == '이름':
                                            if userInfo_dl_value == username:
                                                print('사용자의 카카오 스토리 상의 이름과 데이터 상의 성명이 일치합니다.')
                                                kakaoStory_userInfo['이름'] = userInfo_dl_value.replace(" ", "")
                                                kakaoStory_userInfo['이름_kakaoStory_nickName'] = userInfo_dl_value.replace(" ", "")

                                                print('user_name :', userInfo_dl_value)

                                            else:
                                                print('사용자의 카카오 스토리 상의 이름과 데이터 상의 성명이 \"불\"일치합니다.')
                                                kakaoStory_userInfo['이름'] = username
                                                kakaoStory_userInfo['이름_kakaoStory_nickName'] = userInfo_dl_value.replace(" ", "")

                                                print('userName:', userInfo_dl_value.replace(" ", ""), ', ', 'userNickName :', userInfo_dl_value.replace(" ", ""))

                                        #20180712
                                        if user_info_span_title == '생일':
                                            kakaoStory_userInfo['생일'] = userInfo_dl_value
                                            print('userBirth : ', userInfo_dl_value)
                                        else:
                                            kakaoStory_userInfo['생일'] = ''

                                        if user_info_span_title == '성별':
                                            kakaoStory_userInfo['성별'] = userInfo_dl_value
                                            print('userSex : ', userInfo_dl_value)
                                        else:
                                            kakaoStory_userInfo['성별'] = ''

                                        if user_info_span_title == '한줄음악':
                                            kakaoStory_userInfo['한줄음악'] = userInfo_dl_value
                                            print('userMusic : ', userInfo_dl_value)
                                        else:
                                            kakaoStory_userInfo['한줄음악'] = '한줄음악정보없음'

                                        if user_info_span_title == '직장':
                                            kakaoStory_userInfo['직장'] = userInfo_dl_value
                                            print('userWork :', userInfo_dl_value)
                                        else:
                                            kakaoStory_userInfo['직장'] = '직장정보없음'

                                        if user_info_span_title == '거주지':
                                            kakaoStory_userInfo['거주지'] = userInfo_dl_value
                                            print('userHome :', userInfo_dl_value)
                                        else:
                                            kakaoStory_userInfo['거주지'] = ''

                                    except Exception as userSexException:
                                        print('사용자가 정보를 더이상 공개하지 않았습니다. ->', userSexException)

                                print('기본정보 게시 항목 개수 :', str(dlLength), ' -> ', kakaoStory_userInfo)

                                # 정보(스토리 개수, 출신 학교)
                                if kakaoStory_soup.select('#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > h3')[0].text is not None:
                                    print()
                                    print(kakaoStory_soup.select('#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > h3')[0].text)
                                    print('정보 항목의 개수 :', len(kakaoStory_soup.select('#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt')))

                                    for userInfoDTLength in range(len(kakaoStory_soup.select('#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt'))):
                                        userInfoDTLength += 1
                                        user_compctInfo_title = kakaoStory_soup.select(
                                            '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dt:nth-of-type(' + str(userInfoDTLength) + ') > span:nth-of-type(1)')[0].text
                                        user_compctInfo_value = kakaoStory_soup.select(
                                            '#myStoryContentWrap > div[data-module=myStoryWidget] > div.story_widgets > div[data-part-name=myInfo] > div > dl.list_info > dd:nth-of-type(' + str(userInfoDTLength) + ')')[0].text

                                        kakaoStory_userInfo[user_compctInfo_title] = user_compctInfo_value

                                    print('$', kakaoStory_userInfo)

                                # print('dic test:', kakaoStory_userInfo)
                                # 검색 완료 후 while문 종료
                                break

                            else:
                                print(
                                    'kakaoStory_soup.select(\"#myStoryContentWrap > div:nth-of-type(2) > div > div.profile_collection > h4\")[0].text 값 없음')
                                break
                        # 1st if END

                    except:
                        print('아직 프로필 페이지가 로딩되지 않았습니다.')
                        time.sleep(0.1)

                        error_cnt += 1

                        if error_cnt == 5:
                            print(username, ' 사용자의 페이지가 존재하지 않습니다.')
                            break
                        else:
                            continue
                    # try END
                # while END

            except Exception as e:
                print('더이상 크롤링 대상이 없습니다.--> ', e)
            # try END

            # 정보 제공량 별 점수 산출
            print('Confirm for Extracted Data :', kakaoStory_userInfo)
            print('기본적인 정보 추출이 완료되었습니다. -> 본 정보를 바탕으로 점수 산출을 진행하겠습니다.')
            time.sleep(1.5)
            kakaoStoryValue = 0
            kakaoStory_T_Value = 0
            kakaoStory_C_Value = 0
            kakaoStory_M_Value = 0

            if '성별' in kakaoStory_userInfo:
                if kakaoStory_userInfo['성별'] == '남성':
                    print('성별 남성 : 20점이 부여되었습니다.')
                    kakaoStory_T_Value += 20

                elif kakaoStory_userInfo['성별'] == '여성':
                    kakaoStory_T_Value += 10
                    print('성별 여성 : 10점이 부여되었습니다.')
            else:
                print('성별이 공개되지 않았습니다.')

            if '한줄음악' in kakaoStory_userInfo:
                print('카카오 뮤직 공개 : 20점이 부여되었습니다.')
                kakaoStory_C_Value += 20
            else:
                print('카카오 뮤직 비공개 : 0점이 부여되었습니다.')

            if '거주지' in kakaoStory_userInfo:
                print('거주지 정보 공개')
                if '서울' in kakaoStory_userInfo['거주지']:
                    print('거주지 정보- 서울 : 50점이 부여되었습니다.')
                    kakaoStory_T_Value += 50
                elif '경기' in kakaoStory_userInfo['거주지']:
                    print('거주지 정보- 경기 : 30점이 부여되었습니다.')
                    kakaoStory_T_Value += 30
                else:
                    print('거주지 정보- 비수도권 : 15점이 부여되었습니다.')
                    kakaoStory_T_Value += 15
            else:
                print('거주지 정보 비공개')

            if '스토리' in kakaoStory_userInfo:
                print('게시 스토리 개수 공개')

                try:
                    kstoryCount_str = kakaoStory_userInfo['스토리'].split('개')[0]
                    kstoryCount_int = int(kstoryCount_str.replace(",", ""))

                    if kstoryCount_int >= 200:
                        print('게시 스토리 개수 200개 이상')
                        kakaoStory_M_Value += 50
                    elif kstoryCount_int < 200:
                        print('게시 스토리 개수 200개 미만')
                        kakaoStory_M_Value += 30

                except Exception as ex:
                    print('스토리 개수 표시가 \"~개\" 로 표시되어 있지 않습니다. 단순 숫자로 표시')
                    if int(kakaoStory_userInfo['스토리']) >= 200:
                        print('게시 스토리 개수 200개 이상')
                        kakaoStory_M_Value += 50
                    elif int(kakaoStory_userInfo['스토리']) < 200:
                        print('게시 스토리 개수 200개 미만')
                        kakaoStory_M_Value += 30
            else:
                print('게시 스토리 개수 비공개')

            if '학교' in kakaoStory_userInfo:
                print(kakaoStory_userInfo['학교'])
                print('학력 정보 공개')
                univList = ['서울대학교', '중앙대학교', '덕성여자대학교', '건국대학교', '서울교육대학교', '홍익대학교', '이화여자대학교', '서울시립대학교', '동국대학교', '서울여자대학교',
                            '연세대학교', '명지대학교', '숙명여학교', '고려대학교', '상명대학교', '동덕여자대학교', '서강대학교', '삼육대학교', '국민대학교', '서울과학기술대학교',
                            '한국체육대학교', '성신여자대학교', '한국외국어대학교', '숭실대학교', '총신대학교', '세종대학교', '한국종합예술학교', '한성대학교', '서경대학교', '성공회대학교']

                user_edu_history = kakaoStory_userInfo['학교']

                if user_edu_history in univList:
                    print('학력 정보- in 서울')
                    kakaoStory_T_Value += 50

                else:
                    print('학력 정보- not in 서울')
                    kakaoStory_T_Value += 30
            else:
                print('학력 정보 비공개')
                kakaoStory_userInfo['학교'] = '학력정보가 알아보기 쉽게 명시되지 않았습니다.'

            kakaoStory_userInfo['카카오스토리점수'] = kakaoStoryValue
            kakaoStory_userInfo['kk_TSCORE'] = kakaoStory_T_Value
            kakaoStory_userInfo['kk_CSCORE'] = kakaoStory_C_Value
            kakaoStory_userInfo['kk_MSCORE'] = kakaoStory_M_Value
            print(username, '님의 카카오스토리 크롤링 결과', kakaoStory_userInfo)

            # DB insert
            try:
                # Server Connection to MySQL
                databaseConnection = mysqlConnection.DatabaseConnection_origin()
                databaseConnection.update_kakaoStoryRecord(
                            str(kakaoStory_userInfo['카카오스토리페이지ID'].replace(" ", "")),
                            str(kakaoStory_userInfo['이름_kakaoStory_nickName'].replace(" ", "")),
                            str(kakaoStory_userInfo['스토리'].replace(" ", "").replace("개","")),
                            str(kakaoStory_userInfo['생일'].replace(" ", "")),
                            str(kakaoStory_userInfo['학교'].replace(" ", "")),
                            str(kakaoStory_userInfo['한줄음악'].replace(" ", "")),
                            str(kakaoStory_userInfo['거주지'].replace(" ", "")),
                            str(kakaoStory_userInfo['직장'].replace(" ", "")),
                            str(kakaoStory_userInfo['kk_TSCORE']),
                            str(kakaoStory_userInfo['kk_CSCORE']),
                            str(kakaoStory_userInfo['kk_MSCORE']),
                            userCellPhNum
                )

            except Exception as e_maria:
                logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

            # 20180509
            # kakaoStory_userInfo ==> dictionary type
            writer = csv.writer(kksFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([username + '님의 카카오 스토리 관련 정보'])

            for key, val in kakaoStory_userInfo.items():
                writer.writerow([key, val])
            writer.writerow([])

        end_time = time.time() - start_time_per
        print('현 단계 크롤러 구동 시간 :', end_time)
        print()
        returnValue_kks_singleData = True

    end_time = time.time() - start_time_all
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)

    driver.close()

    kakaoStory_userInfo['trueOrFalse'] = True


    # 20180509
    #생성한 CSV 파일 읽기 - 정상 입력 검사
    with open("C:\\python_project\\aster879_project\\PycharmProjects\\CrawledData_"+ hereWork +"_" + currDate + ".csv", "r") as readCSVfile:
        reader = csv.reader(readCSVfile)

        # read file row by row
        for row in reader:
            print(row)

    #boolean 값
    return kakaoStory_userInfo





























