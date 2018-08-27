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
    print('last_height : ', last_height)
    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 5):

        print('@ : ', cyc)
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        print('new_height : ', new_height)

        if new_height == last_height:
            print('같다고?')
            break
        last_height = new_height
        print('값 대입해')

        # autoScroll crawling data 가져오기
        autoScrolled_data_soup = bs(driver.page_source, 'html.parser')

    return autoScrolled_data_soup



def readCSV_goodExpressions():

    #C:\python_project\aster879_project\PycharmProjects
    reader = csv.reader(
        open('C:\\dev_syhan\\aster_jeniel_test_dev_201808\\긍정어.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|')

    #print('함수안에서의 전달받은 값 : ', searchTValue)

    wordList = []
    for row in reader:
        wordList.append(', '.join(row))
    #print('긍정어 wordList : ', wordList)

    return wordList



chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

prefs = {}
prefs['profile.default_content_setting_values.notifications'] = 2
chrome_options.add_experimental_option('prefs', prefs)
driver_chrome = r"C:\python_project\chromedriver.exe"

# go to Google and click the I'm Feeling Lucky button
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)

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

try:

    articleLikeTotCnt = 0
    articleReplyTotCnt = 0
    articleShareTotCnt = 0

    articleNum = 0

    articleCnt = articles_reply_soup.select('#recent_capsule_container > ol > div')
    #print('게시글 개수:', len(articleCnt) )

    if len(articleCnt) is not 0:

        returnExpList = readCSV_goodExpressions()
        # print('단어 리스트 길이 :', len(returnExpList) )


        for articleLength in range(len(articleCnt)):
            #1. 게시글의 등록 날짜 가져오기
            innerArticleCnt = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type('+ str( articleLength + 1 ) +') > div')

            #게시글을 출력하는 묶음 단위가 존재하며, 각 묶음단위별 포함하고 있는 게시글의 갯수가 상이함.
            print('innerArticleCnt : ', len(innerArticleCnt))

            for innerArtclLnth in range(len(innerArticleCnt)):

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

                print('게시글 등록 시간:', updatedTime)

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

                # 2. 게시글의 작성된 글 내용 가져오기
                print('updatedArticleContents :', updatedArticleContents)

                articles_reply_data.append(updatedArticleContents)

                article_reply_text = '@'.join(articles_reply_data)





                # 2-2. 게시글의 내용(단어)를 리스트로 변환
                # 2-3. 게시글 내용 리스트와 긍정어 단어 리스트의 비교 분석 및 빈도수 측정
                cycNum = 0
                #returnExpList : 긍정어.csv 파일에서 가져온 긍정어 항목
                for expListLngth in range(len(returnExpList)):
                    #긍정어 표현 목록 길이 만큼 반복문을 돈다.

                    #print('index:', expListLngth)

                    #articles_reply_data :  게시글에서 추출한 단어 리스트
                    if returnExpList[expListLngth] in articles_reply_data:
                        #긍정어.csv에서 가져온 단어가 게시글에서 추출한 단어 리스트에 존재하는지.

                        print('일치하는 긍정어 있음 :', returnExpList[expListLngth])

                        cycNum += 1
                        #print('cycNum:', cycNum)
                        continue

                    else:
                        #print('일치하는 긍정어 없음')
                        cycNum += 1
                        #print('cycNum:', cycNum)
                        continue



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
                articleLikeCnt : 김동근님 외 239명
                '''


                #댓글영역
                #댓글 개수
                try:
                    articleReplyContentsList = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(1) > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1)')[0].text
                except Exception as e:
                    print('댓글영역 > 댓글 개수 부분 에러')

                #댓글 12개
                '''
                예)
                articleReplyContentsList : 댓글 103개
                또는
                articleReplyContentsList : 댓글 48개공유 13회
                '''

                articleReplyContentsList0 = ''
                articleReplyContentsList1 = ''

                try:
                    articleReplyContentsList0 = articleReplyContentsList.split(" ")[0]
                    #articleReplyContentsList0 = '댓글'

                    try:
                        articleReplyContentsList1 = articleReplyContentsList.split(" ")[1]
                        #articleReplyContentsList1 = 'XX개공유'
                        articleShareCnt = 0

                        #articleReplyContentsList.replace(" ", "") = 댓글XX개공유XX회
                        articleShareCnt = int(articleReplyContentsList.replace(" ", "").split("공유")[1].replace("회", ""))
                        articleShareTotCnt += articleShareCnt
                        #print('articleShareCnt :', articleShareCnt)

                    except Exception as e:
                        print('공유 횟수는 없습니다.')

                        articleReplyContentsCnt = articleReplyContentsList1.split("개")[0]
                        articleReplyTotCnt += int(articleReplyContentsCnt)

                except Exception as e:

                    print('댓글 이나 게시 공유가 없습니다.')


                #댓글영역
                #댓글 추출
                # 3. 게시글의 댓글 가져오기(댓글중 텍스트와 텍스트 아닌 것을 구분하기)
                try:
                    articleReplyContentsList = articles_reply_soup.select('#recent_capsule_container > ol > div:nth-of-type(' + str(
                        articleLength + 1) + ') > div:nth-of-type(' + str(
                        innerArtclLnth + 1) + ') > div > div:nth-of-type(3) > div:nth-of-type(2) > form > div:nth-of-type(2)')


                except Exception as e:
                    print('댓글영역 > 댓글 추출 부분 에러')


        print('articleLikeTotCnt: ', articleLikeTotCnt)
        print('articleReplyTotCnt: ', articleReplyTotCnt)
        print('articleShareCnt :', articleShareTotCnt)

        articles_reply_data_dic['댓글개수'] = articleReplyTotCnt
        articles_reply_data_dic['게시글좋아요수'] = articleLikeTotCnt
        articles_reply_data_dic['게시글공유수'] = articleShareTotCnt
        articles_reply_data_dic['댓글내용'] = article_reply_text




except Exception as e:
    print('게시글이 공개되지 않았습니다. ')




