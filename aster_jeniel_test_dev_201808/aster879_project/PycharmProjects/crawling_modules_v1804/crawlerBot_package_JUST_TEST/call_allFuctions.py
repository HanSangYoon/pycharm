#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.handlers
import math
import time

import self

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    facebookCrawlerBot as snsScrapBot
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    kakaostoryCrawlerBot as kakaostoryScrapBot
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    naverBlogCrawlerBot as naverblogScrapBot

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection

'''
#facebook
# 외부에서 데이터를 받아야 함. 아래 설정은 임의 설정임
#facebook_USERURL = 'hyoungwoo.kim.zermatt'
facebook_USERURL = 'kpokem'
userName = '김동근'
#instagram
#instagram_USERURL = 'therock'
instagram_USERURL = 'dasolmom_'
#kakaostory
kakaoStory_USERURL = 'happyleader'
#naverBlog
naverBlog_USERURL = 'pamicusq'
'''

reqClient = 'sci'

# 현재시각 추출
currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

# logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger('start_point_log')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

# fileHandler와 StreamHandler를 생성
file_max_bytes = 10 * 1024 * 1024  # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler(
    'C://python_project/aster879_project/PycharmProjects/log/aster_sci_crawlerbot_logging_' + currTime,
    maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

# Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

