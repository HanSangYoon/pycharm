#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def __getHTMLDoc_beautifulSoup4(driver, URL):

    driver.get(URL)

    html_src_chrome = driver.page_source
    soupHTMLDoc = bs(html_src_chrome, 'html.parser')

    return soupHTMLDoc


def autoScroller(driver, URL):

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
    for cyc in range(0, 3):

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

    try:
        #C:\python_project\aster879_project\PycharmProjects
        reader = csv.reader( open('C:\\micro\\dev_syhan\\aster_jeniel_test_dev_201808\\긍정어4.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|' )
    except Exception as e:
        print('readCSV 부분:', e)

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




chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

prefs = {}
prefs['profile.default_content_setting_values.notifications'] = 2
chrome_options.add_experimental_option('prefs', prefs)
#driver_chrome = r"C:\Users\micro\dev_syhan\chromedriver.exe"

driver_chrome = r"C:\dev_syhan\aster_jeniel_test_dev_201808\chromedriver.exe"

# go to Google and click the I'm Feeling Lucky button
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)
#driver = webdriver.Chrome(chrome_options=chrome_options)

# url
driver.get('https://www.facebook.com')

user_id = '01027746254'
user_pass = 'Gkstkddbs4$'

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
                driver.find_element_by_xpath('// *[ @ id = "u_0_b"]').click()
                login_or_not = True
            except Exception as ex4:
                print('로그인 버튼 id 값이 u_0_b 가 아닙니다.', ex4)

                try:
                    driver.find_element_by_xpath('// *[ @ id = "u_0_d"]').click()
                    login_or_not = True
                except Exception as ex5:
                    print('로그인 버튼 id 값이 u_0_d 가 아닙니다.', ex5)

                    try:
                        driver.find_element_by_xpath('// *[ @ id = "u_0_e"]').click()
                        login_or_not = True
                    except Exception as ex6:
                        print('로그인 버튼 id 값이 u_0_e 가 아닙니다.', ex6)

                        try:
                            driver.find_element_by_xpath('// *[ @ id = "u_0_f"]').click()
                            login_or_not = True
                        except Exception as ex7:
                            print('로그인 버튼 id 값이 u_0_f 가 아닙니다.', ex7)

                            try:
                                driver.find_element_by_xpath('// *[ @ id = "u_0_a"]').click()
                                login_or_not = True
                            except Exception as ex8:
                                print('로그인 버튼 id 값이 u_0_a 가 아닙니다.로그인 실패입니다. 소스를 다시 분석해야 합니다.', ex8)
                                login_or_not = False


currTime = str(time.localtime().tm_year) + '년' + str(time.localtime().tm_mon) + '월' + str(
    time.localtime().tm_mday) + '일'

user_fbpage_id = 'kpokem'


#게시글 댓글 수 정보 추가- 타임라인

userFacebook_currentUrl = 'https://www.facebook.com/' + user_fbpage_id

#driver.get('https://www.facebook.com/' + user_fbpage_id)
#articles_reply_html = driver.page_source
#articles_reply_soup = bs(articles_reply_html, 'html.parser')
articles_reply_soup = autoScroller(driver, userFacebook_currentUrl)

articles_reply_data = []
articles_reply_data_dic = {}


articles_reply_data_dic['댓글개수'] = 0
articles_reply_data_dic['댓글내용'] = '표시할 댓글 없음'

articles_reply_data_dic['게시글좋아요수'] = 0
articles_reply_data_dic['게시글공유수'] = 0

articles_reply_data_dic['수집한게시글개수'] = 0


articles_reply_data_dic['평균댓글개수'] = 0
articles_reply_data_dic['평균덧글개수'] = 0
articles_reply_data_dic['전체긍정어사용빈도'] = 0
articles_reply_data_dic['평균긍정어사용비율'] = 0

