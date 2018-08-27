#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, json, http.client
import sys
import csv
import self
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import logging
import logging.handlers
from pymongo import MongoClient


from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import Getting_HTMLDoc_bSoup4 as Get_HTML_bs
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import Getting_CommunicationScore as CScore
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import Getting_ManagementScore as MScore
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import Getting_TrustScore as TScore
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mongoDB_conn


class facebookCrawlerBot:
    def __init__(self):
        print('start')



global driver
global user_id
global user_pass
global pagelet_dict_data
global t_score_count
global returnValue_facebook

global hereWork
hereWork = 'FaceBook'

currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

#log 기본 설정 - 파일로 남기기 위해 [filename='./log/fb_logging_' + currTime] parameter로 추가한다.
#logging.basicConfig(filename='C:/python_project/just_project/PycharmProjects/log/' + hereWork + 'crawlerbot_logging_' + currTime, level=logging.DEBUG)

#logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

#fileHandler와 StreamHandler를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C:/python_project/log/' + hereWork + '_crawlerbot_logging_' + currTime +'_MAIN', maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

#logging
logging.debug(hereWork + '_crawlerbot_debugging on' + currTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')


#Common Methods
############################################################################
def webDriverSetting_chrome():

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {}
    prefs['profile.default_content_setting_values.notifications'] = 2
    chrome_options.add_experimental_option('prefs', prefs)
    driver_chrome = r"C:\python_project\chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)

    return driver

def login_facebook_admin(driver, admin_id, admin_pass):

    # Admin_url
    driver.get('https://www.facebook.com')
    driver.find_element_by_name('email').send_keys(admin_id)
    driver.find_element_by_name('pass').send_keys(admin_pass)

    # try login : 로그인 버튼의 id 값이 아래의 범위 내에서 무작위로 변경되기 때문에 이에 대한 대응차원임.
    # facebook 내에서 webdriver의 로그인 버튼 search에 대한 횟수 제한을 5회 정도로 제한을 둔 듯 함. 조건문 6번째 부터는 사실상 의미 없은 조건문임
    try:
        driver.find_element_by_xpath('// *[ @ id = "u_0_2"]').click()
        login_or_not = True
    except Exception as ex1:
        print('로그인 버튼 id 값이 u_0_2 가 아닙니다.', ex1)

        try:
            driver.find_element_by_xpath('// *[ @ id = "u_0_3"]').click()
            login_or_not = True
        except Exception as ex2:
            print('로그인 버튼 id 값이 u_0_3 이 아닙니다.', ex2)

            try:
                driver.find_element_by_xpath('// *[ @ id = "u_0_4"]').click()
                login_or_not = True
            except Exception as ex3:
                print('로그인 버튼 id 값이 u_0_4 가 아닙니다.', ex3)

                try:
                    driver.find_element_by_xpath('// *[ @ id = "u_0_d"]').click()
                    login_or_not = True
                except Exception as ex4:
                    print('로그인 버튼 id 값이 u_0_d 가 아닙니다.', ex4)

                    try:
                        driver.find_element_by_xpath('// *[ @ id = "u_0_f"]').click()
                        login_or_not = True
                    except Exception as ex5:
                        print('로그인 버튼 id 값이 u_0_f 가 아닙니다.', ex5)

                        try:
                            driver.find_element_by_xpath('// *[ @ id = "u_0_a"]').click()
                            login_or_not = True
                        except Exception as ex6:
                            print('로그인 버튼 id 값이 u_0_f 가 아닙니다.', ex6)

                            try:
                                driver.find_element_by_xpath('// *[ @ id = "u_0_e"]').click()
                                login_or_not = True
                            except Exception as ex7:
                                print('로그인 버튼 id 값이 u_0_e 가 아닙니다. 로그인 실패입니다. 소스를 다시 분석하세요.', ex7)
                                login_or_not = False


    return login_or_not





#Start Point ###########################################################################
def CrawlingByFacebookCrawlBot(loginCnt, userFacebookPageId, insertedUserName):
    start_time_all = time.time()
    returnValue_facebook = False

    user_id = '01027746254'
    user_pass = 'Gkstkddbs4$'

    #common Methods

    driver = webDriverSetting_chrome()
    login_returnResult = login_facebook_admin(driver, user_id, user_pass)

    loginCnt += 1

    user_facebook_page_id = userFacebookPageId
    directlyTypedUserName = insertedUserName

    logger.debug('For Test driver.current_url : {}'.format(driver.current_url))

    #Function
    returnedValue_from_method = FacebookTextDataCrawling(login_returnResult, loginCnt, user_facebook_page_id, directlyTypedUserName, driver)

    if returnedValue_from_method == True:
        returnValue_facebook = True

    end_time = time.time() - start_time_all
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)

    driver.close()

    #처음 호출한 웹서버에 리턴
    return returnValue_facebook






