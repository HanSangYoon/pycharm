#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import requests, json, http.client
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging.handlers

class worknetCrawlerBot:
    def __init__(self):
        print('start')

global driver
global user_id
global user_pass
global pagelet_dict_data
global t_score_count
global returnValue_facebook

global hereWork
hereWork = 'worknet'

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

#def CrawlingByWorkNetCrawlBot():
start_time_all = time.time()
returnValue_worknet = False

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        last_height = new_height

    # autoScroll crawling data 가져오기
    autoScrolled_data_soup_html = bs(driver.page_source, 'html.parser')
    return autoScrolled_data_soup_html


def getTotalRecruitCount(driver):
    worknet_firstPage_soup_html = bs(driver.page_source, 'html.parser')
    print('게시글 전체 갯수', worknet_firstPage_soup_html.select("#searchCondExtVO > div.sub_search_wrap.matching2 > div.sch_total > span > em")[0].text)

    totCnt_recruit = worknet_firstPage_soup_html.select("#searchCondExtVO > div.sub_search_wrap.matching2 > div.sch_total > span > em")[0].text.replace(",", "")

    return totCnt_recruit

def getPagination(driver, searchURL):

    #soup = bs(r.content, "html.parser")
    page_url = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex={}"

    driver.get(page_url.format(1))

    totalCount_str = getTotalRecruitCount(driver)

    totalCount = int(int(totalCount_str)/10)+1

    print(totalCount)

    #연결될 각 페이지의 URL
    #dept_page_url = [page_url.format(i) for i in range(1, totalCount)]
    dept_page_url = [page_url.format(i) for i in range(1, 11)]  #테스트를 위해 10페이지로 제한.

    #결과값 딕셔너리 타입
    result_workNetDictionaty = {}


    #각각의 URL을 driver.get()에 주입하여 loop를 돌리면서 각 페이지를 crawling.
    i = 0
    for page_length in range(len(dept_page_url)):
        driver.get(dept_page_url[i])

        i += 1
        print(i, '.', driver.current_url)

        #logger
        logger.debug('current_url => {}'.format(driver.current_url))

        #scrapping
        result_autoScroller = autoScroller(driver)

        list_indies = '0,1,2,3,4,5,6,7,8,9'

        for list_length in range(len(result_autoScroller.select("#searchCondExtVO > table > tbody > tr"))):

            #기업 명 체크박스 선별
            #pageSourceText = result_autoScroller.find_all('input', {'id': 'chkboxWantedAuthNo' + list_indies.split(',')[list_length]} )

            #회사명 + 모집 업무
            corpName_key = '회사명' + str(i) + str(list_length) + list_indies.split(',')[list_length]
            corpJob_key = '모집업무' + str(i) + str(list_length) + list_indies.split(',')[list_length]

            corpName = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(2)")[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n", "").replace("\xa0", "").replace("워크넷", "/워크넷_인증")
            result_workNetDictionaty[corpName_key] = corpName

            try:
                corpJob = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(3) > dl > dd:nth-of-type(1)")[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n", "").replace("\xa0", "")
                result_workNetDictionaty[corpJob_key] = corpJob

            except Exception as e:
                #채용 정보 미리 보기 없음
                if "미리보기없음" in corpJob:
                    result_workNetDictionaty[corpJob_key] = '___채용정보미리보기없음___'
                    logger.debug('corp_info => {}'.format('$$$$$$$__'+ corpName + '&&채용정보 미리보기 없음'))
                result_workNetDictionaty[corpJob_key] = '___채용정보미리보기없음___'

                logger.error('error_in_corpName&corpJob ==> {}'.format(e))
                logger.debug('corp_info => {}'.format('$$$$$$$__'+ corpName + '&&채용정보 미리보기 없음'))


            #학력 조건
            corpEduHistory_key = '학력조건' + str(i) + str(list_length) + list_indies.split(',')[list_length]
            try:
                corpEduHistory = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(3) > dl > dd:nth-of-type(2)")[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n", "").replace("\xa0", "")
                result_workNetDictionaty[corpEduHistory_key] = corpEduHistory

                logger.debug('corp_info => {}'.format('$$$$$$$__' + corpName + '&&' + corpJob + '&&' + corpEduHistory))

            #기재된 학력 조건 사항 없음
            except Exception as e:
                corpEduHistory = '기재된 학력 조건 사항 없음'
                result_workNetDictionaty[corpEduHistory_key] = corpEduHistory

                logger.error('error_in_corpEduHistory ==> {}'.format(e))
                logger.debug('corp_info => {}'.format('$$$$$$$__' + corpName + '&&' + corpJob + '&&기재된 학력 조건 사항 없음'))


            #근무 위치
            corpLocation_key = '근무위치' + str(i) + str(list_length) + list_indies.split(',')[list_length]
            try:
                corpLocation = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(3) > dl > dd:nth-of-type(3)")[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ","").replace("\n","").replace("\xa0", "")
                result_workNetDictionaty[corpLocation_key] = corpLocation

                logger.debug('corp_info => {}'.format('$$$$$$$__' + corpName + '&&' + corpJob + '&&' + corpEduHistory + '&&' + corpLocation))
            except Exception as e:
                #근무지 정보 없음
                corpLocation = '근무지 정보 없음'
                result_workNetDictionaty[corpLocation_key] = corpLocation

                logger.error('error_in_corpLocation ==> {}'.format(e))
                logger.debug('corp_info => {}'.format('$$$$$$$__'+ corpName + '&&' + corpJob + '&&' + corpEduHistory + '&&근무지 정보 없음'))

    print('##', result_workNetDictionaty)
    return result_workNetDictionaty


def bringContentBasicData(driver, searchURL):

    driver.get(searchURL)
    crawledResults = getPagination(driver, searchURL)

    return crawledResults

def startWorknetCrawling():
    with requests.Session() as s:

        #hereWork = 'worknet'

        visitedURL = 'http://www.work.go.kr'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        response = requests.get(visitedURL, headers=headers)
        #print(response)

        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        prefs = {}
        prefs['profile.default_content_setting_values.notifications'] = 2
        chrome_options.add_experimental_option('prefs', prefs)
        driver_chrome = r"C:\python_project\chromedriver.exe"

        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)
        driver.get(visitedURL)

        #print("worknet entered!")
        #print("1", driver.current_url)

        searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
        returnResult = bringContentBasicData(driver, searchURL)

        # DB Connection=======================================
        currDate = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(
            time.localtime().tm_mday) + '-' \
                   + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min) + '-' + str(time.localtime().tm_sec)
        print(currDate)

        Client = MongoClient('localhost', 27017)
        db_workNetCrawledData = Client[hereWork + 'CrawledData']
        collection_worknet = db_workNetCrawledData['PostText_' + hereWork]

        try:
            collection_worknet.insert({'Description(user_' + hereWork + '_URL)': 'http://www.work.go.kr',
                                         hereWork + '_data': returnResult,
                                         'inserted date': currDate})
            print('DB에 데이터를 정상적으로 INSERT 하였습니다.')
        except Exception as e:
            print('데이터 INSERT를 실패하였습니다.', e)
            logger.error('error_DB_INSERT => {}'.format(e))

        end_time = time.time() - start_time_all
        print('데이터 기반 크롤링 총 구동 시간 :', end_time)

        driver.close()

        returnValue_worknet = True

        return returnValue_worknet