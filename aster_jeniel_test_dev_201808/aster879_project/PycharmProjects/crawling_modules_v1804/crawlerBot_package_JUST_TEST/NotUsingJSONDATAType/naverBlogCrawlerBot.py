#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import logging.handlers
import re
import time

import requests
from bs4 import BeautifulSoup

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection


class naverBlogCrawlerBot():
    def __init__(self):
        print('NaverBlogCrawlerBot_start')

global returnedValue_naverBlog
global hereWork

hereWork = 'NaverBlog'

currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

#logger 인스턴스를 생성 및 로그 레벨 설정 logging --> logger
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


# 에러 리스트 생성 함수
def insert_error(error, error_doc, error_lists):
    for i in error_doc:
        error_log = str(error_doc[i]) + " / " + str(error_doc["page"]) + "page / " + str(error_doc["post_number"]) \
                    + "th post / " + error_doc["title"] \
                    + " / http://blog.naver.com/PostList.nhn?blogId=happy_inhatc&currentPage=" + str(
            error_doc["page"])

    error_lists.append(error_log)


def CrawlingByNaverBlogCrawlBot(userNaverBlogURL,userName, userCellPhNum):
    returnedValue_naverBlog = False
    start_time_all = time.time()

    '''
    currDate = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(
        time.localtime().tm_mday) + '-' \
               + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min) + '-' + str(time.localtime().tm_sec)
    '''
    currDate = currTime

    #print(currDate)
    logger.debug('current date =? {}'.format(currDate))

    Results_DictionatuType = {}

    # Session 생성, with 구문 안에서 유지
    with requests.Session() as s:
        total_num = 0
        error_list = []
        ResultNBDict = {}

        blog_id = userNaverBlogURL
        start_p = 1
        end_p = 100

        naverBlog_Tscore = 0
        naverBlog_Cscore = 0
        naverBlog_Mscore = 0


        #naverBlog_returnResult = []
        print("\nCreating File Naver_Blog_Crawling_Result.txt...\n")

        # 파일 열기
        #file = codecs.open("Log_Text_Folder/Naver_Blog_Crawling_Result.txt", 'w', encoding="utf-8")

        ResultNBDict['사용자ID'] = userNaverBlogURL
        ResultNBDict['게시글수'] = 0
        ResultNBDict['금일방문자수'] = 0
        ResultNBDict['전체방문자수'] = 0
        ResultNBDict['게시글내단어수'] = 0
        ResultNBDict['nb_TSCORE'] = 0
        ResultNBDict['nb_CSCORE'] = 0
        ResultNBDict['nb_MSCORE'] = 0

        # 페이지 단위
        for page in range(1, 30 + 1):

            #구분자 표시
            print("=" * 50)
            #file.write("=" * 50 + "\n")

            #doc = collections.OrderedDict()
            doc = {}

            url = "http://blog.naver.com/PostList.nhn?blogId=" + blog_id + "&currentPage=" + str(page)
            r = requests.get(url)


            if (not r.ok):
                print("Page_" + str(page) + "연결 실패, Skip")

                print('본사용자의 네이버 블로그는 크롤링이 불가합니다. ')

                returnedValue_naverBlog = False

                try:
                    # Server Connection to MySQL
                    databaseConnection = mysqlConnection.DatabaseConnection_origin()
                    databaseConnection.update_naverblogRecord(
                        str(ResultNBDict['사용자ID'].replace(" ", "")),
                        str(ResultNBDict['게시글수']),
                        str(ResultNBDict['금일방문자수']),
                        str(ResultNBDict['전체방문자수']),
                        str(ResultNBDict['게시글내단어수']),
                        str(ResultNBDict['nb_TSCORE']),
                        str(ResultNBDict['nb_CSCORE']),
                        str(ResultNBDict['nb_MSCORE']),
                        userCellPhNum
                    )
                except Exception as e_maria:
                    logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

                ResultNBDict['trueOrFalse'] = False

                return ResultNBDict

                break
                #continue

            # html 파싱
            soup = BeautifulSoup(r.text.encode("utf-8"), "html.parser")

            naverCrawledData_dictionary = {}

            #네이버 블로그가 존재하면 기본 TSCORE 15점 부여
            naverCrawledData_dictionary['nb_TSCORE'] = 15

            #전체보기 글 전체 개수 : MSCORE
            post_tot_cnt = soup.find_all('h4', class_='pcol2')

            try:

                #게시글이 존재하는 지 여부 따지기
                print('post_tot_cnt :', post_tot_cnt[0].text.split(" ")[1].replace("개의", "").replace(",", ""))
                postCnt = int(post_tot_cnt[0].text.split(" ")[1].replace("개의", "").replace(",", ""))


                print('포스트 개수 :', postCnt)

                ResultNBDict['게시글수'] = postCnt

                ResultNBDict['금일방문자수'] = 0
                ResultNBDict['전체방문자수'] = 0

                if postCnt >= 5000:
                    naverBlog_Mscore += 20
                elif postCnt < 5000 and postCnt >= 3000:
                    naverBlog_Mscore += 15
                elif postCnt < 3000 and postCnt >= 1000:
                    naverBlog_Mscore += 10
                elif postCnt < 1000 and postCnt >= 500:
                    naverBlog_Mscore += 5
                else:
                    print('게시글 개수가 부족합니다.')

                naverCrawledData_dictionary['nb_MSCORE'] = naverBlog_Mscore
                cycleLength = postCnt / 10

                # 페이지 당 포스트 수 (printPost_# 형식의 id를 가진 태그 수)
                post_count = len(soup.find_all("table", {"id": re.compile("printPost.")}))
                doc['page_' + str(page)] = page
                #naverCrawledData_dictionary[str(doc['page_' + str(page)])] = page
                #print('@#@#:', naverCrawledData_dictionary[str(doc['page_' + str(page)])])

                # 포스트 단위
                for pidx in range(1, post_count + 1):
                    print('-' * 50)
                    #file.write('-' * 50 + "\n")

                    doc['post_number_' + str(pidx)] = pidx
                    post = soup.find("table", {"id": "printPost" + str(pidx)})

                    naverCrawledData_dictionary[str(doc['post_number_' + str(pidx)])] = pidx

                    # 제목 찾기---------------------------
                    title = post.find("h3", {"class": "se_textarea"})

                    # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
                    if (title == None):
                        title = post.find("span", {"class": "pcol1 itemSubjectBoldfont"})

                    if (title != None):
                        doc["title_" + str(pidx)] = title.text.strip()

                        naverCrawledData_dictionary[str(doc["title_" + str(pidx)])] = title.text.strip()
                        #naverCrawledPostData_list.append(list(str(doc['title']).replace(",", "").replace(" ", "")))
                        #print('$$_dictionary', naverCrawledData_dictionary)

                    else:
                        doc["title"] = "TITLE ERROR"

                    # 날짜 찾기---------------------------
                    date = post.find("span", {"class": "se_publishDate pcol2 fil5"})

                    # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
                    if (date == None):
                        date = post.find("p", {"class": "date fil5 pcol2 _postAddDate"})

                    if (date != None):
                        doc['date_'+ currDate] = date.text.replace(". ", "_")
                        naverCrawledData_dictionary[str(doc['date_'+ currDate])] = date.text.replace(". ", "_")

                    else:
                        doc['date_'+ currDate] = "DATE ERROR"
                        naverCrawledData_dictionary[str(doc['date_' + currDate])] = "DATE ERROR"

                        logger.error('ERROR_DATE => {}'.format(currDate))

                    # 내용 찾기---------------------------
                    content = post.find("div", {"class": "se_component_wrap sect_dsc __se_component_area"})

                    # 스마트에디터3 타이틀 제거 임시 적용 (클래스가 다름)
                    if (content == None):
                        content = post.find("div", {"id": "postViewArea"})

                    if (title != None):
                        # Enter 5줄은 하나로
                        doc["content_postNo_" + str(pidx)] = "\n" + content.text.strip().replace("\n" * 5, "\n").replace(".", "__")
                        naverCrawledData_dictionary[str(doc["content_postNo_"+ str(pidx)])] = "\n" + content.text.strip().replace("\n" * 5, "\n")

                        logger.debug( 'DEBUG_CONTENT_postNo_ => {}'.format(str(pidx)) )

                    else:
                        doc["content_postNo_" + str(pidx)] = "CONTENT ERROR"
                        naverCrawledData_dictionary[str(doc["content_postNo_" + str(pidx)])] = "CONTENT ERROR"

                        logger.error( 'ERROR_CONTENT_postNo_ => {}'.format(str(pidx)) )

                    # doc 출력 (UnicodeError - 커맨드 창에서 실행 시 발생)
                    print('text data', list(doc))
                    tot_wordCnt = 0
                    for i in doc:

                        str_doc = str(i) + ": " + str(doc[i])
                        try:
                            print(str_doc)
                            wordCnt = len(str_doc.split(" "))

                            tot_wordCnt += wordCnt

                        except UnicodeError:
                            print(str_doc.encode("utf-8"))
                            wordCnt = 0

                        #file.write(str_doc + "\n")


                        # 파일 쓰기
                        if ("ERROR" in str(doc[i])):
                            insert_error(doc[i], doc, error_list)

                    ResultNBDict['게시글내단어수'] += tot_wordCnt

                    # 전체 수 증가
                    total_num += 1

                    continue
                print('END')
            except Exception as e:
                print('게시글이 존재하지 않습니다. ')
                break

        # 결과 출력 (전체 글 수, 에러 수)
        print("=" * 50)
        #file.write("=" * 50 + "\n")

        print("Total : " + str(total_num))
        logger.debug('DEBUG_TOTAL_POST_COUNT => {}'.format(str(total_num)))


        #DB insert
        try:
            # Server Connection to MySQL
            databaseConnection = mysqlConnection.DatabaseConnection_origin()
            databaseConnection.update_naverblogRecord(
                str(ResultNBDict['사용자ID'].replace(" ", "")),
                str(ResultNBDict['게시글수']),
                str(ResultNBDict['금일방문자수']),
                str(ResultNBDict['전체방문자수']),
                str(ResultNBDict['게시글내단어수']),
                str(ResultNBDict['nb_TSCORE']),
                str(ResultNBDict['nb_CSCORE']),
                str(ResultNBDict['nb_MSCORE']),
                userCellPhNum
            )

            returnedValue_naverBlog = True
            ResultNBDict['trueOrFalse'] = True

        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))



        #ERROR detection
        error_count = len(error_list)
        print("Error : " + str(error_count))

        logger.error('ERROR_COUNT => {}'.format(str(error_count)))

        # 에러가 있을 경우 출력
        if (error_count != 0):
            print("Error Post : ")
            for i in error_list:
                print(i)
                logger.error('ERROR_POST_LIST => {}'.format(i) )

        #returnedValue_naverBlog = True

        #list(doc) --> [ "page", "post_number", "title", "date", "content" ]

        #DB Connection=======================================
        end_time = time.time() - start_time_all
        print('데이터 기반 크롤링 총 구동 시간 :', end_time)

        ResultNBDict['trueOrFalse'] = True


        return ResultNBDict

        # 파일 닫기
        #file.close()