#function No.00 ###########################################################################
def FacebookTextDataCrawling(loginValue, lgnCnt, insertedUser_fbpage_id, insertedUserName, driver):
    returnedValue_profileTextDataCrawling = False

    if (loginValue == False):

        if (lgnCnt > 3):
            #print('페이스북 로그인에 최종 실패하여, 사용자 정보 크롤링이 불가합니다.')
            logger.error('페이스북 로그인 시도 횟수가 3회를 초과하여 로그인에 실패하였습니다. 사용자 정보 크롤링이 불가합니다.')
            driver.close()
        else:
            #print('프로그램을 중지하시고, 페이스북 로그인 정보를 다시 확인하시기 바랍니다.')
            logger.error('로그인을 다시 시도합니다.')
            CrawlingByFacebookCrawlBot(lgnCnt)

    elif (loginValue == True):
        logger.debug('Facebook login success!')

    #https://www.facebook.com/userpageID 상의 프로필 란에 게시된 정보 취득(Dictionary type)
    tscore = TScore.getTrustScore(insertedUser_fbpage_id, insertedUserName, lgnCnt, driver)



    '''
    
    
    profileInfo = TScore.getProfileData(timeLine_url, insertedUserName, driver)

    #https://www.facebook.com/userpageID/about 상의 [개요] & [경력 및 학력] & [거주했던 장소] & [연락처 및 기본 정보] & [가족 및 결혼/연애상태] & [자세한 소개] & [중요 이벤트] 취득 (Dictionary type)
    #returnedAboutPageResultDict = TScore.getAboutInfoDictionaryType(user_fbpage_id, driver, lgnCnt)
    tscore = TScore.getAboutInfoDictionaryType(user_fbpage_id, driver, lgnCnt)

  

    cscore = CScore.getAboutInfoDictionaryType(user_fbpage_id, driver, lgnCnt)
    mscore = MScore.getAboutInfoDictionaryType(user_fbpage_id, driver, lgnCnt)




    returnedResultDict = dict(returnedAboutPageResultDict, **profileInfo)
    logger.debug(':'.format(returnedResultDict) )
    returnedResultDictValues = returnedResultDict.values()

    #returnedResultDic 안에 거주지, 출신지, 친구수, 팔로우수, 좋아요수 를 저장해야 함.
    #returnedResultDictValues에는 T,C,M 점수를 산출할 수 있는 모든 결과값을 가지고 있어야 함.
    tscore = TScore.getTScore(returnedResultDictValues)
    cscore = CScore.getCScore(returnedResultDictValues)
    mscore = MScore.getMScore(returnedResultDictValues)




    returnedResultDict.update({'좋아요__사람전체명수': likePushPersonCnt, '좋아요(image)__표시전체갯수': cnt_like_img})


    # T SCORE, C CORE 값을 넘겨 SCM SCORE 산출
    returnedValue_from_method_TCMCountGen = TCMCountGen(t_score_count, c_score_count, returnedResultDict, User_timeLine_site_url_addr, driver)

    if returnedValue_from_method_TCMCountGen == True:
        print('TCM SCORE가 정상 산출 되었습니다.')
        returnedValue_profileTextDataCrawling = True

    elif returnedValue_from_method_TCMCountGen == False:
        print('TCM SCORE가 산출 되지 않았습니다.')
        returnedValue_profileTextDataCrawling = True

    return returnedValue_profileTextDataCrawling


  '''








