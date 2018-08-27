#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import logging.handlers
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    mysqlConnection_jeniel


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
fileHandler = logging.handlers.RotatingFileHandler('C://python_project/aster879_project/PycharmProjects/log/' + hereWork + 'crawlerbot_logging_' + currTime, maxBytes=file_max_bytes, backupCount=10)
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

def __getHTMLDoc_beautifulSoup4(driver, URL):

    driver.get(URL)

    html_src_chrome = driver.page_source
    soupHTMLDoc = bs(html_src_chrome, 'html.parser')

    return soupHTMLDoc



def autoScrollerContentsPhotoText(url_addr, driver):

    driver.get('https://www.facebook.com/'+ url_addr + '/photos_all')
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    html_detail_fb_chrome = ''

    for cyc in range(0, 5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        html_detail_fb_chrome = html_detail_fb_chrome + driver.page_source

    detail_fb_info_soup = bs(html_detail_fb_chrome, 'html.parser')

    #print('@@', detail_fb_info_soup.select('#pagelet_timeline_medley_photos > div:nth-of-type(2) > div > ul > li')[0].attrs)
    #print('@@', len(detail_fb_info_soup.select('#pagelet_timeline_medley_photos > div:nth-of-type(2) > div > ul > li') ) )
    try:
        likeCnt_int = 0
        commentCont_int = 0
        for lngth  in range(len(detail_fb_info_soup.select('#pagelet_timeline_medley_photos > div:nth-of-type(2) > div > ul > li'))):

            try:
                likeCnt_str = detail_fb_info_soup.select('#pagelet_timeline_medley_photos > div:nth-of-type(2) > div > ul > li:nth-of-type('+ str(lngth +1)+') > div > div:nth-of-type(2) > div > a:nth-of-type(4) > div > div:nth-of-type(1) > div:nth-of-type(2)')[0].text
                #print('likeCnt :', likeCnt_str)
                likeCnt_int += int(likeCnt_str)
                #print('Total Like Cnt :', likeCnt_int)

                commentCont_str = detail_fb_info_soup.select('#pagelet_timeline_medley_photos > div:nth-of-type(2) > div > ul > li:nth-of-type('+ str(lngth +1)+') > div > div:nth-of-type(2) > div > a:nth-of-type(4) > div > div:nth-of-type(2) > div:nth-of-type(2)')[0].text
                #print('commentCont_str :', commentCont_str)
                commentCont_int += int(commentCont_str)




            except Exception as e:
                print('더이상 좋아요 또는 댓글 표시가 없습니다.', e)

        print('총 좋아요 수 :', likeCnt_int)
        print('총 댓글 수 :', commentCont_int)

        # update_PhotoLikeCmntCnt(댓글수, 좋아요수, 페이브북아이디)
        databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
        databaseConnection_jeniel.update_PhotoLikeCmntCnt(str(commentCont_int), str(likeCnt_int), url_addr)


    except Exception as e:
        print('HTML 구조가 변경되어 다시 시도하여야 합니다. ')




def autoScroller2(driver, URL):

    driver.get(URL)

    print(driver.current_url)
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 2
    #2초가 페이지 로딩에 안정적인 대기시간이다. 사실 매우 느리다.

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''

    last_height = driver.execute_script("return document.body.scrollHeight")
    #print('last_height : ', last_height)
    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 15):

        #print('@ : ', cyc)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        #print('new_height : ', new_height)

        if new_height == last_height:
            #print('같다고?')
            print()
            break
        last_height = new_height
        #print('값 대입해')

        # autoScroll crawling data 가져오기
        autoScrolled_data_soup = bs(driver.page_source, 'html.parser')

    return autoScrolled_data_soup



def readCSV_goodExpressions():
    print('1')

    #C:\python_project\aster879_project\PycharmProjects
    reader = csv.reader( open('C:\\dev_syhan\\aster_jeniel_test_dev_201808\\긍정어4.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|' )
    #'rt', encoding='utf-8-sig' 로 설정을 해야 1번째 CSV 값앞에 UTF-8로 인코딩한 헤더(\ufeff)가 나타나지 않는다.
    #print('reader:', reader)

    wordList = []

    try:
        for row in reader:
            #print(row)
            wordList.append(', '.join(row))
        #print('긍정어 wordList : ', wordList)

    except Exception as e:
        print(e)

    return wordList






def login_facebook(self, loginCnt, userFacebookPageId, insertedUserName, requestClient):
    start_time_all = time.time()

    returnValue_facebook = False

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {}
    prefs['profile.default_content_setting_values.notifications'] = 2
    chrome_options.add_experimental_option('prefs', prefs)
    driver_chrome = r"C:\python_project\aster879_project\PycharmProjects\chromedriver.exe"

    # go to Google and click the I'm Feeling Lucky button
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)

    # url
    driver.get('https://www.facebook.com')

    user_id = '01027746254'
    user_pass = 'Gkstkddbs4$'

    #user_id ='daramrec@naver.com'
    #user_pass = 'gwanwoo777'

    # id and password
    driver.find_element_by_name('email').send_keys(user_id)
    driver.find_element_by_name('pass').send_keys(user_pass)

    # try login : 로그인 버튼의 id 값이 아래의 범위 내에서 무작위로 변경되기 때문에 이에 대한 대응차원임.
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
                        driver.find_element_by_xpath('// *[ @ id = "u_0_b"]').click()
                        login_or_not = True
                    except Exception as ex5:
                        print('로그인 버튼 id 값이 u_0_b 가 아닙니다.', ex5)
                        login_or_not = False

    loginCnt += 1
    # calling next Function
    user_facebook_page_id = userFacebookPageId

    # for test user facebook page id
    directlyTypedUserName = insertedUserName

    print('driver.current_url : ', driver.current_url)
    returnedValue_from_method = profileTextDataCrawling(login_or_not, loginCnt, user_facebook_page_id, directlyTypedUserName, driver, requestClient)

    if returnedValue_from_method['trueOrFalse'] == True:
        returnValue_facebook = True

    end_time = time.time() - start_time_all
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)

    driver.close()

    #처음 호출한 웹서버에 리턴
    return returnedValue_from_method