# logging
logging.debug('start_point_log_crawler_module_debugging on' + currTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')

global userCellPhoneNumber
global kakaoStory_USERURL
global facebook_USERURL

global tot_TSCORE
global tot_CSCORE
global tot_MSCORE
global userSNSRank

global userSNS_T_Rank
global userSNS_T_Rank_score

global userSNS_C_Rank
global userSNS_C_Rank_score

global userSNS_M_Rank
global userSNS_M_Rank_score

global avg_RankgScore


def start_crawling(userName, userCellPhoneNumber, kakaoStory_USERURL, naverblog_USERURL, facebook_USERURL, reqClient,
                   fromDate, toDate):
    tot_TSCORE = 50
    tot_CSCORE = 50
    tot_MSCORE = 50
    userSNSRank = 'D-'

    userSNS_T_Rank_score = 1
    userSNS_C_Rank_score = 1
    userSNS_M_Rank_score = 1

    # FACEBOOK
    if facebook_USERURL is not None:
        try:

            print('facebook_USERURL :', facebook_USERURL)
            # CrawlingByFacebookCrawlBot

            ResultDict1 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName, userCellPhNum, reqClient)
            # ResultDict1 = snsScrapBot.CrawlingByFacebookCrawlBot(self, 1, facebook_USERURL, userName)

            if ResultDict1['trueOrFalse'] == True:
                print('페이스북 크롤링 성공, Score : ', ResultDict1['tcmScore']['fb_TSCORE'],
                      ResultDict1['tcmScore']['fb_CSCORE'], ResultDict1['tcmScore']['fb_MSCORE'])

                tot_TSCORE += ResultDict1['tcmScore']['fb_TSCORE']
                tot_CSCORE += ResultDict1['tcmScore']['fb_CSCORE']
                tot_MSCORE += ResultDict1['tcmScore']['fb_MSCORE']

                print('facebook : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

            else:
                print('페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                tot_TSCORE += 0
                tot_CSCORE += 0
                tot_MSCORE += 0

                print('facebook: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

        except Exception as ex_facebook:
            print('페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook)
            print()

            try:
                ResultDict2 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName, userCellPhNum, reqClient)

                if ResultDict2['trueOrFalse'] == True:
                    print('2차 페이스북 크롤링 성공, Score : ', ResultDict2['tcmScore'])

                    tot_TSCORE += ResultDict2['tcmScore']['fb_TSCORE']
                    tot_CSCORE += ResultDict2['tcmScore']['fb_CSCORE']
                    tot_MSCORE += ResultDict2['tcmScore']['fb_MSCORE']

                    print('facebook: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

                else:
                    print('2차 페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                    tot_TSCORE += 0
                    tot_CSCORE += 0
                    tot_MSCORE += 0

                    print('facebook: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

            except Exception as ex_facebook2:
                print('2차 페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook2)

                tot_TSCORE += 0
                tot_CSCORE += 0
                tot_MSCORE += 0

                print('facebook: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)
    else:
        facebook_USERURL = None

    # KAKAOSTORY
    if kakaoStory_USERURL is not None:

        print('kakaoStory_USERURL :', kakaoStory_USERURL)

        try:
            returnValue_kakaostory = kakaostoryScrapBot.crawling_singleData_KakaoStoryCrawlerBot(kakaoStory_USERURL,
                                                                                                 userName,
                                                                                                 userCellPhNum)
            print('returnValue_kakaostory : ', returnValue_kakaostory)

            if returnValue_kakaostory['trueOrFalse'] == True:
                print('카카오스토리 크롤링 성공')

                tot_TSCORE += returnValue_kakaostory['kk_TSCORE']
                tot_CSCORE += returnValue_kakaostory['kk_CSCORE']
                tot_MSCORE += returnValue_kakaostory['kk_MSCORE']

                print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

            else:
                print('카카오스토리 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                tot_TSCORE += 0
                tot_CSCORE += 0
                tot_MSCORE += 0

                print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

        except BaseException as e:
            print('카카오 스토리 크롤링이 페이지 구조 변경등의 외부요인으로 종료되었습니다.', e)

            tot_TSCORE += 0
            tot_CSCORE += 0
            tot_MSCORE += 0

            print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

    else:
        print('카카오스토리 주소가 존재하지 않습니다.')

        tot_TSCORE += 0
        tot_CSCORE += 0
        tot_MSCORE += 0

        print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

    '''                
    else:
        #kakaoStory_USERURL is None:

        #특정 경로에 CSV 파일이 존재하는지 분기
        if

        returnValue_kakaostory = kakaostoryScrapBot.crawling_CSVdata_KakaoStoryCrawlerBot(userCellPhNum)
        print('returnValue_kakaostory : ', returnValue_kakaostory)
        if returnValue_kakaostory['trueOrFalse'] == True:
            print('카카오스토리 크롤링 성공')

            tot_TSCORE += returnValue_kakaostory['kk_TSCORE']
            tot_CSCORE += returnValue_kakaostory['kk_CSCORE']
            tot_MSCORE += returnValue_kakaostory['kk_MSCORE']

            print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)
        else:
            print('카카오스토리 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

            tot_TSCORE += 0
            tot_CSCORE += 0
            tot_MSCORE += 0

            print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)
    '''

    # NAVERBLOG
    if naverblog_USERURL is not None:

        print('naverblog_USERURL :', naverblog_USERURL)

        try:
            returnValue_naverblog = naverblogScrapBot.CrawlingByNaverBlogCrawlBot(naverblog_USERURL, userName,
                                                                                  userCellPhNum)

            if returnValue_naverblog['trueOrFalse'] == True:
                print('네이버블로그 크롤링 성공')

                tot_TSCORE += returnValue_naverblog['nb_TSCORE']
                tot_CSCORE += returnValue_naverblog['nb_CSCORE']
                tot_MSCORE += returnValue_naverblog['nb_MSCORE']

                print('facebook + kakaostory + naverblog : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

            else:
                print('네이버블로그 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                tot_TSCORE += 0
                tot_CSCORE += 0
                tot_MSCORE += 0

                print('facebook + kakaostory + naverblog : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

        except Exception as e:
            print('네이버블로그 크롤링이 페이지 구조 변경등의 외부요인으로 종료되었습니다.', e)

            tot_TSCORE += 0
            tot_CSCORE += 0
            tot_MSCORE += 0

            print('facebook + kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

    else:
        print('네이버블로그 주소가 존재하지 않습니다.')

        tot_TSCORE += 0
        tot_CSCORE += 0
        tot_MSCORE += 0

        print('facebook + kakaostory + naverblog : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

    '''       
    #instagram
    if instagram_USERURL is not None:

        print('인스타그램 크롤링')
        returnValue_instagram = instagramScrapBot.CrawlingByInstagramCrawlBot(instagram_USERURL, userName, userCellPhNum)

        if returnValue_instagram['trueOrFalse'] == True:
            print('인스타그램 크롤링 성공')

            tot_TSCORE += returnValue_instagram['insta_TSCORE']
            tot_CSCORE += returnValue_instagram['insta_CSCORE']
            tot_MSCORE += returnValue_instagram['insta_MSCORE']

            print('facebook + kakaostory + instagram : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

        else:
            print('인스타그램 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')
    else:
        print('인스타그램 크롤링을 위한 계정정보가 존재하지 않습니다.')
    '''

    # 사용자 등급 : userSnsRank
    userSNS_T_Rank = ''
    if (tot_TSCORE <= 600 and tot_TSCORE > 500):
        userSNS_T_Rank = 'T_A+'
        userSNS_T_Rank_score = 8
    elif (tot_TSCORE <= 500 and tot_TSCORE > 400):
        userSNS_T_Rank = 'T_A-'
        userSNS_T_Rank_score = 7
    elif (tot_TSCORE <= 400 and tot_TSCORE > 350):
        userSNS_T_Rank = 'T_B+'
        userSNS_T_Rank_score = 6
    elif (tot_TSCORE <= 350 and tot_TSCORE > 300):
        userSNS_T_Rank = 'T_B-'
        userSNS_T_Rank_score = 5
    elif (tot_TSCORE <= 300 and tot_TSCORE > 250):
        userSNS_T_Rank = 'T_C+'
        userSNS_T_Rank_score = 4
    elif (tot_TSCORE <= 250 and tot_TSCORE > 200):
        userSNS_T_Rank = 'T_C-'
        userSNS_T_Rank_score = 3
    elif (tot_TSCORE <= 200 and tot_TSCORE > 100):
        userSNS_T_Rank = 'T_D+'
        userSNS_T_Rank_score = 2
    elif (tot_TSCORE <= 100 and tot_TSCORE > 1):
        userSNS_T_Rank = 'T_D-'
        userSNS_T_Rank_score = 1

    print('사용자의 T 등급 :', userSNS_T_Rank)

    userSNS_C_Rank = ''
    if (tot_CSCORE <= 1000 and tot_CSCORE > 850):
        userSNS_C_Rank = 'C_A+'
        userSNS_C_Rank_score = 8
    elif (tot_CSCORE <= 850 and tot_CSCORE > 700):
        userSNS_C_Rank = 'C_A-'
        userSNS_C_Rank_score = 7
    elif (tot_CSCORE <= 700 and tot_CSCORE > 550):
        userSNS_C_Rank = 'C_B+'
        userSNS_C_Rank_score = 6
    elif (tot_CSCORE <= 550 and tot_CSCORE > 400):
        userSNS_C_Rank = 'C_B-'
        userSNS_C_Rank_score = 5
    elif (tot_CSCORE <= 400 and tot_CSCORE > 300):
        userSNS_C_Rank = 'C_C+'
        userSNS_C_Rank_score = 4
    elif (tot_CSCORE <= 300 and tot_CSCORE > 200):
        userSNS_C_Rank = 'C_C-'
        userSNS_C_Rank_score = 3
    elif (tot_CSCORE <= 200 and tot_CSCORE > 100):
        userSNS_C_Rank = 'C_D+'
        userSNS_C_Rank_score = 2
    elif (tot_CSCORE <= 100 and tot_CSCORE > 1):
        userSNS_C_Rank = 'C_D-'
        userSNS_C_Rank_score = 1

    print('사용자의 C 등급 :', userSNS_C_Rank)

    userSNS_M_Rank = ''
    if (tot_MSCORE <= 400 and tot_MSCORE > 350):
        userSNS_M_Rank = 'M_A+'
        userSNS_M_Rank_score = 8
    elif (tot_MSCORE <= 350 and tot_MSCORE > 300):
        userSNS_M_Rank = 'M_A-'
        userSNS_M_Rank_score = 7
    elif (tot_MSCORE <= 300 and tot_MSCORE > 250):
        userSNS_M_Rank = 'M_B+'
        userSNS_M_Rank_score = 6
    elif (tot_MSCORE <= 250 and tot_MSCORE > 200):
        userSNS_M_Rank = 'M_B-'
        userSNS_M_Rank_score = 5
    elif (tot_MSCORE <= 200 and tot_MSCORE > 150):
        userSNS_M_Rank = 'M_C+'
        userSNS_M_Rank_score = 4
    elif (tot_MSCORE <= 150 and tot_MSCORE > 100):
        userSNS_M_Rank = 'M_C-'
        userSNS_M_Rank_score = 3
    elif (tot_MSCORE <= 100 and tot_MSCORE > 50):
        userSNS_M_Rank = 'M_D+'
        userSNS_M_Rank_score = 2
    elif (tot_MSCORE <= 50 and tot_MSCORE > 1):
        userSNS_M_Rank = 'M_D-'
        userSNS_M_Rank_score = 1

    print('사용자의 M 등급 :', userSNS_M_Rank)

    avg_RankgScore = math.ceil((userSNS_T_Rank_score + userSNS_C_Rank_score + userSNS_M_Rank_score) / 3)

    print('사용자의 평균 SCORE : ', avg_RankgScore)

    if avg_RankgScore <= 8 and avg_RankgScore > 7:
        userSNSRank = 'A+'
    elif avg_RankgScore <= 7 and avg_RankgScore > 6:
        userSNSRank = 'A-'
    elif avg_RankgScore <= 6 and avg_RankgScore > 5:
        userSNSRank = 'B+'
    elif avg_RankgScore <= 5 and avg_RankgScore > 4:
        userSNSRank = 'B-'
    elif avg_RankgScore <= 4 and avg_RankgScore > 3:
        userSNSRank = 'C+'
    elif avg_RankgScore <= 3 and avg_RankgScore > 2:
        userSNSRank = 'C-'
    elif avg_RankgScore <= 2 and avg_RankgScore > 1:
        userSNSRank = 'D+'
    elif avg_RankgScore <= 1 and avg_RankgScore > 0:
        userSNSRank = 'D-'

    print('userSNS_Rank:', userSNSRank)

    # DB insert
    try:
        # Server Connection to MySQL
        databaseConnection = mysqlConnection.DatabaseConnection_origin()
        databaseConnection.update_totalTCM_Record(
            str(tot_TSCORE),
            str(tot_CSCORE),
            str(tot_MSCORE),
            userSNSRank,
            fromDate,
            toDate,
            userCellPhNum,
            userName
        )
    except Exception as e_maria:
        print('[ Error ] MariaDB About information Insertion :', e_maria)

    print('분석 종료')
    print()
    print()


# 실행 함수 선언
if __name__ == '__main__':
    # start_crawling(userCellPhNum, kakaoStoryURL, naverblogURL, facebookURL, reqClient)

    global roll
    roll = 0

    while roll < 10000:

        databaseConnection = mysqlConnection.DatabaseConnection_origin()
        search_idx_queue = databaseConnection.pre_Insert_sci_record()

        print('search_idx_queue :', search_idx_queue)

        search_idx_tbl = databaseConnection.select_lastIndex_sci_record(str(search_idx_queue[0]).replace(" ", ""))
        print('search log index로 가져온 search_log_index값 :', str(search_idx_tbl[0]).replace(" ", ""), ', ',
              str(search_idx_tbl[1]).replace(" ", ""))

        userRealName = str(search_idx_tbl[1]).replace(" ", "")

        databaseConnection = mysqlConnection.DatabaseConnection_origin()
        # usr_origin_data = databaseConnection.select_sci_record(str(search_idx_queue[0]).replace(" ","") )
        usr_origin_data = databaseConnection.select_sci_record(str(search_idx_tbl[0]).replace(" ", ""))

        print('origin :', usr_origin_data)
        # SELECT search_log_mobile, search_log_kakaostory_url, search_log_naver_blog_url, search_log_facebook_url, search_log_from_date, search_log_to_date
        print(usr_origin_data[0], usr_origin_data[1], usr_origin_data[2], usr_origin_data[3], usr_origin_data[4],
              usr_origin_data[5])

        try:
            # SELECT search_log_mobile, search_log_kakaostory_url, search_log_naver_blog_url, search_log_facebook_url FROM search_log WHERE search_log_index='52';
            userCellPhNum = usr_origin_data[0]
        except Exception as e:
            print('사용자 휴대폰 번호가 없습니다.')

        try:
            # https://story.kakao.com/_5HFOi6
            kakaoStoryURL = usr_origin_data[1].split('com')[1].replace('/', '')
            print('kakaoStoryURL :', kakaoStoryURL)
        except Exception as e:
            print('사용자의 카카오 스토리 계정정보가없습니다.')
            kakaoStoryURL = None

        try:
            # 'https://blog.naver.com/ssuyeon0524/221321171233
            # https://blog.naver.com/gozuall
            naverblogURL = usr_origin_data[2].split('com/')[1].replace(' ', '')
            print('naverblog_USERURL :', naverblogURL)
        except Exception as e:
            print('사용자의 페이스북 계정 정보가 없습니다.')
            naverblogURL = None

        try:
            facebookURL_parse_01 = usr_origin_data[3].split('https://www.facebook.com/')[1]

            if 'profile.php' in facebookURL_parse_01:
                # https://www.facebook.com/profile.php?id=100018030067378 & hc_location=friend_browser
                facebookURL = facebookURL_parse_01.split('&')[0].split('id=')[1]
            else:
                facebookURL = facebookURL_parse_01

            print('facebook_USERURL :', facebookURL)
        except Exception as e:
            print('사용자의 페이스북 계정 정보가 없습니다.')
            facebookURL = None

        try:
            startDate = str(usr_origin_data[4]).replace("-", "")
        except Exception as e:
            print('There is no start DATE')
            startDate = ''

        try:
            endDate = str(usr_origin_data[5]).replace("-", "")
        except Exception as e:
            print('There is no end DATE')
            endDate = ''

        print('startDate :', startDate, ',', 'endDate :', endDate)

        if int(str(search_idx_queue[0]).replace(" ", "")) <= int(str(search_idx_tbl[0]).replace(" ", "")):
            # print('test print: ', str(search_idx_queue[0]).replace(" ", ""), ' vs ', str(search_idx_tbl[0]).replace(" ", ""))

            start_crawling(userRealName, userCellPhNum, kakaoStoryURL, naverblogURL, facebookURL, reqClient, startDate,
                           endDate)
            roll = roll + 1

    else:
        print('크롤링이 완료되었습니다. ')