#function No.01 ###########################################################################
# https://www.facebook.com/userpageID
def getProfileData(User_timeLine_site_url_addr, insertedName, driver):
    profileDic = {}
    fb_tmln_soup= Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, User_timeLine_site_url_addr)

    # get applicant's name
    usernamefromDirect = insertedName

    #이름 일치 여부
    try:
        user_name = fb_tmln_soup.select('#fb-timeline-cover-name > a')[0].text
        print('페이스북 상의 사용자 이름 : ', user_name)
    except:
        print('페이스북 사용자 이름을 가져올 수 없습니다.')
        user_name = usernamefromDirect

    if user_name == usernamefromDirect:
        #print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')
        logger.debug('[이름 일치]facebook user name => {} , 이력서 상의 이름 => {}'.format(user_name, usernamefromDirect))
    else:
        #print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')
        logger.debug('[이름 불-일치]facebook user name => {} , 이력서 상의 이름 => {}'.format(user_name, usernamefromDirect))

    # DATA crawling and parsing part
    # scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    #print('last_height : ', last_height)

    # 페이스북 타임라인 좌측 상단의 프로필(소개글) https://www.facebook.com/facebook_PageID?
    try:
        # 타임라인 프로필 내 소개글 존재 여부
        intro_text_title = fb_tmln_soup.select(
            'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > span')
        if not intro_text_title:
            print('타임라인 프로필 내 소개글이 존재하지 않습니다.')
            logger.debug('타임라인 프로필 내 소개글이 존재하지 않습니다.')
            exist_text_or_not = False
        else:
            print(intro_text_title[0].text)  # 출력 내용 : '소개'

            try:
                # 타임라인 프로필 내 소개글
                intro_text_detail = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div#profile_intro_card_bio > div > div > div > span')
                profileDic['introText'] = intro_text_detail[0].text.replace(' ', '')
            except Exception as ew:
                logger.debug('소개글 게시판 HTML 구조가 변경되어 다시 검색합니다.')
                intro_text_detail2 = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div > div')
                intro_text_detail = intro_text_detail2
                profileDic['introText'] = intro_text_detail[0].text.replace(' ', '')

            logger.debug('타임라인 프로필 내 소개글 => {}'.format(profileDic))

    except Exception as e:
        logger.error('페이스북 타임라인 프로필(소개글)이 존재하지 않습니다.=> {}'.format(e))

    # 페이스북 타임라인 좌측 상단의 프로필(세부 프로필 내용, 공개 여부에 따라 항목 개수가 상이함) https://www.facebook.com/facebook_PageID?
    try:
        profile_list_test_old = fb_tmln_soup.select(
            'div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')
        profile_list_detail_text_01_old = fb_tmln_soup.select(
            'div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')

        lengthOfProfileList = len(profile_list_test_old)
        lengthOfDetailListText = len(profile_list_detail_text_01_old)

        originalHTMLDOMRegion = 'div#intro_container_id > div:nth-of-type(2) >'
        alteredHTMLDOMRegion = 'div#intro_container_id > div:nth-of-type(1) >'

        # DOM 구조 변경에 따른 경로 수정
        if lengthOfProfileList == 0:
            # 경로가 변경되었을 경우, 경로 변경
            profile_list_test = fb_tmln_soup.select(alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            # print('(altered)프로필 영역 개수 ->', len(profile_list_test))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
            logger.debug('공개된 프로필 영역 개수 => {}'.format(len(profile_list_test)))

        else:
            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_test = fb_tmln_soup.select(originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            # print('(original)프로필 영역 개수 ->', len(profile_list_test))
            logger.debug('공개된 프로필 영역 개수 => {}'.format(len(profile_list_test)))

        if lengthOfDetailListText == 0:
            # 경로가 변경되었을 경우, 경로 변경
            profile_list_detail_text_01 = fb_tmln_soup.select(
                alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            # print('(altered) 값 ->', len(profile_list_detail_text_01))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
            logger.debug('문서의 구조 변경이 감지됨.')

        else:
            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_detail_text_01 = fb_tmln_soup.select(
                originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            print('(original)값 ->', len(profile_list_detail_text_01))

        if not profile_list_detail_text_01:
            logger.debug('사용자가 프로필 정보를 등록하지 않았습니다.')
        else:
            logger.debug('프로필 정보 : {}'.format(profile_list_detail_text_01[0].text))

        prf = 0
        try:
            while prf < len(profile_list_test):
                key = '프로필 정보_0' + str(int(prf + 1))
                print('key : ', key)

                value = fb_tmln_soup.select(
                    originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        int(prf + 1)) + ') > div > div > div > div')[0].text.replace(" ", "")
                print('value : ', value)

                logger.debug('{} : {}'.format(key, value))

                profileDic[key] = value
                prf += 1
                # returnedResultList.append(value)
        except:
            logger.debug('더이상 가져올 수 있는 정보가 없습니다.')

    except Exception as e:
        logger.error('프로필 정보 취득 중 오류-> {}'.format(e))

    logger.debug('공개된 프로필 :', profileDic)

    return profileDic



#TCM SCORE 산출
def TCMCountGen(tScoreCount, cScoreCount, ResultDict, user_fbpage_url, driver):

    returnedValue_TCMCountGen = False

    #dictResult ={}
    print('M_SCORE를 산출하겠습니다.')
    userContent_list_result = autoScrollerUserWrapperContents(driver)

    if userContent_list_result is not None:
        totalPicCnt = autoScroller_MSCORE(user_fbpage_url, driver)

        prfl_vodCnt = 0
        prfl_picCnt = 0
        contentCnt = 0

        m_score_count = 0
        m_score_count_detail=0

        # 동영상, 사진 갯수 추출
        for contntLength in range(len(userContent_list_result)):
            try:
                if '동영상을 공유' in userContent_list_result[contntLength].text:
                    #print(contntLength + 1, '.', userContent_list_result[contntLength].text)
                    prfl_vodCnt += 1

                if '사진을 공유' in userContent_list_result[contntLength].text:
                    #print(contntLength + 1, '.', userContent_list_result[contntLength].text)
                    prfl_picCnt += 1

            except TimeoutException as ex:
                print('Timeout Exception', ex)
                break

            contentCnt +=1

        print('동영상수 :', prfl_vodCnt)
        print('사진수 :', totalPicCnt)
        print('게시글(사진, 동영상 포함) 수 : ', len(userContent_list_result))
        print('게시글(사진, 동영상 포함) 수 : ', contentCnt + totalPicCnt)
        print('게시글(텍스트로만 구성) 수 : ', contentCnt - (prfl_picCnt + prfl_vodCnt))


        if totalPicCnt >= 500:
            print('사진 수가 500장 이상일 경우 10점이 가산됩니다.')
            m_score_count_detail += 10
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 200 <= totalPicCnt < 500:
            print('사진 수가 200장 이상 500장 미만일 경우 5점이 가산됩니다.')
            m_score_count_detail += 5
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 10 <= totalPicCnt < 200:
            print('사진 수가 10장 이상 200장 미만일 경우 3점이 가산됩니다.')
            m_score_count_detail += 3
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)

        ResultDict.update({'동영상수':prfl_vodCnt, '사진수':totalPicCnt })

        mScoreCount = m_score_count

        # 게시글 텍스트 크롤링
        autoScrollerContentsText(user_fbpage_url, driver)

        print('최종 T SCORE : ', tScoreCount)
        print('최종 C SCORE : ', cScoreCount)
        print('최종 M SCORE : ', mScoreCount)
        print()

        ResultDict.update({'T_SCORE':tScoreCount, 'C_SCORE':cScoreCount, 'M_SCORE':mScoreCount})

        print('최종 RESULT : ', ResultDict)

        #{'생일': '1985년10월7일',
        # '음력생일': '1985년8월23일',
        # '성별': '남성',
        # '혈액형': 'B형',
        # 'Facebook': 'http://facebook.com/hyoungwoo.kim.zermatt',
        # '프로필 정보_01': '가톨릭대학교서울성모병원에서근무',
        # '프로필 정보_02': '가톨릭대학교의과대학에서공부했음',
        # '프로필 정보_03': '서현고등학교졸업',
        # '친구수': 286,
        # '"좋아요"사람전체명수': 0,
        # '"좋아요(image)"표시전체갯수': 0,
        # '동영상수': 2,
        # '사진수': 316,
        # 'T_SCORE': 40,
        # 'C_SCORE': 8,
        # 'M_SCORE': 5}

        returnedValue_TCMCountGen = True

    else:
        print('M Score를 산출할 수 없습니다.')

        ResultDict.update({'T_SCORE': tScoreCount, 'C_SCORE': cScoreCount, 'M_SCORE': 0})

    # 20180509 _0510
    # 가공 데이터 CSV 파일화 작업
    currDate = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
        time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(
        time.localtime().tm_sec)
    '''
    # DB Connection=======================================
    #return_DBconn_result = MongoDB collection name
    return_DBconn_result = mongoDB_conn.MongoDB_CRUD.mngDB_connection(hereWork)

    #mngDB_INSERT(hereWork, userSNS_URL, userSNS_dictionaryTypeData, currDate, collectionName_SNS):
    mongoDB_conn.MongoDB_CRUD.mngDB_INSERT(hereWork, user_fbpage_url, ResultDict, currDate, return_DBconn_result)
    '''

    with open("C:\python_project\just_project\PycharmProjects\CrawledData_"+ hereWork +"_" + currDate + ".csv", "w", newline='') as fbFile:

        # 20180509
        # kakaoStory_userInfo ==> dictionary type
        # with open("C:\python_project\just_project\PycharmProjects\kakaoStory_CrawledData_donyangOnline_"+currDate+".csv", "w") as kksFile:
        writer = csv.writer(fbFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([str(user_fbpage_url + '님의 페이스북 정보 근거 TCM 산출 정보')])

        for key, val in ResultDict.items():
            writer.writerow([key, val])

        writer.writerow([])

    # 20180509
    #생성한 CSV 파일 읽기 - 정상 입력 검사
    with open("C:\python_project\just_project\PycharmProjects\CrawledData_"+ hereWork +"_" + currDate + ".csv", "r") as readCSVfile:
        reader = csv.reader(readCSVfile)

        # read file row by row
        for row in reader:
            print(row)

    return returnedValue_TCMCountGen



def autoScrollerUserWrapperContents(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')
        userContent_list_result = []

    try:
        time.sleep(0.5)
        userContent_list_result = autoScrolled_data_soup_html.find_all('div', attrs={'class': 'userContentWrapper'})

    except Exception as e:
        print('autoScrollerUserWrapperContents에서 userContentWrapper를 찾지 못했습니다. -> ', e)
        userContent_list_result is None

    return userContent_list_result




def autoScroller_MSCORE(User_site_url_addr, driver):
    driver.get(User_site_url_addr + '/photos_albums')

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    userContent_list_result = []

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup = bs(autoScrolled_data, 'html.parser')
        try:

            userContent_list_result = autoScrolled_data_soup.find_all('span', attrs={'class': '_2ieq _50f7'})
        except:
            print('해당 클래스 값이 없습니다.')

    pictureCntT = 0
    pictureCnt = 0
    for picture_index in userContent_list_result:
        pictureDiscribText = picture_index.text.split(' · ')

        matching = [s for s in pictureDiscribText if "항목" in s]
        pictureCnt = int(str(matching).split()[1].split('개')[0])

        pictureCntT += pictureCnt
    print('총 사진 수 : ', pictureCntT)

    return pictureCntT



#autoScroller관련 함수 =========================================================================

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')

    #return bs(autoScrolled_data, 'html.parser')
    return autoScrolled_data_soup_html



def autoScrollerContentsText(User_timeLine_site_url_addr, driver):

    driver.get(User_timeLine_site_url_addr)
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    textDataList = []
    userContent_list_result = ''
    autoScrolled_data_soup = ''
    for cyc in range(0, 10):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup = bs(autoScrolled_data, 'html.parser')

    try:
        userContent_list_result = autoScrolled_data_soup.find_all('div',attrs={'class': '_5pbx userContent _3576'})
        #print('@@', userContent_list_result)
        for textOnly in userContent_list_result:
            textData = textOnly.text.split()
            #print('###',textData)
            textDataList += textData
        print('textDataList :', textDataList)

        #print(sys.getsizeof(textDataList)) #Return the size of object in bytes.

        corp = {}
        textDataListVal = ''
        samsung_cnt = 0
        lg_cnt = 0
        hd_cnt = 0
        kia_cnt = 0
        sk_cnt = 0
        hankook_cnt = 0
        kt_cnt = 0
        gs_cnt = 0
        shinhan_cnt = 0
        hana_cnt = 0
        hanhwa_cnt = 0
        woori_cnt = 0
        daewoo_cnt = 0
        doosan_cnt = 0
        lotte_cnt = 0
        kb_cnt = 0
        hkook_cnt = 0
        ibk_cnt = 0
        soil_cnt = 0
        korean_cnt = 0
        asiana_cnt = 0
        dongkook_cnt = 0
        kolon_cnt = 0
        naver_cnt = 0
        daum_cnt = 0
        corpmem_cnt = 0

        try:
            if '엘지' in textDataList:
                print('엘지(이)라는 글자가 노출되었습니다')
                lg_cnt += 1
                textDataListVal += textDataList

            if '현대' in textDataList:
                print('현대(이)라는 글자가 노출되었습니다')
                hd_cnt += 1
                textDataListVal += textDataList

            if '기아' in textDataList:
                print('기아(이)라는 글자가 노출되었습니다')
                kia_cnt += 1
                textDataListVal += textDataList

            if '삼성' in textDataList:
                print('삼성(이)라는 글자가 노출되었습니다.')
                samsung_cnt += 1
                textDataListVal += textDataList

            if '에스케이' in textDataList:
                print('에스케이(이)라는 글자가 노출되었습니다')
                sk_cnt += 1
                textDataListVal += textDataList

            if '한국' in textDataList:
                print('한국(이)라는 글자가 노출되었습니다')
                hankook_cnt += 1
                textDataListVal += textDataList

            if '케이티' in textDataList:
                print('케이티(이)라는 글자가 노출되었습니다')
                kt_cnt += 1
                textDataListVal += textDataList

            if '지에스' in textDataList:
                print('지에스(이)라는 글자가 노출되었습니다')
                gs_cnt += 1
                textDataListVal += textDataList

            if '신한' in textDataList:
                print('신한(이)라는 글자가 노출되었습니다')
                shinhan_cnt += 1
                textDataListVal += textDataList

            if '하나' in textDataList:
                print('하나(이)라는 글자가 노출되었습니다')
                hana_cnt += 1
                textDataListVal += textDataList

            if '한화' in textDataList:
                print('한화(이)라는 글자가 노출되었습니다')
                hanhwa_cnt += 1
                textDataListVal += textDataList

            if '우리' in textDataList:
                print('우리(이)라는 글자가 노출되었습니다')
                woori_cnt += 1
                textDataListVal += textDataList

            if '대우' in textDataList:
                print('대우(이)라는 글자가 노출되었습니다')
                daewoo_cnt += 1
                textDataListVal += textDataList

            if '두산' in textDataList:
                print('두산(이)라는 글자가 노출되었습니다')
                doosan_cnt += 1
                textDataListVal += textDataList

            if '롯데' in textDataList:
                print('롯데(이)라는 글자가 노출되었습니다')
                lotte_cnt += 1
                textDataListVal += textDataList

            if '케이비' in textDataList:
                print('케이비(이)라는 글자가 노출되었습니다')
                kb_cnt += 1
                textDataListVal += textDataList

            if '흥국' in textDataList:
                print('흥국(이)라는 글자가 노출되었습니다')
                hkook_cnt += 1
                textDataListVal += textDataList

            if '기업' in textDataList:
                print('기업(이)라는 글자가 노출되었습니다')
                ibk_cnt += 1
                textDataListVal += textDataList

            if 'S-oil' in textDataList:
                print('s-oil(이)라는 글자가 노출되었습니다')
                soil_cnt += 1
                textDataListVal += textDataList

            if '대한' in textDataList:
                print('대한(이)라는 글자가 노출되었습니다')
                korean_cnt += 1
                textDataListVal += textDataList

            if '아시아나' in textDataList:
                print('아시아나(이)라는 글자가 노출되었습니다')
                asiana_cnt += 1
                textDataListVal += textDataList

            if '동국' in textDataList:
                print('동국(이)라는 글자가 노출되었습니다')
                dongkook_cnt += 1
                textDataListVal += textDataList

            if '코오롱' in textDataList:
                print('코오롱(이)라는 글자가 노출되었습니다')
                kolon_cnt += 1
                textDataListVal += textDataList

            if '네이버' in textDataList:
                print('네이버(이)라는 글자가 노출되었습니다')
                naver_cnt += 1
                textDataListVal += textDataList

            if '다음' in textDataList:
                print('다음(이)라는 글자가 노출되었습니다')
                daum_cnt += 1
                textDataListVal += textDataList

            if '사원' in textDataList:
                print('사원증(이)라는 글자가 노출되었습니다.')
                corpmem_cnt += 1
                textDataListVal += textDataList

            print('textDataListVal', textDataListVal)
            readCSV(textDataListVal)

        except Exception as es:
            print('기업 이름이 검색되지 않았습니다. : ', es)
            textDataListVal = ''

    except Exception as readCsvEx:
        print('AutoCrolling 한 객체가 없습니다. ')




#CSV 파일 읽기 ======================================================================
def readCSV(listValue):

    resultList = []
    with open('C:\\python_project\\just_project\\PycharmProjects\\1_500Corp.csv', 'rt', encoding='utf-8') as csvCorpNameFile:
        # reader = csv.DictReader(csvCorpNameFile)
        reader = csv.reader(csvCorpNameFile, delimiter=',')
        matchedCnt = 0

        for row in reader:
            if row[1].strip() == listValue:
                resultList.append(listValue)

        print('##', resultList)