articles_reply_data_dic['페이스북게시글등록시간'] =''


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

    articleRegisterDate = []

    articleCnt = articles_reply_soup.select('#recent_capsule_container > ol > div')
    #print('게시글 개수:', len(articleCnt) )

    if len(articleCnt) is not 0:

        for articleLength in range(len(articleCnt)):
            #1. 게시글의 등록 날짜 가져오기
            innerArticleCnt = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type('+ str( articleLength + 1 ) +') > div')

            #게시글을 출력하는 묶음 단위가 존재하며, 각 묶음단위별 포함하고 있는 게시글의 갯수가 상이함.

            print()
            print('내부의 묶음게시글 개수 : ', len(innerArticleCnt))

            for innerArtclLnth in range(len(innerArticleCnt)):
                #1. 게시글 내용 리스트화
                #2. 게시글 내용 vs 긍정어 단어 매칭 빈도수 측정(확률로 계산하면 될 듯)

                #게시글 영역
                #게시글 등록 시간
                try:
                    updatedTime = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type('+ str(
                        innerArtclLnth + 1 ) +') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div > span:nth-of-type(3) > span > a > abbr > span')[
                        0].text
                except Exception as e:
                    updatedTime = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > div > span:nth-of-type(3) > span > abbr > span')[
                        0].text

                print()
                print('현재시간 :', currTime)
                print('게시글 등록 시간_origin:', updatedTime)

                # 올해 게시물일 경우
                # 현재의 년월일값 : currTime = str(time.localtime().tm_year) + '년' + str(time.localtime().tm_mon) + '월' + str(time.localtime().tm_mday) + '일'
                currYear = '%04d' % time.localtime().tm_year
                currMnth = '%02d' % time.localtime().tm_mon
                currDays = '%02d' % time.localtime().tm_mday

                # 현재시간
                rightNowTime = currYear + currMnth + currDays

                print('rightNowTime:', rightNowTime)

                try:
                    # 게시글 등록 월
                    articleUpdatedTimeMonth = '%02d' % int(updatedTime.replace(" ", "").split("오")[0].split('월')[0])
                    print('articleUpdatedTimeMonth: ', articleUpdatedTimeMonth)

                except Exception as e:
                    print('게시글 등록 월 Exception:', e)
                    articleUpdatedTimeMonth = currMnth

                try:
                    # 게시글 등록 일
                    articleUpdatedTimedays = '%02d' % int(updatedTime.replace(" ", "").split("오")[0].split('월')[1].replace("일", ""))
                    print('articleUpdatedTimedays: ', articleUpdatedTimedays)

                except Exception as e:
                    print('게시글 등록 일 Exception:', e)
                    articleUpdatedTimedays = currDays

                print(articleUpdatedTimeMonth, ',', articleUpdatedTimedays)

                if '년' in updatedTime.replace(" ", "").split("오")[0]:
                    print('올해 게시물 아님')
                    articleUpdatedTimeYear = '%02d' % updatedTime.replace(" ", "").split("오")[0].split('월')[0]

                else:
                    print('올해 게시물임')
                    monthList1 = [1, 3, 5, 7, 8, 10, 12]
                    monthList2 = [4, 6, 9, 11]

                    # updatedTime = currTimeUpdated을 만들기 위한 조건문
                    if '시간' in updatedTime.replace(" ", ""):
                        print('1')
                        print(updatedTime.split('시간')[0])
                        # 현재시간 - 표시된 시간 = 경과한 시간값
                        #updatedTime = rightNowTime
                        #print('updatedTime:', updatedTime)

                        try:
                            passedHour = int(str(time.localtime().tm_hour)) - int(updatedTime.split('시간')[0])
                        except Exception as e:
                            print('시간 생성 에러')

                        if passedHour < 0:
                            print('int(str(time.localtime().tm_mon)) : ', int(str(time.localtime().tm_mon)))

                            # 31일로 끝나는 달의 경우
                            if int(str(time.localtime().tm_mday)) == 1 and int(
                                    str(time.localtime().tm_mon)) in monthList1:
                                yearVal = '%04d' % time.localtime().tm_year
                                mnthVal = '%02d' % time.localtime().tm_mon
                                #daysVal = '%02d' % (int(time.localtime().tm_mday))

                                currTimeUpdated = yearVal + mnthVal + '31'

                            # 30일로 끝나는 달의 경우
                            elif int(str(time.localtime().tm_mday)) == 1 and int(
                                    str(time.localtime().tm_mon)) in monthList2:
                                yearVal = '%04d' % time.localtime().tm_year
                                mnthVal = '%02d' % time.localtime().tm_mon
                                #daysVal = '%02d' % (int(time.localtime().tm_mday))

                                currTimeUpdated = yearVal + '년' +mnthVal +'월' + '30일'

                            # 2월의 경우
                            elif int(str(time.localtime().tm_mon)) == 2:
                                if (int(str(time.localtime().tm_year) % 4)) == 0:
                                    if (int(str(time.localtime().tm_year) % 4) % 100) == 0:

                                        # 윤년 인 경우
                                        if (int(str(time.localtime().tm_year) % 4) % 400) == 0:
                                            print("{0} 윤년".format(int(str(time.localtime().tm_year) % 4)))
                                            yearVal = '%04d' % time.localtime().tm_year
                                            # mnthVal = '%02d' % time.localtime().tm_mon
                                            # daysVal = '%02d' % (int(time.localtime().tm_mday) - 1)

                                            currTimeUpdated = yearVal + '년02월29일'

                                        # 윤년이 아닌 경우
                                        else:
                                            print("{0} 윤년아님".format(int(str(time.localtime().tm_year) % 4)))
                                            yearVal = '%04d' % time.localtime().tm_year
                                            # mnthVal = '%02d' % time.localtime().tm_mon
                                            # daysVal = '%02d' % (int(time.localtime().tm_mday) - 1)

                                            currTimeUpdated = yearVal + '년02월28일'
                                    #윤년인 경우
                                    else:
                                        print("{0} 윤년".format(int(str(time.localtime().tm_year) % 4)))
                                        yearVal = '%04d' % time.localtime().tm_year
                                        #mnthVal = '%02d' % time.localtime().tm_mon
                                        #daysVal = '%02d' % (int(time.localtime().tm_mday) - 1)

                                        currTimeUpdated = yearVal + '년02월29일'

                                #윤년이 아닌 경우
                                else:
                                    print("{0} 윤년아님".format(int(str(time.localtime().tm_year) % 4)))
                                    yearVal = '%04d' % time.localtime().tm_year
                                    #mnthVal = '%02d' % time.localtime().tm_mon
                                    #daysVal = '%02d' % (int(time.localtime().tm_mday) - 1)

                                    currTimeUpdated = yearVal + '년02월28일'
                            else:
                                yearVal = '%04d' % time.localtime().tm_year
                                mnthVal = '%02d' % time.localtime().tm_mon
                                daysVal = '%02d' % (int(time.localtime().tm_mday)-1)

                                currTimeUpdated = yearVal + mnthVal + daysVal

                            print('currTimeUpdated:', currTimeUpdated)
                            updatedTime = currTimeUpdated

                    elif '분' in updatedTime.replace(" ", ""):
                        # 동시간 대라고 여김
                        updatedTime = rightNowTime

                    elif '분전' in updatedTime.replace(" ", ""):
                        # 동시간 대라고 여김
                        updatedTime = rightNowTime

                    elif '어제' in updatedTime.replace(" ", ""):
                        yearVal = '%04d' % time.localtime().tm_year
                        mnthVal = '%02d' % time.localtime().tm_mon
                        daysVal = '%02d' % (int(time.localtime().tm_mday) - 1)

                        currTimeUpdated = yearVal + mnthVal + daysVal

                        updatedTime = currTimeUpdated

                        print('어제:',updatedTime )

                    else:
                        print(articleUpdatedTimeMonth, ',', articleUpdatedTimedays)

                        yearVal = '%04d' % time.localtime().tm_year
                        mnthVal = articleUpdatedTimeMonth
                        daysVal = articleUpdatedTimedays

                        currTimeUpdated = yearVal + mnthVal + daysVal

                        updatedTime = currTimeUpdated

                #print(updatedTime)
                articles_reply_data_dic['페이스북게시글등록시간'] = updatedTime

                # STEP 1. 각 게시물의 게시등록 날짜를 리스트로 받아오기
                articleRegisterDate.append(updatedTime)

                print('articleRegisterDate:', articleRegisterDate)












                articleNum += 1

                print('게시글 번호 :', articleNum)

                #게시글 영역
                #게시글 (작성)내용
                try:
                    updatedArticleContents = articles_reply_soup.select(
                        '#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type(' + str(
                            innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2)')[0].text

                except Exception as e:
                    updatedArticleContents = articles_reply_soup.select(
                        '#recent_capsule_container > ol > div:nth-of-type(' + str(
                            articleLength + 1) + ') > div:nth-of-type('+ str(
                            innerArtclLnth + 1 ) +') > div > div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1)')[0].text

                # 2-1. 게시글의 작성된 글 내용 가져오기
                print('updatedArticleContents :', updatedArticleContents)
                updatedArticleContentsList = updatedArticleContents.split(" ")
                print(updatedArticleContentsList)

                articles_reply_data = articles_reply_data + updatedArticleContentsList
                article_reply_text = '@'.join(articles_reply_data)

                # 2-2. 게시글의 내용(단어)를 리스트로 변환
                # 2-3. 게시글 내용 리스트와 긍정어 단어 리스트의 비교 분석 및 빈도수 측정
                returnExpList = readCSV_goodExpressions()
                #print('단어 리스트 길이 :', len(returnExpList) )

                cycNumGoodWords = 0
                cycNumElseWords = 0
                #returnExpList : 긍정어.csv 파일에서 가져온 긍정어 항목
                for expListLngth in range(len(returnExpList)):
                    #긍정어 표현 목록 길이 만큼 반복문을 돈다.

                    #articles_reply_data :  게시글에서 추출한 단어 리스트
                    if returnExpList[expListLngth] in updatedArticleContentsList:
                        #긍정어.csv에서 가져온 단어가 게시글에서 추출한 단어 리스트에 존재하는지.

                        print('일치하는 긍정어 있음 :', returnExpList[expListLngth])

                        cycNumGoodWords += 1
                        totCycNumGoodWords += 1
                        continue

                    else:
                        cycNumElseWords += 1
                        continue

                #각 게시물별 긍정어 사용 확률값
                rateGoodWords = (cycNumGoodWords / len(articles_reply_data))
                goodWordsUsingRate = float("{:.2f}".format(rateGoodWords))

                print('각 게시물 당 긍정어 사용 비율:', goodWordsUsingRate)

                # 3. 댓글과 덧글의 작성자명을 추출
                # 4. 각 게시물당 댓글 작성자명을 리스트로 변경, 같은 이름의 빈도수를 추출
                # 5. 게시물과 댓글의 내용을 리스트로 변경하여 긍정어 빈도수 추출
                # 6. 댓글 내용 vs 긍정어 단어 매칭 빈도수 측정(확률로 계산하면 될 듯)

                #댓글영역
                #좋아요 수
                try:
                    articleLikeCnt = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1 ) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(1) > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > div > a > span:nth-of-type(2) > span')[0].text
                except Exception as e:
                    print('댓글영역 > 좋아요 수 부분 에러')

                print('articleLikeCnt :', articleLikeCnt)

                articleLikeCnt = articleLikeCnt.split(" ")[2].split('명')[0]

                articleLikeTotCnt += int(articleLikeCnt)

                '''
                예)
                articleLikeCnt : XXX님 외 239명
                '''


                #댓글영역
                #댓글 개수
                try:
                    articleReplyContentsCnt = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(1) > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1)')[0].text
                except Exception as e:
                    print('댓글영역 > 댓글 개수 부분 에러')

                #댓글 12개
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
                    #articleReplyContentsCnt0 = '댓글'

                    try:
                        articleReplyContentsCnt1 = articleReplyContentsCnt.split(" ")[1]
                        #articleReplyContentsCnt1 = 'XX개공유'
                        articleShareCnt = 0

                        #articleReplyContentsCnt.replace(" ", "") = 댓글XX개공유XX회
                        articleShareCnt = int(articleReplyContentsCnt.replace(" ", "").split("공유")[1].replace("회", ""))
                        articleShareTotCnt += articleShareCnt
                        #print('articleShareCnt :', articleShareCnt)

                    except Exception as e:
                        print('공유 횟수는 없습니다.')

                        articleReplyContentsCnt = articleReplyContentsCnt1.split("개")[0]
                        articleReplyTotCnt += int(articleReplyContentsCnt)

                except Exception as e:

                    print('댓글 이나 게시 공유가 없습니다.')


                #댓글영역
                #댓글 추출
                # 3. 게시글의 댓글 가져오기(댓글중 텍스트와 텍스트 아닌 것을 구분하기)

                try:
                    articleReplyContentsList = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div')

                    print('노출된 댓글의 개수:', len(articleReplyContentsList))

                    testPrint = ''
                    try:
                        testPrint = articles_reply_soup.select(
                            '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                articleLength + 1) + ') > div:nth-of-type(' + str(
                                innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(1) > div > div:nth-of-type(2) > a')[0].text

                        testPrintList = testPrint.split(" ")
                        print('testPrintList :', testPrintList)

                        moreReplyCnt = int(testPrintList[1].replace("개",""))
                        print('더 존재하는 댓글 : ', moreReplyCnt)

                    except Exception as e:
                        print()

                    replyAndReply = 0
                    articleReplyContentsWriterList = []
                    for exposedReplyLength in range(len(articleReplyContentsList)):
                        print('댓글 No.', str(exposedReplyLength + 1) )

                        replyReply = 0

                        if '보기' in testPrint:
                            try:
                                #댓글 작성자 이름 추출
                                articleReplyContentsWriter = articles_reply_soup.select(
                                    '#recent_capsule_container > ol > div:nth-of-type(' + str(
                                        articleLength + 1) + ') > div:nth-of-type(' + str(
                                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2) > div > div:nth-of-type(1) > div > div:nth-of-type(' + str(
                                        exposedReplyLength + 2) + ') > div > div > div')[0].text

                                articleReplyContentsWriterList.append(articleReplyContentsWriter.split("  ")[0] )
                                #print('게시글 No.', articleNum, '댓글작성자 리스트:', articleReplyContentsWriterList)

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

                                articleReplyContentsWriterList.append(articleReplyContentsWriter.split("  ")[0] )


                                replyCnt += 1
                            except Exception as e:
                                print('댓글 가져오는 부분 -2 : 댓글에 덧글이 존재함', e)
                                replyAndReply += 1

                    print('게시글 No.', articleNum, '댓글작성자 리스트:', articleReplyContentsWriterList)
                    print('게시물 No.', articleNum, '의 총 "댓글" 개수:', (replyCnt + moreReplyCnt) )
                    print('게시물 No.', articleNum, '의 총 "덧글" 개수:', replyAndReply)

                except Exception as e:
                    print('댓글영역 > 댓글 추출 부분 에러')

        print('게시글 등록날짜 리스트:', articleRegisterDate)

        #현재 월의 게시물 찾기
        yrVal = '%04d' % time.localtime().tm_year
        mnthVal = '%02d' % time.localtime().tm_mon

        dateVal = yrVal+mnthVal
        print('dateVal:', dateVal)

        regArticleDateCnt = 0

        for regDateLength in range(len(articleRegisterDate)):
            #print('regDateLength:', regDateLength)
            #print('@:', articleRegisterDate[regDateLength].count(dateVal))
            if dateVal in articleRegisterDate[regDateLength]:
                regArticleDateCnt += 1
                continue
            else:
                print('해당 월값이 포함되지 않는 시기의 게시물이 있음.')
                continue


        print('%02d' % time.localtime().tm_mon, '월 게시글 개수:', regArticleDateCnt)


        #전 월의 게시물 찾기
        #yrVal = '%04d' % time.localtime().tm_year
        mnthVal2 = '%02d' % (time.localtime().tm_mon-1)

        dateVal_pre = yrVal+mnthVal2
        print('dateVal_pre:', dateVal_pre)

        regArticleDateCnt2 = 0

        for regDateLength2 in range(len(articleRegisterDate)):
            #print('regDateLength:', regDateLength)
            #print('@:', articleRegisterDate[regDateLength].count(dateVal))
            if dateVal_pre in articleRegisterDate[regDateLength2]:
                regArticleDateCnt2 += 1
                continue
            else:
                print('해당 월값이 포함되지 않는 시기의 게시물이 있음.')
                continue


        print('%02d' % (time.localtime().tm_mon-1), '월 게시글 개수:', regArticleDateCnt2)



        print('각 게시글에 대한 평균 댓글 개수 :', ( (replyCnt + moreReplyCnt) /len(articleCnt) ) )
        print('각 게시글에 대한 평균 덧글 개수 :', ( replyAndReply / len(articleCnt) ) )


        print('articleLikeTotCnt: ', articleLikeTotCnt)
        print('articleReplyTotCnt: ', articleReplyTotCnt)
        print('articleShareCnt:', articleShareTotCnt)

        articles_reply_data_dic['수집한게시글개수'] = len(articleCnt)


        articles_reply_data_dic['댓글개수'] = articleReplyTotCnt
        articles_reply_data_dic['게시글좋아요수'] = articleLikeTotCnt
        articles_reply_data_dic['게시글공유수'] = articleShareTotCnt
        articles_reply_data_dic['댓글내용'] = article_reply_text

        articles_reply_data_dic['평균댓글개수'] = float("{:.2f}".format( (replyCnt + moreReplyCnt) /len(articleCnt) ))
        articles_reply_data_dic['평균덧글개수'] = float("{:.2f}".format(replyAndReply / len(articleCnt) ))
        articles_reply_data_dic['전체긍정어사용빈도'] = totCycNumGoodWords
        articles_reply_data_dic['평균긍정어사용비율'] = float("{:.2f}".format(( totCycNumGoodWords / len(articleCnt) )))

        print('TOT:', articles_reply_data_dic)


except Exception as e:
    print('게시글이 공개되지 않았습니다. ')