def profileTextDataCrawling(loginValue, lgnCnt, insertedUser_fbpage_id, insertedUserName, driver, requestClient):
    returnedValue_profileTextDataCrawling = False
    profileDic = {}
    detailInfo = []


    if (loginValue == False):

        if (lgnCnt > 3):
            print('페이스북 로그인에 최종 실패하여, 사용자 정보 크롤링이 불가합니다.')
            driver.close()
        else:
            print('프로그램을 중지하시고, 페이스북 로그인 정보를 다시 확인하시기 바랍니다.')
            login_facebook(lgnCnt)

    elif (loginValue == True):
        print('login success!')

    user_fbpage_id = insertedUser_fbpage_id
    User_timeLine_site_url_addr = 'https://www.facebook.com/' + user_fbpage_id

    #returnedResultList = getDetailInfoListType(user_fbpage_id, driver, lgnCnt, insertedUserName)
    #print('미리 취득한 사용자 세부 데이터 -> ', returnedResultList)

    #timeline_sticky_header_container : 상단의 '최근'을 클릭하여 운영년도를 알 수 있다.




    # No.1 -> 세부정보 선 취득_Dictionary type :
    returnedResultDict = getDetailInfoDictionaryType(user_fbpage_id, driver, lgnCnt, insertedUserName, requestClient)
    print('사용자 페이스북 상의 세부 데이터 -> ', returnedResultDict)

    returnedResultDict['사용자이름'] = '',
    returnedResultDict['페이스북페이지ID'] = '',

    returnedResultDict['전체연락처정보'] = '',
    returnedResultDict['웹사이트및소셜링크정보'] = '',
    returnedResultDict['소개글'] = '',
    returnedResultDict['프로필게시개수'] = 0,
    returnedResultDict['전체프로필정보'] = '',
    returnedResultDict['친구수'] = 0,
    returnedResultDict['좋아요__사람전체명수']=0,
    returnedResultDict['좋아요(image)__표시전체갯수']=0,
    returnedResultDict['동영상수']=0,
    returnedResultDict['사진수']=0



    # wait for loading & set(alter) driver's url
    driver.get(User_timeLine_site_url_addr)

    # get page source in raw state
    html_src_chrome = driver.page_source

    # beautifulsoup4 initialization :  get the page source in soup type(like text).
    fb_tmln_soup = bs(html_src_chrome, 'html.parser')

    # get applicant's name
    usernamefromDirect = insertedUserName

    profileDic['페이스북페이지ID'] = user_fbpage_id
    detailInfo.append('페이스북페이지ID:'+user_fbpage_id)

    try:
        user_name = fb_tmln_soup.select('#fb-timeline-cover-name > a')[0].text
        print('페이스북 상의 사용자 이름 : ', user_name)
        profileDic['사용자이름'] = user_name

        detailInfo.append('@사용자이름:' + user_name)

    except:
        print('페이스북 사용자 이름을 가져올 수 없습니다.')
        user_name = usernamefromDirect
        profileDic['사용자이름'] = user_name

        detailInfo.append('@사용자이름:' + user_name)

    if user_name == usernamefromDirect:
        print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')

        detailInfo.append('@페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')

    else:
        print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')

        detailInfo.append('@페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')

    # DATA crawling and parsing part
    # Got scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 소개 글
    try:
        # 해당 글 영역 존재 여부
        intro_text_title = fb_tmln_soup.select(
            'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > span')
        if not intro_text_title:
            print('소개글 영역이 존재하지 않습니다.')
            exist_text_or_not = False
        else:
            print(intro_text_title[0].text)  # '소개'

            try:
                # 소개글
                intro_text_detail = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div#profile_intro_card_bio > div > div > div > span')
                print('소개글 : ', intro_text_detail[0].text)
                #returnedResultList.append(intro_text_detail[0].text.replace(' ', ''))
                profileDic['소개글'] = intro_text_detail[0].text.replace(' ', '')

                detailInfo.append('@'.join(profileDic['소개글']))


            except Exception as ew:
                print("소개글 게시판 HTML 구조가 변경되어 다시 검색합니다. --> ", ew)

                intro_text_detail2 = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div > div')
                intro_text_detail = intro_text_detail2
                print('소개글 : ', intro_text_detail[0].text)
                #returnedResultList.append(intro_text_detail[0].text.replace(' ', ''))
                profileDic['소개글'] = intro_text_detail[0].text.replace(' ', '')

                detailInfo.append('@'.join(profileDic['소개글']))


            print('1차 dictionary 결과물 출력 -> ', profileDic)
    except Exception as e:
        print('[소개글]게시된 소개글의 값들이 존재하지 않습니다.-> ', e)

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
            print('(altered)프로필 영역 개수 ->', len(profile_list_test))
            profileDic['프로필게시개수'] = str(len(profile_list_test))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
        else:

            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_test = fb_tmln_soup.select(originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            print('(original)프로필 영역 개수 ->', len(profile_list_test))
            profileDic['프로필게시개수'] = str(len(profile_list_test))

        if lengthOfDetailListText == 0:

            # 경로가 변경되었을 경우, 경로 변경
            profile_list_detail_text_01 = fb_tmln_soup.select(
                alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            print('(altered) 값 ->', len(profile_list_detail_text_01))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
        else:

            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_detail_text_01 = fb_tmln_soup.select(
                originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            print('(original)값 ->', len(profile_list_detail_text_01))

        if not profile_list_detail_text_01:

            print('사용자가 프로필 정보를 등록하지 않았습니다.')
        else:
            print('프로필 정보_01 :', profile_list_detail_text_01[0].text)
            #returnedResultList.append(profile_list_detail_text_01[0].text.replace(' ', ''))
            #returnedResultDict['프로필 정보 No.01'] = profile_list_detail_text_01[0].text.replace(' ', '')


        profileDataList = []
        prf = 0
        try:
            while prf < len(profile_list_test):
                key = '프로필정보_0' + str(int(prf + 1))
                print('key : ', key)

                value = fb_tmln_soup.select(
                    originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        int(prf + 1)) + ') > div > div > div > div')[0].text.replace(" ", "")
                print('value : ', value)

                profileDic[key] = value
                profileDataList.append(value)

                prf += 1

            detailInfo = detailInfo + profileDataList
            profileDic['전체프로필정보'] = '_'.join(profileDataList)


        except:
            print('더이상 가져올 수 있는 정보가 없습니다.')
        print('프로필 정보 [Dictionary type] :', profileDic)
        #print('프로필 정보 사이즈 [Dictionary type] :', len(profileDic))

        returnedResultDict = dict(returnedResultDict, **profileDic)
    except Exception as e:
        print('프로필 정보 취득 중 오류-> ', e)

    #print('결과 [List type]: ', returnedResultList)
    print('@@@@@_결과 [Dictionary type]: ', returnedResultDict)


    tcm_score = {}

    # 대상자의 현재 거주지 또는 출신학교 소재지
    t_score_count = 0
    c_score_count = 0

    t_score_count_detail = 0
    c_score_count_detail = 0




    #20180810

    # [개요]

    returnedResultDict['개요항목개수'] = 0
    detail_url_overview = 'https://www.facebook.com/'+ user_fbpage_id +'/about?section=overview'
    detail_fb_overview_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_overview)

    about_overviewURL = '#pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div'

    try:
        aboutOverview_middle_lists = detail_fb_overview_info_soup.select(
            about_overviewURL + ' > div:nth-of-type(1) > ul > li')
        # 개요 항목의 리스트 개수
        print('개요항목길이:', len(aboutOverview_middle_lists))

        returnedResultDict['개요항목개수'] = len(aboutOverview_middle_lists)

        # 개요 항목 리스트 추출
        for about_list in range(len(aboutOverview_middle_lists)):
            print(aboutOverview_middle_lists[about_list].text)
            # 여기서의 구체적인 값들은 '개요'가 아닌 각 큰 카테고리내에서 개별 선별 해야 함.

    except Exception as e:
        print('개요 항목이 존재하지 않음.', e)

    print('##############################################################')

    try:
        aboutOverview_rightSide_lists = detail_fb_overview_info_soup.select(
            about_overviewURL + ' > div:nth-of-type(2) > ul > li')
        # 개요 항목 우측의 리스트 개수
        # print(len(aboutOverview_rightSide_lists))
        # 개요 항목 우측 리스트 추출
        for about_list_right in range(len(aboutOverview_rightSide_lists)):
            # 우측 리스트의 제목
            # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(1)
            title_aboutPage_list_right = detail_fb_overview_info_soup.select(
                about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                    about_list_right + 1) + ') > div > div:nth-of-type(2) > span > div:nth-of-type(1)')

            # 우측 리스트의 내용
            # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(2)
            contents_aboutPage_list_right = detail_fb_overview_info_soup.select(
                about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                    about_list_right + 1) + ') > div > div:nth-of-type(2) > span > div:nth-of-type(2)')

            # print(aboutOverview_rightSide_lists[about_list_right].text)
            print(title_aboutPage_list_right[0].text)
            print(contents_aboutPage_list_right[0].text)

    except Exception as e:
        print('개요의 우측 항목이 존재하지 않음.', e)

    # [경력 및 학력]
    # https://www.facebook.com/kpokem/about?section=education
    detail_url_education = 'https://www.facebook.com/'+ user_fbpage_id + 'about?section=education'
    detail_fb_education_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_education)
    # about_educationURL = '#pagelet_eduwork > div > div'
    aboutEducation_lists = detail_fb_education_info_soup.select('#pagelet_eduwork > div > div')
    # print(len(aboutEducation_lists))

    for about_length_of_education_list in range(len(aboutEducation_lists)):
        work_history_lists_title = detail_fb_education_info_soup.select(
            '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > div > span')[
            0].text

        print(work_history_lists_title)  # 직장/전문기술/학력

        if '전문 기술' in work_history_lists_title:

            # print(work_history_lists_title, '길이: 1')
            work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(
                about_length_of_education_list + 1) + ') > ul > li > div'
            work_history_lists = detail_fb_education_info_soup.select(work_history_lists_dir)

            print(work_history_lists_title, '길이: ', len(work_history_lists))

            print(work_history_lists[0].text)

        else:
            # print('else:', len(aboutEducation_lists))
            work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(
                about_length_of_education_list + 1) + ') > ul > li'
            work_history_lists = detail_fb_education_info_soup.select(work_history_lists_dir)
            for about_length_of_edu_detail in range(len(work_history_lists)):
                print(work_history_lists_title, '길이: ', len(work_history_lists))
                print('@', detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                    about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text)

                print('@', detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                    about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[
                    0].text)

    # [거주했던 장소]
    # https://www.facebook.com/kpokem/about?section=living
    detail_url_living = 'https://www.facebook.com/'+ user_fbpage_id +'/about?section=living'
    detail_fb_living_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_living)
    aboutLiving_lists = detail_fb_living_info_soup.select('#pagelet_hometown > div > div')

    for about_length_of_living_list in range(len(aboutLiving_lists)):
        # print('about_length_of_living_list : ', about_length_of_living_list)
        living_history_lists_title = detail_fb_living_info_soup.select(
            '#pagelet_hometown > div > div:nth-of-type(' + str(about_length_of_living_list + 1) + ') > div > span')[
            0].text

        print('living_history_lists_title : ', living_history_lists_title)  # 거주지와 출신지/기타 살았던 곳/거주지

        living_history_lists_dir = '#pagelet_hometown > div > div:nth-of-type(' + str(
            about_length_of_living_list + 1) + ') > ul > li'
        living_history_lists = detail_fb_living_info_soup.select(living_history_lists_dir)

        if '거주지' in living_history_lists_title:
            if len(living_history_lists) == 1:
                print('거주지 출력 부분은 구조가 1 depth 깊음')

                for about_length_of_living_detail in range(len(living_history_lists)):
                    print('len(living_history_lists) : ', len(living_history_lists))
                    print(detail_fb_living_info_soup.select(
                        living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > span > a')[
                              0].text)
                    print(detail_fb_living_info_soup.select(
                        living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)

            else:
                print('거주지 출력 부분은 구조가 1 depth 깊음')
                for about_length_of_living_detail in range(len(living_history_lists)):
                    print('len(living_history_lists) : ', len(living_history_lists))
                    print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(
                        about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[
                              0].text)
                    print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(
                        about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[
                              0].text)

        else:
            if len(living_history_lists) == 1:

                for about_length_of_living_detail in range(len(living_history_lists)):
                    print('len(living_history_lists) : ', len(living_history_lists))
                    print(detail_fb_living_info_soup.select(
                        living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                    print(detail_fb_living_info_soup.select(
                        living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text)

            else:
                for about_length_of_living_detail in range(len(living_history_lists)):
                    print('len(living_history_lists) : ', len(living_history_lists))
                    print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(
                        about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[
                              0].text)
                    print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(
                        about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[
                              0].text)

        # No.4 [연락처 및 기본정보]-연락처 정보, 웹사이트 및 소셜 링크 정보, 기본 정보
        # https://www.facebook.com/userpageID/about?section=contact-info
        detail_url_contact = 'https://www.facebook.com/'+ user_fbpage_id + '/about?section=contact-info&pnref=about'
        detail_fb_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_contact)

        # [연락처 및 기본정보]-[연락처 정보]란 제목
        user_pglet_contactData_title_01 = detail_fb_info_soup.select(
            '#pagelet_contact > div > div:nth-of-type(1) > div > span')

        # [연락처 및 기본정보]-[웹사이트 및 소셜 링크]란 제목
        user_pglet_contactData_title_01_2 = detail_fb_info_soup.select(
            '#pagelet_contact > div > div:nth-of-type(2) > div > div > span')

        # [연락처 및 기본정보]-[기본 정보]란 제목
        user_pglet_basicData_title_01 = detail_fb_info_soup.select(
            '#pagelet_basic > div > div > span')

        user_pglet_data = detail_fb_info_soup.select('div#pagelet_contact > div > div')[0].text
        print('user_pglet_data = {}'.format(user_pglet_data))

        length_user_pglet_data = len(user_pglet_data)

        print('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : {}'.format(length_user_pglet_data))

        # [연락처 정보]란 취득
        if not user_pglet_contactData_title_01:
            print('사용자가 연락처 정보를 등록하지 않았습니다.')

            # make Data
            # aboutDataDic[user_pglet_contactData_title_01.replace(" ", "")] = ''

        else:
            # pagelet_contact
            if '연락처' in user_pglet_contactData_title_01[0].text:
                print(user_pglet_contactData_title_01[0].text)  # 연락처 정보

                # [연락처 정보]란 하단 세부 정보 타이틀
                pagelet_contact_dir_list = 'div#pagelet_contact > div > div:nth-of-type(1) > ul > li'

                # [연락처 정보]란 하단 세부 정보 타이틀 갯수
                length_of_contList = len(detail_fb_info_soup.select(pagelet_contact_dir_list))

                # [연락처 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conCycle = 0
                try:
                    # 하단 세부 정보 길이 만큼 반복문 실행해 key:value 생성
                    while conCycle < length_of_contList:
                        userContactInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_dir_list + ':nth-of-type(' + str(
                                int(conCycle + 1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [연락처 정보]란_title
                        key = userContactInfoListTitle.replace(" ", "")
                        print('연락처 정보_title: ', key)

                        # [연락처 정보]란_value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_dir_list + ':nth-of-type(' + str(
                                int(conCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[
                            0].text.replace(" ", "")
                        print('연락처 정보_value: ', value)

                        # make Data
                        # aboutDataDic[key] = value

                        # aboutInfo[key] = value
                        conCycle += 1

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    # print('연락처 정보 수집 결과[Dictionary type]:', aboutInfo)

        # [웹사이트 및 소셜 링크]란
        if not user_pglet_contactData_title_01_2:
            print('사용자가 웹사이트 및 소셜 링크 정보를 등록하지 않았습니다.')

            # make Data
            # aboutDataDic[user_pglet_contactData_title_01_2.replace(" ", "")] = ''
        else:
            # pagelet_contact
            if '웹사이트' in user_pglet_contactData_title_01_2[0].text:
                print(user_pglet_contactData_title_01_2[0].text)  # 웹사이트 및 소셜 링크 정보

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀
                pagelet_contact_webSite_dir_list = 'div#pagelet_contact > div > div:nth-of-type(2) > div > ul > li'

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀 갯수
                length_of_contWebSiteList = len(detail_fb_info_soup.select(pagelet_contact_webSite_dir_list))

                # [웹사이트 및 소셜 링크]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conWebCycle = 0

                try:
                    while conWebCycle < length_of_contWebSiteList:
                        userContactWebInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list + ':nth-of-type(' + str(
                                int(conWebCycle + 1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [웹사이트 및 소셜 링크]란 title
                        key = userContactWebInfoListTitle.replace(" ", "")
                        print('웹사이트 및 소셜 링크 정보_title: ', key)

                        # [웹사이트 및 소셜 링크]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list + ':nth-of-type(' + str(
                                int(conWebCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[
                            0].text.replace(" ", "")

                        print('웹사이트 및 소셜 링크 정보_value: ', value)

                        # make Data
                        # aboutDataDic[key] = value

                        # aboutInfo[key] = value
                        conWebCycle += 1

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    # logger.debug('웹사이트 및 소셜 링크 정보 수집 결과[Dictionary type]: {}'.format(aboutDataDic))

        # [기본 정보]란 취득
        if not user_pglet_basicData_title_01:
            print('사용자가 기본 정보를 등록하지 않았습니다.')

            # make Data
            # aboutDataDic[user_pglet_basicData_title_01.replace(" ", "")] = ''

        else:
            # pagelet_basic
            if '기본' in user_pglet_basicData_title_01[0].text:
                print(user_pglet_basicData_title_01[0].text)  # 기본 정보

                # [기본 정보]란 하단 세부 정보 타이틀
                pagelet_basic_dir_list = 'div#pagelet_basic > div > ul > li'

                # [기본 정보]란 하단 세부 정보 타이틀 갯수
                length_of_basicList = len(detail_fb_info_soup.select(pagelet_basic_dir_list))

                # [기본 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                baseCycle = 0
                try:
                    while baseCycle < length_of_basicList:
                        userBasicInfoListTitle = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle + 1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [기본 정보]란 title
                        key = userBasicInfoListTitle.replace(" ", "")

                        print('기본 정보_key : ', key)

                        # [기본 정보]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[
                            0].text.replace(" ", "")

                        print('기본 정보_value : ', value)

                        # make Data
                        # aboutDataDic[key] = value

                        baseCycle += 1

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    # print('기본 정보 수집 결과 [Dictionary type]: {}'.format(aboutDataDic))

    # [가족 및 결혼/연애 상태]
    # https://www.facebook.com/kpokem/about?section=relationship
    detail_url_relationship = 'https://www.facebook.com/' + user_fbpage_id + '/about?section=relationship'
    detail_fb_relationship_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_relationship)
    aboutRelationship_lists = detail_fb_relationship_info_soup.select('#pagelet_relationships > div')

    for about_length_of_Relationships_list in range(len(aboutRelationship_lists)):

        try:
            # 결혼/연애 상태
            relationship_marriage_status_title = detail_fb_relationship_info_soup.select(
                '#pagelet_relationships > div:nth-of-type(' + str(
                    about_length_of_Relationships_list + 1) + ') > div > span')[0].text
            print('relationship_marriage_status_title : ', relationship_marriage_status_title)

            relationship_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(
                about_length_of_Relationships_list + 1) + ') > ul > li'

            relationship_lists = detail_fb_relationship_info_soup.select(relationship_lists_dir)
            # print('##', len(relationship_lists))

            if len(relationship_lists) == 1:
                try:
                    # 결혼/연애상태의 대상자가 존재할 때
                    relationship_list_name = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                        0].text
                    relationship_list_status = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                        0].text
                    print('relationship name & status : ', relationship_list_name, ', ', relationship_list_status)
                except Exception:
                    # 결혼/연애상태의 대상자가 존재하지 않을 때
                    relationship_list_name = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(1) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > span')[
                        0].text
                    print('relationship name : ', relationship_list_name)
            else:
                # 결혼/연애상태의 대상자 수가 복수일 때
                for length_lists in range(len(relationship_lists)):
                    relationship_list_name = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(' + str(
                            length_lists + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                        0].text
                    relationship_list_status = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(' + str(
                            length_lists + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                        0].text
                    print('relationship name & status : ', relationship_list_name, ', ', relationship_list_status)


        except Exception:
            # 가족
            relationship_family_status_title = detail_fb_relationship_info_soup.select(
                '#pagelet_relationships > div:nth-of-type(' + str(
                    about_length_of_Relationships_list + 1) + ') > div > div > span')[0].text
            print('relationship_family_status_title : ', relationship_family_status_title)

            relationship_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(
                about_length_of_Relationships_list + 1) + ') > div > ul > li'
            relationship_lists = detail_fb_relationship_info_soup.select(relationship_lists_dir)

            if len(relationship_lists) == 1:
                relationship_list_name = detail_fb_relationship_info_soup.select(
                    relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                    0].text
                relationship_list_staus = detail_fb_relationship_info_soup.select(
                    relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                    0].text
                print('relationship name & status : ', relationship_list_name, ', ', relationship_list_status)
            else:
                for length_lists in range(len(relationship_lists)):
                    relationship_list_name = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(' + str(
                            length_lists + 1) + ') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > span > a')[
                        0].text
                    relationship_list_status = detail_fb_relationship_info_soup.select(
                        relationship_lists_dir + ':nth-of-type(' + str(
                            length_lists + 1) + ') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                        0].text
                    print('relationship name & status : ', relationship_list_name, ', ', relationship_list_status)

    # [자세한 소개]
    # https://www.facebook.com/kpokem/about?section=bio
    detail_url_bio = 'https://www.facebook.com/' + user_fbpage_id + '/about?section=bio'
    detail_fb_bio_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_bio)

    # bio와 Quotes는 기본으로 출력함
    about_Bio_title = detail_fb_bio_info_soup.select('#pagelet_bio > div > div > span')[0].text  # 누구누구님의 정보
    about_Bio_contents = detail_fb_bio_info_soup.select('#pagelet_bio > div > ul > li > span')[
        0].text  # 내용 또는 표시할 추가 정보 없음
    print('bio : ', about_Bio_title, ', ', about_Bio_contents)

    try:
        about_Pronounce = detail_fb_bio_info_soup.select('#pagelet_pronounce')
    except Exception as e:
        print('pagelet_pronounce 정보가 없습니다.')

    try:
        about_nicknames = detail_fb_bio_info_soup.select('#pagelet_nicknames')
    except Exception as e:
        print('pagelet_nicknames 정보가 없습니다. ')


    about_Quotes_title = ''
    about_Quotes_contents = ''

    try:
        # bio와 Quotes는 기본으로 출력함
        about_Quotes_title = detail_fb_bio_info_soup.select('#pagelet_quotes > div > div > span')[0].text
    except Exception as e:
        print('bio와 Quotes는 기본으로 출력함에서 exception')
    try:
        about_Quotes_contents = detail_fb_bio_info_soup.select('#pagelet_quotes > div > ul > li > div > div > span')[0].text
    except Exception as e:
        print('bio와 Quotes는 기본으로 출력함2에서 exception')

    print('quotes : ', about_Quotes_title, ', ', about_Quotes_contents)

    # [중요 이벤트]
    # https://www.facebook.com/kpokem/about?section=year-overviews
    detail_url_yearOverviews = 'https://www.facebook.com/' + user_fbpage_id + '/about?section=year-overviews'
    detail_fb_yearOverviews_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_yearOverviews)

    yearOverviews_medly_about_title = detail_fb_yearOverviews_info_soup.select(
        '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > div > span')[
        0].text  # 중요 이벤트
    yearOverviews_medly_about_contents_lists = detail_fb_yearOverviews_info_soup.select(
        '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li')

    for list_length in range(len(yearOverviews_medly_about_contents_lists)):

        yearOverviews_medly_about_contents_detail_01 = detail_fb_yearOverviews_info_soup.select(
            '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
                list_length + 1) + ') > div > div:nth-of-type(1) > span')[0].text  # 년도
        yearOverviews_medly_about_contents_detail_list = detail_fb_yearOverviews_info_soup.select(
            '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
                list_length + 1) + ') > div > div:nth-of-type(2) > ul > li')

        # print(len(yearOverviews_medly_about_contents_detail_list))

        for detail_list_length in range(len(yearOverviews_medly_about_contents_detail_list)):
            yearOverviews_medly_about_contents_detail_02 = detail_fb_yearOverviews_info_soup.select(
                '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
                    list_length + 1) + ') > div > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                    detail_list_length + 1) + ') > div > div > a > span')[0].text  # 내용
            print(yearOverviews_medly_about_contents_detail_01, ', ', yearOverviews_medly_about_contents_detail_02)










    DictionaryValue_list = returnedResultDict.values()


    for search_t in DictionaryValue_list:
        try:
            if '남성' in search_t:
                t_score_count_detail = 0
                print('성별 정보 검색 중...')

                print('가산 근거 : 남성일 경우 근속 기간이 여성보다 길기 때문에 70점이 가산 됩니다.')
                t_score_count_detail += 50
                t_score_count += t_score_count_detail

                detailInfo.append('__가산근거:남성일경우근속기간이_여성보다_길기때문에_70점이_가산됩니다.__')

            elif '여성' in search_t:
                t_score_count_detail = 0
                print('성별 정보 검색 중...')

                print('가산 근거 : 여성일 경우 근속 기간이 남성보다 짧기 때문에 50점이 가산 됩니다.')

                detailInfo.append('__가산근거:남성일경우근속기간이_여성보다_길기때문에_50점이_가산됩니다.__')

                t_score_count_detail += 25
                t_score_count += t_score_count_detail

            # try No.1 : 지역관련 정보 검색
            if '근무' in search_t:
                print('근무지 정보 검색 중...')
                t_score_count_detail = 0
                # print("%%", t_score_count)

                if '서울' in search_t:
                    print('가산 근거 : 근무지가 서울일 경우 60점이 가산 됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_60점이_가산됩니다.__')

                    t_score_count_detail += 60
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)
                elif '경기' in search_t:
                    print('가산 근거 : 근무지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_40점이_가산됩니다.__')
                    t_score_count_detail += 40
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)
                else:
                    print('가산 근거 : 근무지가 비-수도권일 경우 20점이 가산됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_20점이_가산됩니다.__')

                    t_score_count_detail += 20
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)

            # 학력사항 정보 검색
            if '공부했음' in search_t:
                if '졸업' in search_t:
                    if '대학원' in search_t:
                        print('대학원 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학원 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학원소재지가_서울일경우_60점이_가산됩니다.__')
                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학원 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학원소재지가_서울일경우_40점이_가산됩니다.__')
                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '대학교' in search_t:
                        print('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '고등학교' in search_t:
                        print('고등학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 고등학교 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                    else:
                        print('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                else:
                    if '대학교' in search_t:
                        print('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학교 소재지가 경기일 경우 30점이 가산됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_30점이_가산됩니다.__')

                            t_score_count_detail += 30
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '고등학교' in search_t:
                        print('고등학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_40점이_가산됩니다.__')
                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 고등학교 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                    else:
                        print('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

        except Exception as e_addr:
            print('T SCORE EXCEPTION : ', e_addr)

    print('T SCORE :', t_score_count)
    print()




    like_cnt_int = 0
    cnt_like_img = 0
    for search_c in DictionaryValue_list:
        try:
            if '거주' in search_c:
                print('거주지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 거주지가 서울일 경우 70점이 가산 됩니다.')

                    detailInfo.append('__거주지가_서울일경우_70점이_가산됩니다.__')

                    c_score_count_detail += 70
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 거주지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__거주지가_서울일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 거주지가 비-수도권일 경우 30점이 가산됩니다.')

                    detailInfo.append('__거주지가_서울일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '출신' in search_c:
                print('출신지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 출신지가 서울일 경우 70점이 가산 됩니다.')

                    detailInfo.append('__출신지가_서울일경우_70점이_가산됩니다.__')

                    c_score_count_detail += 70
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 출신지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__출신지가_서울일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 출신지가 비-수도권일 경우 30점이 가산됩니다.')

                    detailInfo.append('__출신지가_서울일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '팔로우' in search_c:

                followCntVal = str(search_c).split('명이')
                followCnt = int(followCntVal[0])
                print('팔로우 수: ', followCnt)
                c_score_count_detail = 0

                if followCnt >= 50:
                    print('팔로워 수가 50명 이상일 경우 50점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_50점이_가산됩니다.__')

                    c_score_count_detail += 50
                    c_score_count += c_score_count_detail

                elif 40 <= followCnt < 50:
                    print('팔로워 수가 40명 이상 50명 미만일 경우 40점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail

                elif 30 <= followCnt < 40:
                    print('팔로워 수가 30명 이상 40명 미만일 경우 30점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail

                elif 20 <= followCnt < 30:
                    print('팔로워 수가 20명 이상 30명 미만일 경우 20점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_20점이_가산됩니다.__')

                    c_score_count_detail += 20
                    c_score_count += c_score_count_detail

                elif 10 <= followCnt < 20:
                    print('팔로워 수가 10명 이상 20명 미만일 경우 10점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_10점이_가산됩니다.__')

                    c_score_count_detail += 10
                    c_score_count += c_score_count_detail

                elif 1 <= followCnt < 10:
                    print('팔로워 수가 1명 이상 10명 미만일 경우 5점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_5점이_가산됩니다.__')

                    c_score_count_detail += 5
                    c_score_count += c_score_count_detail

                else:
                    print('팔로워가 없으므로 가산점이 부여되지 않습니다. ')
                    detailInfo.append('팔로워가_없으므로_가산점이_부여되지_않습니다.')

        except Exception as e_c:
            print('C SCORE EXCEPTION :', e_c)

    # (returnedResult : 미리 받아온 세부 데이터)를 이용하지 않고, 친구 수 값을 추출하여 C_SCORE를 산출하기
    # friend count
    try:
        autoScrolled_data_soup_html_result = autoScroller(driver)
        userContent_FriendList = autoScrolled_data_soup_html_result.find('div', attrs={
            'id': 'profile_timeline_tiles_unit_pagelets_friends'})


        if userContent_FriendList:
            print('친구 리스트 공개 중입니다.')
            # friendsCnt_str = autoScrolled_data_soup_html_result.select('profile_timeline_tiles_unit_pagelets_friends > li > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > span')[0].text
            friendsCnt_str = autoScrolled_data_soup_html_result.select(
                '#profile_timeline_tiles_unit_pagelets_friends > li > div > div:nth-of-type(1) > div > div.clearfix._3-8t._2pi4 > div > div > div:nth-of-type(2) > div > span._50f8._2iem > a')[
                0].text

            print(friendsCnt_str)
            friendsCnt = int(friendsCnt_str.split('명')[0].replace(',', ''))

            #returnedResultDict['친구수'] = int(friendsCnt_str.split('명')[0].replace(',', ''))
            #{'모든친구': 1228, '함께아는친구': 5, '최근추가한친구': 18, '대학교': 20, '거주지': 407, '출신지': 38, '팔로워': 644}
            print('친구 수 : ', friendsCnt)


            if friendsCnt >= 500:
                print('친구 수가 500명 이상일 경우 70점이 가산됩니다.')

                detailInfo.append('친구수가_500명이상일경우_70점이_가산됩니다.')

                c_score_count_detail += 70
                c_score_count += c_score_count_detail

            elif 400 <= friendsCnt < 500:
                print('친구 수가 400명 이상 500명 미만일 경우 60점이 가산됩니다.')

                detailInfo.append('친구 수가 400명 이상 500명 미만일 경우_60점이_가산됩니다.')

                c_score_count_detail += 60
                c_score_count += c_score_count_detail

            elif 300 <= friendsCnt < 400:
                print('친구 수가 300명 이상 400명 미만일 경우 50점이 가산됩니다.')

                detailInfo.append('친구 수가 300명 이상 400명 미만일 경우 50점이 가산됩니다.')

                c_score_count_detail += 50
                c_score_count += c_score_count_detail

            elif 200 <= friendsCnt < 300:
                print('친구 수가 200명 이상 300명 미만일 경우 30점이 가산됩니다.')

                detailInfo.append('친구 수가 200명 이상 300명 미만일 경우 30점이 가산됩니다.')

                c_score_count_detail += 30
                c_score_count += c_score_count_detail

            elif 100 <= friendsCnt < 200:
                print('친구 수가 100명 이상 200명 미만일 경우 20점이 가산됩니다.')

                detailInfo.append('친구 수가 100명 이상 200명 미만일 경우 20점이 가산됩니다.')

                c_score_count_detail += 20
                c_score_count += c_score_count_detail

            elif 1 <= friendsCnt < 100:
                print('친구 수가 1명 이상 100명 미만일 경우 10점이 가산됩니다.')

                detailInfo.append('친구 수가 1명 이상 100명 미만일 경우 10점이 가산됩니다.')

                c_score_count_detail += 10
                c_score_count += c_score_count_detail

            else:
                print('친구가 없으므로 가산점이 부여되지 않습니다. ')
                detailInfo.append('친구가 없으므로 가산점이 부여되지 않습니다.')
        else:
            print('친구 리스트가 비공개로 설정되어 있습니다.')
            detailInfo.append('친구 리스트가 비공개로 설정되어 있습니다.')

    except Exception as ex:
        print('친구 수 추적에 실패했습니다.', ex)




    # 친구수 정보 추가-syhan
    driver.get('https://www.facebook.com/' + user_fbpage_id + '/friends')

    friends_html = driver.page_source
    friends_soup = bs(friends_html, 'html.parser')

    returnedResultDict['친구수'] = 0
    returnedResultDict['모든친구'] = 0
    returnedResultDict['함께아는친구'] = 0
    returnedResultDict['최근추가한친구'] = 0
    returnedResultDict['대학교'] = 0
    returnedResultDict['거주지'] = 0
    returnedResultDict['출신지'] = 0
    returnedResultDict['팔로워'] = 0

    try:
        friends_all_cnt = friends_soup.select(
            '#pagelet_timeline_medley_friends > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a')

        if len(friends_all_cnt) is not 0:

            # friends_data = {}
            for frnKindLgth in range(len(friends_all_cnt)):
                friendsKind = friends_soup.select(
                    '#pagelet_timeline_medley_friends > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        frnKindLgth + 1) + ') > span:nth-of-type(1)')[0].text

                friendsKind_Cnt = friends_soup.select(
                    '#pagelet_timeline_medley_friends > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        frnKindLgth + 1) + ') > span:nth-of-type(2)')[0].text

                # print(friendsKind, ':', friendsKind_Cnt)

                '''
                예시)
                모든 친구 : 1,228
                함께 아는 친구 : 5
                최근 추가한 친구 : 18
                대학교 : 20
                거주지 : 407
                출신지 : 38
                팔로워 : 644
                '''

                # 위의 항목들중 존재하는 항목들이 returnedResultDict에 추가될 것이다.
                returnedResultDict[friendsKind.replace(" ", "")] = int(friendsKind_Cnt.replace(",", ""))
                # print(friendsKind.replace(" ", ""), ':', int(friendsKind_Cnt.replace(",","")))

            print(returnedResultDict)

        else:
            print('표시할 친구 없음')

    except Exception as e:
        print('친구 정보가 공개되지 않았습니다. ')








    returnedResultDict['좋아요클릭한사람수'] = 0
    returnedResultDict['이미지에좋아요클릭한사람수'] = 0
    likePushPersonCnt = 0

    try:
        attrValue_like_imgVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > span._3t54 > a._3emk._401_')
        cnt_like_img = len(attrValue_like_imgVal)

        attrValue_like_txtVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > a._2x4v > span._4arz > span')

        likeManCnt = 0
        likeManCnt1 = 0

        for likePerson in range(len(attrValue_like_txtVal)):
            like_cnt_str = attrValue_like_txtVal[likePerson].text.split('명')[0]

            try:
                like_cnt_int = like_cnt_int + int(like_cnt_str)
                # print('"좋아요" 표시 전체 갯수 :', like_cnt_int)
                likePushPersonCnt += 1

            except ValueError as e_p:
                like_man = attrValue_like_txtVal[likePerson].text
                likePushPersonCnt += 1
                # 갯수가 표시되지 않고 사람 이름이 표시된 경우에 해당함.
                # print('"좋아요"를 누른 사람의 이름:', like_man)
                if '외' in like_man:
                    likeManCntStr = like_man.split('외')[1].strip()
                    likeManCnt1 = int(likeManCntStr.split('명')[0])
                else:
                    print('"좋아요"를 누른 사람의 이름:', like_man)
            likeManCnt += likeManCnt1

            print('Total like man count : ', likeManCnt)

        if likeManCnt >= 5000:
            print('좋아요 표시가 5000개 이상일 경우 70점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 5000개 이상일 경우 70점이 가산됩니다.')

            c_score_count_detail += 70
            c_score_count += c_score_count_detail

        elif 4000 <= likeManCnt < 5000:
            print('좋아요 표시가 4000개 이상 5000개 미만일 경우 60점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 4000개 이상 5000개 미만일 경우 60점이 가산됩니다.')

            c_score_count_detail += 60
            c_score_count += c_score_count_detail

        elif 3000 <= likeManCnt < 4000:
            print('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            c_score_count_detail += 50
            c_score_count += c_score_count_detail

        elif 2000 <= likeManCnt < 3000:
            print('좋아요 표시가 2000개 이상 3000개 미만일 경우 40점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            c_score_count_detail += 40
            c_score_count += c_score_count_detail

        elif 1000 <= likeManCnt < 2000:
            print('좋아요 표시가 1000개 이상 2000개 미만일 경우 30점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 1000개 이상 2000개 미만일 경우 30점이 가산됩니다.')

            c_score_count_detail += 30
            c_score_count += c_score_count_detail

        elif 1 <= likeManCnt < 1000:
            print('좋아요 표시가 1개 이상 1000개 미만일 경우 15점이 가산됩니다.')
            detailInfo.append('좋아요 표시가 1개 이상 1000개 미만일 경우 15점이 가산됩니다.')
            c_score_count_detail += 15
            c_score_count += c_score_count_detail

        else:
            print('좋아요 표시가 없으므로 가산점이 부여되지 않습니다. ')
            detailInfo.append('좋아요 표시가 없으므로 가산점이 부여되지 않습니다. ')
        print('C SCORE :', c_score_count)

    except Exception as e_lk:
        print('좋아요 정보 추출 Exception', e_lk)


    print('좋아요_사람 전체 명수 : ', likePushPersonCnt)
    print('이미지에좋아요클릭한사람수: ', cnt_like_img)

    returnedResultDict['좋아요클릭한사람수'] = likePushPersonCnt
    returnedResultDict['이미지에좋아요클릭한사람수'] = cnt_like_img






    #좋아요(관심사) - syhan
    returnedResultDict['좋아요모두'] = 0
    returnedResultDict['영화'] = 0
    returnedResultDict['TV프로그램'] = 0
    returnedResultDict['음악'] = 0
    returnedResultDict['책'] = 0
    returnedResultDict['스포츠팀'] = 0
    returnedResultDict['음식점'] = 0
    returnedResultDict['앱과게임'] = 0



    driver.get('https://www.facebook.com/' + user_fbpage_id + '/likes')

    likes_html = driver.page_source
    likes_soup = bs(likes_html, 'html.parser')

    try:
        likes_all_cnt = likes_soup.select(
            '#pagelet_timeline_medley_likes > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a')

        print(likes_all_cnt)
        if len(likes_all_cnt) is not 0:

            print('길이:', len(likes_all_cnt))
            # likes_data = {}

            for likesKindLgth in range(len(likes_all_cnt)):
                likesKind = likes_soup.select(
                    '#pagelet_timeline_medley_likes > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        likesKindLgth + 1) + ') > span:nth-of-type(1)')[0].text

                likesKind_Cnt = likes_soup.select(
                    '#pagelet_timeline_medley_likes > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        likesKindLgth + 1) + ') > span:nth-of-type(2)')[0].text

                # print(likesKind, ':', likesKind_Cnt)

                '''
                예시)            
                좋아요 모두 : 407
                영화 : 11
                TV 프로그램 : 14
                음악 : 32
                책 : 12
                스포츠 팀 : 1
                음식점 : 3
                앱과 게임 : 7
                '''

                returnedResultDict[likesKind.replace(" ", "")] = int(likesKind_Cnt.replace(",", ""))
                print(likesKind.replace(" ", ""), ':', int(likesKind_Cnt.replace(",", "")))
                # {'좋아요모두': 407, '영화': 11, 'TV프로그램': 14, '음악': 32, '책': 12, '스포츠팀': 1, '음식점': 3, '앱과게임': 7}

            print(returnedResultDict)

        else:
            print('표시할 좋아요 없음')

    except Exception as e:
        print('좋아요 정보가 공개되지 않았습니다. ')

    # 체크인 수 정보 추가
    driver.get('https://www.facebook.com/' + user_fbpage_id + '/map')

    map_html = driver.page_source
    map_soup = bs(map_html, 'html.parser')

    returnedResultDict['장소'] = 0
    returnedResultDict['도시'] = 0
    returnedResultDict['최근에가본곳'] = 0

    try:
        map_all_cnt = map_soup.select(
            '#pagelet_timeline_medley_map > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a')
        #print(map_all_cnt)

        if len(map_all_cnt) is not 0:
            #print('길이:', len(map_all_cnt))

            #returnedResultDict = {}

            for mapKindLgth in range(len(map_all_cnt)):
                mapKind = map_soup.select(
                    '#pagelet_timeline_medley_map > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        mapKindLgth + 1) + ') > span:nth-of-type(1)')[0].text

                mapKind_Cnt = map_soup.select(
                    '#pagelet_timeline_medley_map > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        mapKindLgth + 1) + ') > span:nth-of-type(2)')[0].text

                # print(likesKind, ':', likesKind_Cnt)

                '''
                예시)
                길이: 3
                장소 : 203
                도시 : 56
                최근에가본곳 : 417            
                '''

                returnedResultDict[mapKind.replace(" ", "")] = int(mapKind_Cnt.replace(",", ""))
                #print(mapKind.replace(" ", ""), ':', int(mapKind_Cnt.replace(",", "")))

            print(returnedResultDict)
            # {'장소': 203, '도시': 56, '최근에가본곳': 417}

        else:
            print('표시할 체크인 없음')

    except Exception as e:
        print('체크인 정보가 공개되지 않았습니다. ')





    # 이벤트 수 정보 추가
    driver.get('https://www.facebook.com/' + user_fbpage_id + '/events')

    events_html = driver.page_source
    events_soup = bs(events_html, 'html.parser')

    returnedResultDict['이벤트내용개수'] = 0
    returnedResultDict['이벤트내용'] = '표시할 이벤트 없음'

    try:
        events_all_list = events_soup.select(
            '#pagelet_timeline_medley_events > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')

        # print(events_all_list)

        events_data = []
        #events_data_dic = {}

        if len(events_all_list) is not 0:

            # print('길이:', len(events_all_list))

            for eventsKindLgth in range(len(events_all_list)):
                eventsKind_title = events_soup.select(
                    '#pagelet_timeline_medley_events > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        eventsKindLgth + 1) + ') > div > div:nth-of-type(1) > div:nth-of-type(2) > a')[0].text

                eventsKind_date = events_soup.select(
                    '#pagelet_timeline_medley_events > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        eventsKindLgth + 1) + ') > div > div:nth-of-type(1) > div:nth-of-type(2) > div')[0].text

                # print(eventsKind_title, ':', eventsKind_date)

                '''
                예시)
                케이채사진전TheSouth:작가와의만남:2018년4월28일토요일오후3:00
                @박정민개인전‘소년,제주에살다’오프닝파티:2018년2월2일금요일오후8:00
                @관철수대선단독출마:2017년12월20일수요일오전6:00
                @8월서울정기모임:2016년8월6일토요일오후3:00
                @사진읽기9월3주차정기모임:2015년9월19일토요일오후2:00
                @포토그래퍼스갤러리코리아선정8월의작가고방원초대개인전:2015년8월19일수요일오전11:00
                @2013-1한예종연극원레퍼토리<로미오와줄리엣>:2013년5월30일목요일오전12:00
                @"Catchtheeye;Eve"2012.12.24.Mon@BehiveLounge'sFirstParty:2012년12월24일월요일오후10:00    
                '''

                events_data.append(eventsKind_title.replace(" ", "").replace("'", "") + ':' + eventsKind_date.replace(" ", ""))
                # print(events_data)

            # print('@'.join(events_data) )

            returnedResultDict['이벤트내용개수'] = len(events_all_list)
            returnedResultDict['이벤트내용'] = '_@'.join(events_data)

            print(returnedResultDict['이벤트내용개수'], ', ', returnedResultDict['이벤트내용'])


        else:
            print('표시할 이벤트 없음')

    except Exception as e:
        print('이벤트 정보가 공개되지 않았습니다. ')





    # 영화 수 정보 추가
    driver.get('https://www.facebook.com/' + user_fbpage_id + '/movies')

    movies_html = driver.page_source
    movies_soup = bs(movies_html, 'html.parser')

    movies_data = []
    #movies_data_dic = {}

    returnedResultDict['봤어요'] = 0
    returnedResultDict['영화'] = 0
    returnedResultDict['영화내용개수'] = 0
    returnedResultDict['영화제목'] = '표시할 영화 없음'

    try:
        movies_all_cnt = movies_soup.select(
            '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a')

        print('movies_all_cnt :', len(movies_all_cnt))

        if len(movies_all_cnt) is not 0:
            for moviesKindTitleLength in range(len(movies_all_cnt)):
                moviesKind_title = movies_soup.select(
                    '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        moviesKindTitleLength + 1) + ') > span:nth-of-type(1)')[0].text

                moviesKind_cnt = movies_soup.select(
                    '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(' + str(
                        moviesKindTitleLength + 1) + ') > span:nth-of-type(2)')[0].text

                returnedResultDict[moviesKind_title.replace(" ", "")] = int(moviesKind_cnt.replace(",", ""))

            #returnedResultDict['봤어요'] = int(moviesKind_cnt.replace(",", "")
            #returnedResultDict['영화'] = int(moviesKind_cnt.replace(",", "")



        movies_all_list = movies_soup.select('#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')

        print('movies_all_list: ', len(movies_all_list))

        if len(movies_all_list) is not 0:
            for moviesKindLgth in range(len(movies_all_list)):
                movies_title = movies_soup.select(
                    '#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        moviesKindLgth + 1) + ') > div > div:nth-of-type(1) > a')[0].text

                moviesSaw_date = movies_soup.select(
                    '#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        moviesKindLgth + 1) + ') > div > div:nth-of-type(1) > div:nth-of-type(1) > a > div > abbr > span')[
                    0].text

                movies_data.append(movies_title.replace(" ", "").replace("'","") + ':' + moviesSaw_date.replace(" ", ""))
                #print(events_data)

            #print('@'.join(events_data) )
            returnedResultDict['영화내용개수'] = len(movies_all_list)
            returnedResultDict['영화제목'] = '_@'.join(movies_data)
            #print(returnedResultDict['영화내용개수'], ', ', returnedResultDict['영화제목'])

        else:
            print('표시할 영화 없음')

    except Exception as e:
        print('영화 정보가 공개되지 않았습니다. ')



    # 게시글 댓글 수 정보 추가- 타임라인

    userFacebook_currentUrl = 'https://www.facebook.com/' + user_fbpage_id

    # driver.get('https://www.facebook.com/' + user_fbpage_id)
    # articles_reply_html = driver.page_source
    # articles_reply_soup = bs(articles_reply_html, 'html.parser')
    articles_reply_soup = autoScroller2(driver, userFacebook_currentUrl)

    articles_reply_data = []
    #articles_reply_data_dic = {}

    returnedResultDict['댓글개수'] = 0
    returnedResultDict['댓글내용'] = '표시할 댓글 없음'

    returnedResultDict['게시글좋아요수'] = 0
    returnedResultDict['게시글공유수'] = 0

    returnedResultDict['수집한게시글개수'] = 0

    returnedResultDict['평균댓글개수'] = 0
    returnedResultDict['평균덧글개수'] = 0
    returnedResultDict['전체긍정어사용빈도'] = 0
    returnedResultDict['평균긍정어사용비율'] = 0

    try:

        articleLikeTotCnt = 0
        articleReplyTotCnt = 0
        articleShareTotCnt = 0

        articleNum = 0

        replyCnt = 0
        moreReplyCnt = 0

        totCycNumGoodWords = 0
        goodWordsUsingRate = 0.00
        rateGoodWords = 0.00

        articleCnt = articles_reply_soup.select('#recent_capsule_container > ol > div')
        # print('게시글 개수:', len(articleCnt) )

        if len(articleCnt) is not 0:

            for articleLength in range(len(articleCnt)):
                # 1. 게시글의 등록 날짜 가져오기
                innerArticleCnt = articles_reply_soup.select(
                    '#recent_capsule_container > ol > div:nth-of-type(' + str(articleLength + 1) + ') > div')

                # 게시글을 출력하는 묶음 단위가 존재하며, 각 묶음단위별 포함하고 있는 게시글의 갯수가 상이함.

                print()
                print()
                print()
                print('innerArticleCnt : ', len(innerArticleCnt))

                for innerArtclLnth in range(len(innerArticleCnt)):

                    # 1. 게시글 내용 리스트화
                    # 2. 게시글 내용 vs 긍정어 단어 매칭 빈도수 측정(확률로 계산하면 될 듯)

                    # 게시글 영역
                    # 게시글 등록 시간
                    try:
                        updatedTime = \
                        articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type(' + str(
                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div > span:nth-of-type(3) > span > a > abbr > span')[
                            0].text
                    except Exception as e:
                        updatedTime = \
                        articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type(' + str(
                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div > span:nth-of-type(3) > span > abbr > span')[
                            0].text

                    print()
                    print()
                    print()
                    print('게시글 등록 시간:', updatedTime)

                    articleNum += 1

                    print('게시글 번호 :', articleNum)

                    # 게시글 영역
                    # 게시글 (작성)내용
                    try:
                        updatedArticleContents = articles_reply_soup.select(
                            '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                articleLength + 1) + ') > div:nth-of-type(' + str(
                                innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2)')[
                            0].text

                    except Exception as e:
                        updatedArticleContents = articles_reply_soup.select(
                            '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                articleLength + 1) + ') > div:nth-of-type(' + str(
                                innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1)')[
                            0].text

                    # 2-1. 게시글의 작성된 글 내용 가져오기
                    print('updatedArticleContents :', updatedArticleContents.replace("'",""))
                    # print('$1')
                    updatedArticleContentsList = updatedArticleContents.split(" ")
                    # print('$2')
                    print(updatedArticleContentsList)

                    # print('$3')
                    articles_reply_data = articles_reply_data + updatedArticleContentsList
                    # print('$4')

                    article_reply_text = '@'.join(articles_reply_data)

                    # 2-2. 게시글의 내용(단어)를 리스트로 변환
                    # 2-3. 게시글 내용 리스트와 긍정어 단어 리스트의 비교 분석 및 빈도수 측정
                    returnExpList = readCSV_goodExpressions()
                    # print('1-1')

                    # print('단어 리스트 길이 :', len(returnExpList) )

                    cycNumGoodWords = 0
                    cycNumElseWords = 0
                    # returnExpList : 긍정어.csv 파일에서 가져온 긍정어 항목
                    for expListLngth in range(len(returnExpList)):
                        # 긍정어 표현 목록 길이 만큼 반복문을 돈다.

                        # articles_reply_data :  게시글에서 추출한 단어 리스트
                        if returnExpList[expListLngth] in updatedArticleContentsList:
                            # 긍정어.csv에서 가져온 단어가 게시글에서 추출한 단어 리스트에 존재하는지.

                            print('일치하는 긍정어 있음 :', returnExpList[expListLngth])

                            cycNumGoodWords += 1
                            totCycNumGoodWords += 1
                            continue

                        else:
                            cycNumElseWords += 1
                            continue

                    # 각 게시물별 긍정어 사용 확률값

                    rateGoodWords = (cycNumGoodWords / len(articles_reply_data))

                    goodWordsUsingRate = float("{:.2f}".format(rateGoodWords))

                    print('각 게시물 당 긍정어 사용 비율:', goodWordsUsingRate)

                    # 3. 댓글과 덧글의 작성자명을 추출
                    # 4. 각 게시물당 댓글 작성자명을 리스트로 변경, 같은 이름의 빈도수를 추출
                    # 5. 게시물과 댓글의 내용을 리스트로 변경하여 긍정어 빈도수 추출
                    # 6. 댓글 내용 vs 긍정어 단어 매칭 빈도수 측정(확률로 계산하면 될 듯)

                    # 댓글영역
                    # 좋아요 수
                    try:
                        articleLikeCnt = \
                        articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type(' + str(
                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(1) > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > a > span:nth-of-type(2) > span')[
                            0].text
                    except Exception as e:
                        print('댓글영역 > 좋아요 수 부분 에러')

                    print('articleLikeCnt :', articleLikeCnt)

                    articleLikeCnt = articleLikeCnt.split(" ")[2].split('명')[0]

                    articleLikeTotCnt += int(articleLikeCnt)

                    '''
                    예)
                    articleLikeCnt : XXX님 외 239명
                    '''

                    # 댓글영역
                    # 댓글 개수
                    try:
                        articleReplyContentsCnt = \
                        articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type(' + str(
                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(1) > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1)')[
                            0].text
                    except Exception as e:
                        print('댓글영역 > 댓글 개수 부분 에러')

                    # 댓글 12개
                    '''
                    예)
                    articleReplyContentsCnt : 댓글 103개
                    또는
                    articleReplyContentsCnt : 댓글 48개공유 13회
                    '''

                    articleReplyContentsCnt0 = ''
                    articleReplyContentsCnt1 = ''

                    try:
                        articleReplyContentsCnt0 = articleReplyContentsCnt.split(" ")[0]
                        # articleReplyContentsCnt0 = '댓글'

                        try:
                            articleReplyContentsCnt1 = articleReplyContentsCnt.split(" ")[1]
                            # articleReplyContentsCnt1 = 'XX개공유'
                            articleShareCnt = 0

                            # articleReplyContentsCnt.replace(" ", "") = 댓글XX개공유XX회
                            articleShareCnt = int(
                                articleReplyContentsCnt.replace(" ", "").split("공유")[1].replace("회", ""))
                            articleShareTotCnt += articleShareCnt
                            # print('articleShareCnt :', articleShareCnt)

                        except Exception as e:
                            print('공유 횟수는 없습니다.')

                            articleReplyContentsCnt = articleReplyContentsCnt1.split("개")[0]
                            articleReplyTotCnt += int(articleReplyContentsCnt)

                    except Exception as e:

                        print('댓글 이나 게시 공유가 없습니다.')

                    # 댓글영역
                    # 댓글 추출
                    # 3. 게시글의 댓글 가져오기(댓글중 텍스트와 텍스트 아닌 것을 구분하기)

                    try:
                        articleReplyContentsList = articles_reply_soup.select(
                            '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                articleLength + 1) + ') > div:nth-of-type(' + str(
                                innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div')

                        print('노출된 댓글의 개수:', len(articleReplyContentsList))

                        testPrint = ''
                        try:
                            testPrint = articles_reply_soup.select(
                                '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                    articleLength + 1) + ') > div:nth-of-type(' + str(
                                    innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > a')[
                                0].text

                            testPrintList = testPrint.split(" ")
                            print('testPrintList :', testPrintList)

                            moreReplyCnt = int(testPrintList[1].replace("개", ""))
                            print('더 존재하는 댓글 : ', moreReplyCnt)

                        except Exception as e:
                            print()

                        replyAndReply = 0
                        articleReplyContentsWriterList = []
                        for exposedReplyLength in range(len(articleReplyContentsList)):
                            print('댓글 No.', str(exposedReplyLength + 1))

                            replyReply = 0

                            if '보기' in testPrint:
                                try:
                                    # 댓글 작성자 이름 추출
                                    articleReplyContentsWriter = articles_reply_soup.select(
                                        '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                            articleLength + 1) + ') > div:nth-of-type(' + str(
                                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(' + str(
                                            exposedReplyLength + 2) + ') > div > div > div')[0].text

                                    articleReplyContentsWriterList.append(articleReplyContentsWriter.split("  ")[0])
                                    # print('게시글 No.', articleNum, '댓글작성자 리스트:', articleReplyContentsWriterList)

                                    replyCnt += 1
                                except Exception as e:
                                    print('댓글 가져오는 부분 -1 : 댓글에 덧글이 존재함', e)
                                    replyAndReply += 1

                                    replyReply += 1

                            else:
                                try:
                                    articleReplyContentsWriter = articles_reply_soup.select(
                                        '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                            articleLength + 1) + ') > div:nth-of-type(' + str(
                                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(' + str(
                                            exposedReplyLength + 1) + ') > div > div > div')[0].text

                                    articleReplyContentsWriterList.append(articleReplyContentsWriter.split("  ")[0])

                                    replyCnt += 1
                                except Exception as e:
                                    print('댓글 가져오는 부분 -2 : 댓글에 덧글이 존재함', e)
                                    replyAndReply += 1

                        print('게시글 No.', articleNum, '댓글작성자 리스트:', articleReplyContentsWriterList)
                        print('게시물 No.', articleNum, '의 총 "댓글" 개수:', (replyCnt + moreReplyCnt))
                        print('게시물 No.', articleNum, '의 총 "덧글" 개수:', replyAndReply)

                    except Exception as e:
                        print('댓글영역 > 댓글 추출 부분 에러')

            print('각 게시글에 대한 평균 댓글 개수 :', ((replyCnt + moreReplyCnt) / len(articleCnt)))
            print('각 게시글에 대한 평균 덧글 개수 :', (replyAndReply / len(articleCnt)))

            print('articleLikeTotCnt: ', articleLikeTotCnt)
            print('articleReplyTotCnt: ', articleReplyTotCnt)
            print('articleShareCnt:', articleShareTotCnt)

            returnedResultDict['수집한게시글개수'] = len(articleCnt)

            returnedResultDict['댓글개수'] = articleReplyTotCnt
            returnedResultDict['게시글좋아요수'] = articleLikeTotCnt
            returnedResultDict['게시글공유수'] = articleShareTotCnt
            returnedResultDict['댓글내용'] = article_reply_text.replace("'","")

            returnedResultDict['평균댓글개수'] = float("{:.2f}".format((replyCnt + moreReplyCnt) / len(articleCnt)))
            returnedResultDict['평균덧글개수'] = float("{:.2f}".format(replyAndReply / len(articleCnt)))
            returnedResultDict['전체긍정어사용빈도'] = totCycNumGoodWords
            returnedResultDict['평균긍정어사용비율'] = float("{:.2f}".format((totCycNumGoodWords / len(articleCnt))))

            #print('게시글관련정보_중간점검_출력', returnedResultDict)


    except Exception as e:
        print('게시글이 공개되지 않았습니다. ')











    print('C_SCORE를 산출하겠습니다.')
    print('C SCORE :', c_score_count)
    print()



    returnedResultDict['DETAIL'] = detailInfo

    # T SCORE, C CORE 값을 넘겨 SCM SCORE 산출
    returnedValue_from_method_TCMCountGen = TCMCountGen(t_score_count, c_score_count, returnedResultDict, User_timeLine_site_url_addr, driver, requestClient)

    print('TCMCountGen 의 결과 :', TCMCountGen)



    if returnedValue_from_method_TCMCountGen['trueOrFalse'] == True:
        print('TCM SCORE가 정상 산출 되었습니다.')

    elif returnedValue_from_method_TCMCountGen['trueOrFalse'] == False:
        print('TCM SCORE가 산출 되지 않았습니다.')

    return returnedValue_from_method_TCMCountGen



#getDetailInfo 관련 함수 ========================================================================================
#dictionary type 으로 취합할 정보 : 연락처 정보, 웹사이트 및 소셜 링크 정보, 기본 정보
def getDetailInfoDictionaryType(userPageId, driver, loginCnt, userName, reqClientNm):
    detail_url = 'https://www.facebook.com/'+ userPageId +'/about?section=contact-info&pnref=about'

    driver.get(detail_url)
    html_detail_fb_chrome = driver.page_source
    detail_fb_info_soup = bs(html_detail_fb_chrome, 'html.parser')

    #print('T_SCORE를 산출하겠습니다.')
    #pagelet_basic_list_data = []

    #[연락처 정보]란 제목
    user_pglet_contactData_title_01 = detail_fb_info_soup.select(
        '#pagelet_contact > div > div:nth-of-type(1) > div > span')

    #[웹사이트 및 소셜 링크]란 제목
    user_pglet_contactData_title_01_2 = detail_fb_info_soup.select(
        '#pagelet_contact > div > div:nth-of-type(2) > div > div > span')

    #[기본 정보]란 제목
    user_pglet_basicData_title_01 = detail_fb_info_soup.select(
        '#pagelet_basic > div > div > span')

    user_pglet_data = detail_fb_info_soup.select('div#pagelet_contact > div > div')
    #print('user_pglet_data = ', user_pglet_data)

    length_user_pglet_data = len(user_pglet_data)

    if length_user_pglet_data == 0:
        print('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : ', length_user_pglet_data)
        print('페이스북 접속이 원할하지 않아 다시 시도해야 합니다.')
        if loginCnt <= 2:

            userInfoDetailDic = False

            return userInfoDetailDic

            #login_facebook(loginCnt, userPageId, userName)

        else:
            print('페이스북 크롤링을 재 구동하여야 합니다. 작동을 중지합니다.')
            driver.close()

    else:
        print('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : ', length_user_pglet_data)

        #[연락처 정보] & [소셜링크 및 웹사이트 정보] Dictionary
        contDic = {}
        contDataList = []
        contDataList_webSns = []

        #[기본 정보] Dictionary
        basicDic = {}
        basicDataList = []

        #[연락처 정보]란 취득
        if not user_pglet_contactData_title_01:
            print('사용자가 연락처 정보를 등록하지 않았습니다.')
        else:
            #pagelet_contact
            if '연락처' in user_pglet_contactData_title_01[0].text:
                print(user_pglet_contactData_title_01[0].text)  # 연락처 정보

                # [연락처 정보]란 하단 세부 정보 타이틀
                pagelet_contact_dir_list = 'div#pagelet_contact > div > div:nth-of-type(1) > ul > li'

                # [연락처 정보]란 하단 세부 정보 타이틀 갯수
                length_of_contList = len(detail_fb_info_soup.select(pagelet_contact_dir_list))

                # [연락처 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conCycle = 0

                try:
                    #하단 세부 정보 길이 만큼 반복문 실행해 key:value 생성
                    while  conCycle < length_of_contList:
                        userContactInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_dir_list + ':nth-of-type(' + str(int(conCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [연락처 정보]란_title
                        key = userContactInfoListTitle.replace(" ", "")
                        #print('연락처 정보_title: ', key)

                        # [연락처 정보]란_value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_dir_list +':nth-of-type(' + str(
                                int(conCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")
                        #print('연락처 정보_value: ', value)

                        contDic[key] = value
                        contDataList.append(value)
                        conCycle += 1

                    #contDic['전체연락처정보'] = '__'.join(contDataList)
                    #print("contDic['전체연락처정보'] :", contDic['전체연락처정보'])

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    #contDic['전체연락처정보'] = '전체연락처정보가없습니다'

                print('연락처 정보 수집 결과[Dictionary type]: ' , contDic)
                #contDic['전체연락처정보'] = '전체연락처정보가없습니다'

        # [웹사이트 및 소셜 링크]란
        if not user_pglet_contactData_title_01_2:
            print('사용자가 웹사이트 및 소셜 링크 정보를 등록하지 않았습니다.')
        else:
            #pagelet_contact
            if '웹사이트' in user_pglet_contactData_title_01_2[0].text:
                print(user_pglet_contactData_title_01_2[0].text)  #웹사이트 및 소셜 링크 정보

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀
                pagelet_contact_webSite_dir_list = 'div#pagelet_contact > div > div:nth-of-type(2) > div > ul > li'

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀 갯수
                length_of_contWebSiteList = len(detail_fb_info_soup.select(pagelet_contact_webSite_dir_list))

                # [웹사이트 및 소셜 링크]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conWebCycle = 0

                try:
                    while  conWebCycle < length_of_contWebSiteList:
                        userContactWebInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list + ':nth-of-type(' + str(int(conWebCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [웹사이트 및 소셜 링크]란 title
                        key = userContactWebInfoListTitle.replace(" ", "")
                        print('웹사이트 및 소셜 링크 정보_title: ', key)

                        # [웹사이트 및 소셜 링크]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list +':nth-of-type(' + str(
                                int(conWebCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")

                        contDic[key] = value

                        contDataList_webSns.append(value)
                        conWebCycle += 1

                    contDic['웹사이트및소셜링크정보'] = '_'.join(contDataList_webSns)

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    contDic['웹사이트및소셜링크정보'] = ''

                print('웹사이트 및 소셜 링크 정보 수집 결과[Dictionary type]: ' , contDic)

        # [기본 정보]란 취득
        if not user_pglet_basicData_title_01:
            print('사용자가 기본 정보를 등록하지 않았습니다.')
        else:
            #pagelet_basic
            if '기본' in user_pglet_basicData_title_01[0].text:
                print(user_pglet_basicData_title_01[0].text)  # 기본 정보

                # [기본 정보]란 하단 세부 정보 타이틀
                pagelet_basic_dir_list = 'div#pagelet_basic > div > ul > li'

                # [기본 정보]란 하단 세부 정보 타이틀 갯수
                length_of_basicList = len(detail_fb_info_soup.select(pagelet_basic_dir_list))

                # [기본 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                baseCycle = 0

                try:
                    while  baseCycle < length_of_basicList:
                        userBasicInfoListTitle = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [기본 정보]란 title
                        key = userBasicInfoListTitle.replace(" ", "")

                        # [기본 정보]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")

                        basicDic[key] = value
                        basicDataList.append(value)

                        baseCycle += 1
                    basicDic['전체기본정보'] = ''.join(basicDataList)

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    basicDic['전체기본정보'] = ''

                print('기본 정보 수집 결과 [Dictionary type]: ' , basicDic)

        userInfoDetailDic = dict(basicDic, **contDic)

        print('결과 -> 사용자 페이스북 상의 상세 정보 [Dictionary type] : ', userInfoDetailDic)

        return userInfoDetailDic




#TCM SCORE 산출
def TCMCountGen(tScoreCount, cScoreCount, ResultDict, user_fbpage_url, driver, requestClient):


    print('TCMCountGen에서의 중간결과 :', ResultDict['DETAIL'])

    ResultDict['동영상수'] = 0
    ResultDict['사진수'] = 0


    detailInfoList = '_'.join(ResultDict['DETAIL'])

    print('detailInfoList :', detailInfoList.replace(".", ""))

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
        m_score_count_detail = 0

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
        mCountData = 0
        mCountData = contentCnt + totalPicCnt
        print('게시글(사진, 동영상 포함) 수 : ', contentCnt + totalPicCnt)
        print('게시글(텍스트로만 구성) 수 : ', contentCnt - (prfl_picCnt + prfl_vodCnt))




        if mCountData >= 500:
            print('사진 수가 500장 이상일 경우 80점이 가산됩니다.')
            m_score_count_detail += 80
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 200 <= mCountData < 500:
            print('사진 수가 200장 이상 500장 미만일 경우 65점이 가산됩니다.')
            m_score_count_detail += 65
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 10 <= mCountData < 200:
            print('사진 수가 10장 이상 200장 미만일 경우 50점이 가산됩니다.')
            m_score_count_detail += 50
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)

        ResultDict['동영상수'] = prfl_vodCnt

        print('ResultDict["동영상수"] :', ResultDict['동영상수'])
        print('ResultDict["사진수"] :', ResultDict['사진수'])

        ResultDict['사진수'] = totalPicCnt

        mScoreCount = m_score_count

        # 게시글 텍스트 크롤링
        autoScrollerContentsText(user_fbpage_url, driver)

        print('최종 T SCORE : ', tScoreCount)
        print('최종 C SCORE : ', cScoreCount)
        print('최종 M SCORE : ', mScoreCount)
        print()

        ResultDict.update({'T_SCORE':tScoreCount, 'C_SCORE':cScoreCount, 'M_SCORE':mScoreCount})

        print('최종 RESULT : ', ResultDict)

        '''
        ResultDict['친구수'] = 0
        ResultDict['모든친구'] = 0
        ResultDict['함께아는친구'] = 0
        ResultDict['최근추가한친구'] = 0
        ResultDict['대학교'] = 0
        ResultDict['거주지'] = 0
        ResultDict['출신지'] = 0
        ResultDict['팔로워'] = 0

        ResultDict['좋아요모두'] = 0
        ResultDict['영화'] = 0
        ResultDict['TV프로그램'] = 0
        ResultDict['음악'] = 0
        ResultDict['책'] = 0
        ResultDict['스포츠팀'] = 0
        ResultDict['음식점'] = 0
        ResultDict['앱과게임'] = 0
        ResultDict['좋아요클릭한사람수'] = 0

        ResultDict['장소'] = 0
        ResultDict['도시'] = 0
        ResultDict['최근에가본곳'] = 0	

        ResultDict['이벤트내용개수'] = 0
        ResultDict['이벤트내용'] = '표시할 이벤트 없음'	

        ResultDict['봤어요'] = 0
        ResultDict['영화'] = 0
        ResultDict['영화내용개수'] = 0
        ResultDict['영화제목'] = '표시할 영화 없음'	

        ResultDict['댓글개수'] = 0
        ResultDict['댓글내용'] = '표시할 댓글 없음'    
        ResultDict['게시글좋아요수'] = 0
        ResultDict['게시글공유수'] = 0
        
        
        ResultDict['평균댓글개수'] = float("{:.2f}".format((replyCnt + moreReplyCnt) / len(articleCnt)))
        ResultDict['평균덧글개수'] = float("{:.2f}".format(replyAndReply / len(articleCnt)))
        ResultDict['전체긍정어사용빈도'] = totCycNumGoodWords
        ResultDict['평균긍정어사용비율'] = float("{:.2f}".format((totCycNumGoodWords / len(articleCnt))))
        
        ResultDict['개요항목개수']

        '''

        #DB INSERT
        try:
            # Server Connection to MySQL:
            databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
            databaseConnection_jeniel.insert_record_origin_version(
                                                            ResultDict['사용자이름'],
                                                            ResultDict['페이스북페이지ID'],
                ''.join(ResultDict['전체기본정보']),
                '_'.join(ResultDict['전체연락처정보']),
                '_'.join(ResultDict['웹사이트및소셜링크정보']),
                '_'.join(ResultDict['소개글']),
                                                            str(ResultDict['프로필게시개수']),
                                                            ResultDict['전체프로필정보'],
                                                            str(ResultDict['친구수']),
                                                            str(ResultDict['좋아요클릭한사람수']),
                                                            str(ResultDict['이미지에좋아요클릭한사람수']),
                                                            str(ResultDict['동영상수']),
                                                            str(ResultDict['사진수']),
                                                            str(ResultDict['T_SCORE']),
                                                            str(ResultDict['C_SCORE']),
                                                            str(ResultDict['M_SCORE']),
                '_'.join(ResultDict['DETAIL']),
                                                            str(ResultDict['모든친구']),        #allFrndCnt
                                                            str(ResultDict['함께아는친구']),    #knowEachFrnd
                                                            str(ResultDict['최근추가한친구']),  #latestAddFrnd
                                                            str(ResultDict['대학교']),          #univFrnd
                                                            str(ResultDict['거주지']),          #homeFrnd
                                                            str(ResultDict['출신지']),          #homeTwnFrnd
                                                            str(ResultDict['팔로워']),          #fllwerCnt
                                                            str(ResultDict['좋아요모두']),      #likeHobbyAllCnt
                                                            str(ResultDict['영화']),            #movieLikeCnt
                                                            str(ResultDict['TV프로그램']),      #tvLikeCnt
                                                            str(ResultDict['음악']),            #musicLikeCnt
                                                            str(ResultDict['책']),              #bookLikeCnt
                                                            str(ResultDict['스포츠팀']),        #sportsTemaLikeCnt
                                                            str(ResultDict['음식점']),          #foodPlaceCnt
                                                            str(ResultDict['앱과게임']),        #appAndGamesCnt
                                                            str(ResultDict['장소']),            #visitedPlc
                                                            str(ResultDict['도시']),            #visitedCity
                                                            str(ResultDict['최근에가본곳']),    #recentVisitPlc
                                                            str(ResultDict['이벤트내용개수']),  #evntCnt
                                                            str(ResultDict['이벤트내용']),      #eventContents
                                                            str(ResultDict['봤어요']),          #sawItCnt
                                                            str(ResultDict['영화']),            #sawMovieCnt
                                                            str(ResultDict['영화내용개수']),    #sawMovieContentCnt
                                                            str(ResultDict['영화제목']),        #sawMovieTitle
                                                            str(ResultDict['댓글개수']),        #replyCnt
                                                            str(ResultDict['댓글내용']),        #replyContents
                                                            str(ResultDict['게시글좋아요수']),  #articleLikeCnt
                                                            str(ResultDict['게시글공유수']),    #articleShareCnt

                                                str(ResultDict['평균댓글개수']),                #avgReplyCnt
                                                str(ResultDict['평균덧글개수']),                #avgReplyAndReply
                                                str(ResultDict['전체긍정어사용빈도']),          #gdExpssCnt
                                                str(ResultDict['평균긍정어사용비율']),          #avgGdExpssRate
                                                str(ResultDict['개요항목개수'])                 #aboutInfoCnt
            )


        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

        returnedValue_TCMCountGen = True



    else:

        print('M SCORE를 산출할 수 없습니다.')
        ResultDict.update({'T_SCORE': tScoreCount, 'C_SCORE': cScoreCount, 'M_SCORE': 0})


        #DB INSERT
        try:
            # Server Connection to MySQL:
            databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
            databaseConnection_jeniel.insert_record_origin_version(
                                                            ResultDict['사용자이름'],
                                                            ResultDict['페이스북페이지ID'],
                ''.join(ResultDict['전체기본정보']),
                '_'.join(ResultDict['전체연락처정보']),
                '_'.join(ResultDict['웹사이트및소셜링크정보']),
                '_'.join(ResultDict['소개글']),
                                                            str(ResultDict['프로필게시개수']),
                                                            ResultDict['전체프로필정보'],
                                                            str(ResultDict['친구수']),
                                                            str(ResultDict['좋아요클릭한사람수']),
                                                            str(ResultDict['이미지에좋아요클릭한사람수']),
                                                            str(ResultDict['동영상수']),
                                                            str(ResultDict['사진수']),
                                                            str(ResultDict['T_SCORE']),
                                                            str(ResultDict['C_SCORE']),
                                                            str(ResultDict['M_SCORE']),
                '_'.join(ResultDict['DETAIL']),
                                                            str(ResultDict['모든친구']),        #allFrndCnt
                                                            str(ResultDict['함께아는친구']),    #knowEachFrnd
                                                            str(ResultDict['최근추가한친구']),  #latestAddFrnd
                                                            str(ResultDict['대학교']),          #univFrnd
                                                            str(ResultDict['거주지']),          #homeFrnd
                                                            str(ResultDict['출신지']),          #homeTwnFrnd
                                                            str(ResultDict['팔로워']),          #fllwerCnt
                                                            str(ResultDict['좋아요모두']),      #likeHobbyAllCnt
                                                            str(ResultDict['영화']),            #movieLikeCnt
                                                            str(ResultDict['TV프로그램']),      #tvLikeCnt
                                                            str(ResultDict['음악']),            #musicLikeCnt
                                                            str(ResultDict['책']),              #bookLikeCnt
                                                            str(ResultDict['스포츠팀']),        #sportsTemaLikeCnt
                                                            str(ResultDict['음식점']),          #foodPlaceCnt
                                                            str(ResultDict['앱과게임']),        #appAndGamesCnt
                                                            str(ResultDict['장소']),            #visitedPlc
                                                            str(ResultDict['도시']),            #visitedCity
                                                            str(ResultDict['최근에가본곳']),    #recentVisitPlc
                                                            str(ResultDict['이벤트내용개수']),  #evntCnt
                                                            str(ResultDict['이벤트내용']),      #eventContents
                                                            str(ResultDict['봤어요']),          #sawItCnt
                                                            str(ResultDict['영화']),            #sawMovieCnt
                                                            str(ResultDict['영화내용개수']),    #sawMovieContentCnt
                                                            str(ResultDict['영화제목']),        #sawMovieTitle
                                                            str(ResultDict['댓글개수']),        #replyCnt
                                                            str(ResultDict['댓글내용']),        #replyContents
                                                            str(ResultDict['게시글좋아요수']),  #articleLikeCnt
                                                            str(ResultDict['게시글공유수']),    #articleShareCnt

                                                str(ResultDict['평균댓글개수']),                #avgReplyCnt
                                                str(ResultDict['평균덧글개수']),                #avgReplyAndReply
                                                str(ResultDict['전체긍정어사용빈도']),          #gdExpssCnt
                                                str(ResultDict['평균긍정어사용비율']),          #avgGdExpssRate
                                                str(ResultDict['개요항목개수'])                 #aboutInfoCnt
            )


        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

        returnedValue_TCMCountGen = True



    # 리뷰수 추출
    reviewsCnt_str = '0'
    try:
        # https://www.facebook.com/kpokem/reviews
        driver.get('https://www.facebook.com/' + user_fbpage_url + '/reviews')
        print('리뷰 추출 페이지 확인 : ', driver.current_url)

        autoScrolled_data = driver.page_source
        soup_html = bs(autoScrolled_data, 'html.parser')

        reviewsCnt_str = soup_html.select(
            '#pagelet_timeline_medley_reviews > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a > span:nth-of-type(2)')[
            0].text
        reviewsCnt_int = int(reviewsCnt_str)

        print('모든 리뷰 수 :', reviewsCnt_int)


        databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
        databaseConnection_jeniel.update_ReviewCnt(reviewsCnt_str, user_fbpage_url)


    except Exception as e:
        print('리뷰수 정보가 노출되지 않았습니다. ', e)
        print('모든 리뷰 수 :', reviewsCnt_str)

        databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
        databaseConnection_jeniel.update_ReviewCnt(reviewsCnt_str, user_fbpage_url)

    # 팔로우 수 추출
    frndCnt = '0'
    try:
        driver.get('https://www.facebook.com/' + user_fbpage_url + '/followers')
        print('팔로우 페이지 확인 :', driver.current_url)

        crawled_followsData = driver.page_source
        soup_html = bs(crawled_followsData, 'html.parser')

        frndTitle = soup_html.select(
            '#pagelet_timeline_medley_friends > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(7) > span:nth-of-type(1)')[
            0].text

        frndCnt = soup_html.select(
            '#pagelet_timeline_medley_friends > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type(7) > span:nth-of-type(2)')[
            0].text

        print(frndTitle, '-', frndCnt)

        databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
        databaseConnection_jeniel.update_FollowerCnt(frndCnt, user_fbpage_url)
    except Exception as e:
        print('팔로우 수 노출되지 않았습니다.')
        databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
        databaseConnection_jeniel.update_FollowerCnt('0', user_fbpage_url)

    # 사진첩의 댓글 개수, 좋아요 개수
    autoScrollerContentsPhotoText(user_fbpage_url, driver)




    print('returnedValue_TCMCountGen :', returnedValue_TCMCountGen)

    returnTCMResult = {}
    returnTCMResult['trueOrFalse'] = returnedValue_TCMCountGen
    returnTCMResult['tcmScore'] = ResultDict

    return returnTCMResult



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
        time.sleep(2)
        userContent_list_result = autoScrolled_data_soup_html.find_all('div', attrs={'class': 'userContentWrapper'})

    except Exception as e:
        print('autoScrollerUserWrapperContents에서 userContentWrapper를 찾지 못했습니다. -> ', e)
        #userContent_list_result is None
        userContent_list_result = None

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
            #각 사진 블록 내의 항목 값 추출
            userContent_list_result = autoScrolled_data_soup.find_all('span', attrs={'class': '_2ieq _50f7'})
        except:
            print('사진 블록 내의 항목 값 추출 값이 없습니다.')

    hangmok_pictureCntT = 0
    gaesimul_pictureCnt = 0
    try:
        for picture_index in userContent_list_result:
            pictureDiscribText = picture_index.text.split(' · ')

            print('항목 및 게시물 값 추출 테스트 출력 : ', pictureDiscribText)

            try:
                hangmok_matching = [s for s in pictureDiscribText if "항목" in s]
            except Exception as e:
                print('항목 부분 구조 변경-', e)
                hangmok_matching = '항목 0개'

            hangmok_pictureCnt = int(str(hangmok_matching).split()[1].split('개')[0])

            try:
                gaesimul_matching = [s for s in pictureDiscribText if "게시물" in s]
            except Exception as e:
                print('게시물 부분 구조 변경-', e)
                gaesimul_matching = '게시물 0개'
            gaesimul_pictureCnt = int(str(gaesimul_matching).split()[1].split('개')[0])

            hangmok_pictureCntT += hangmok_pictureCnt
            gaesimul_pictureCnt += gaesimul_pictureCnt

        print('총 사진 수: ', hangmok_pictureCntT, ', ', '총 게시물 수: ', gaesimul_pictureCnt)
    except Exception as e:
        print('항목 내에서의 총 사진 수: ', hangmok_pictureCntT, ', ', '항목 내에서의 총 게시물 수: ', gaesimul_pictureCnt)

    return hangmok_pictureCntT



#autoScroller관련 함수 =========================================================================

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 2

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
            textDataList += textData
        print('textDataList :', textDataList)
        textDataListVal = ''
        corp_cnt = 0

        try:
            if '엘지' in textDataList:
                print('엘지(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '현대' in textDataList:
                print('현대(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '기아' in textDataList:
                print('기아(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '삼성' in textDataList:
                print('삼성(이)라는 글자가 노출되었습니다.')
                corp_cnt += 7
                textDataListVal += textDataList

            if '에스케이' in textDataList:
                print('에스케이(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '한국' in textDataList:
                print('한국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '케이티' in textDataList:
                print('케이티(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '지에스' in textDataList:
                print('지에스(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '신한' in textDataList:
                print('신한(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '하나' in textDataList:
                print('하나(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '한화' in textDataList:
                print('한화(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '우리' in textDataList:
                print('우리(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '대우' in textDataList:
                print('대우(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '두산' in textDataList:
                print('두산(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '롯데' in textDataList:
                print('롯데(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '케이비' in textDataList:
                print('케이비(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '흥국' in textDataList:
                print('흥국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '기업' in textDataList:
                print('기업(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if 'S-oil' in textDataList:
                print('s-oil(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '대한' in textDataList:
                print('대한(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '아시아나' in textDataList:
                print('아시아나(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '동국' in textDataList:
                print('동국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '코오롱' in textDataList:
                print('코오롱(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '네이버' in textDataList:
                print('네이버(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '다음' in textDataList:
                print('다음(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '사원' in textDataList:
                print('사원증(이)라는 글자가 노출되었습니다.')
                corp_cnt += 7
                textDataListVal += textDataList

            print(corp_cnt)
            print('textDataListVal', textDataListVal)
            #readCSV(textDataListVal)

        except Exception as es:
            print('기업 이름이 검색되지 않았습니다. : ', es)

    except Exception as readCsvEx:
        print('AutoCrolling 한 객체가 없습니다. ')



#CSV 파일 읽기 ======================================================================
def readCSV(searchTValue):

    #C:\python_project\aster879_project\PycharmProjects
    reader = csv.reader(
        open('C:\\python_project\\aster879_project\\PycharmProjects\\1_500Corp.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|')

    print(searchTValue)

    corpList = []
    for row in reader:
        corpList.append(', '.join(row))

    returnScore = 0
    #500대 기업 loop
    for row2 in corpList:
        returnScore1 = 0
        for loopInt in range(len(searchTValue)):
            print('searchTValue['+str(loopInt)+'] :', searchTValue[loopInt])
            if searchTValue[loopInt] in row2:
                returnScore1 += 10
                break
        returnScore += returnScore1
    print(returnScore)
    return returnScore

