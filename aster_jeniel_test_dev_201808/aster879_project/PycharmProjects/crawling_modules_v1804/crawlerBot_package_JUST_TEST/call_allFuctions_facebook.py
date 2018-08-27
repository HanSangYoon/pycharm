#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.handlers
import math
import time

import self

from multiprocessing import Process

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


def start_crawling_facebook(userName, userCellPhoneNumber, facebook_USERURL,reqClient, fromDate, toDate):
    completeOrNot = False

    facebookResult = {}

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

                fb_TSCORE = ResultDict1['tcmScore']['fb_TSCORE']
                fb_CSCORE = ResultDict1['tcmScore']['fb_CSCORE']
                fb_MSCORE = ResultDict1['tcmScore']['fb_MSCORE']

                completeOrNot = True

                facebookResult['fb_TSCORE'] = fb_TSCORE
                facebookResult['fb_CSCORE'] = fb_CSCORE
                facebookResult['fb_MSCORE'] = fb_MSCORE
                facebookResult['completeOrNot'] = completeOrNot


                print('facebook : ', facebookResult)

                return facebookResult

            else:
                print('페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                fb_TSCORE = 0
                fb_CSCORE = 0
                fb_MSCORE = 0

                facebookResult['fb_TSCORE'] = fb_TSCORE
                facebookResult['fb_CSCORE'] = fb_CSCORE
                facebookResult['fb_MSCORE'] = fb_MSCORE
                facebookResult['completeOrNot'] = completeOrNot

                print('facebook : ', fb_TSCORE, fb_CSCORE, fb_MSCORE)

                return facebookResult

        except Exception as ex_facebook:
            print('페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook)
            print()

            try:
                ResultDict2 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName, userCellPhNum, reqClient)

                if ResultDict2['trueOrFalse'] == True:
                    print('2차 페이스북 크롤링 성공, Score : ', ResultDict2['tcmScore'])

                    fb_TSCORE = ResultDict2['tcmScore']['fb_TSCORE']
                    fb_CSCORE = ResultDict2['tcmScore']['fb_CSCORE']
                    fb_MSCORE = ResultDict2['tcmScore']['fb_MSCORE']

                    completeOrNot = True

                    facebookResult['fb_TSCORE'] = fb_TSCORE
                    facebookResult['fb_CSCORE'] = fb_CSCORE
                    facebookResult['fb_MSCORE'] = fb_MSCORE
                    facebookResult['completeOrNot'] = completeOrNot

                    print('facebook : ', fb_TSCORE, fb_CSCORE, fb_MSCORE)

                    return facebookResult

                else:
                    print('2차 페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                    fb_TSCORE = 0
                    fb_CSCORE = 0
                    fb_MSCORE = 0

                    facebookResult['fb_TSCORE'] = fb_TSCORE
                    facebookResult['fb_CSCORE'] = fb_CSCORE
                    facebookResult['fb_MSCORE'] = fb_MSCORE
                    facebookResult['completeOrNot'] = completeOrNot

                    print('facebook : ', fb_TSCORE, fb_CSCORE, fb_MSCORE)

                    return facebookResult

            except Exception as ex_facebook2:
                print('2차 페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook2)

                fb_TSCORE = 0
                fb_CSCORE = 0
                fb_MSCORE = 0

                facebookResult['fb_TSCORE'] = fb_TSCORE
                facebookResult['fb_CSCORE'] = fb_CSCORE
                facebookResult['fb_MSCORE'] = fb_MSCORE
                facebookResult['completeOrNot'] = completeOrNot

                print('facebook : ', fb_TSCORE, fb_CSCORE, fb_MSCORE)

                return facebookResult
    else:

        print('페이스북 계정 정보가 존재하지 않습니다.')
        facebook_USERURL = None

        fb_TSCORE = 0
        fb_CSCORE = 0
        fb_MSCORE = 0

        facebookResult['fb_TSCORE'] = fb_TSCORE
        facebookResult['fb_CSCORE'] = fb_CSCORE
        facebookResult['fb_MSCORE'] = fb_MSCORE
        facebookResult['completeOrNot'] = completeOrNot

        print('facebook : ', fb_TSCORE, fb_CSCORE, fb_MSCORE)

        return facebookResult

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

print('facebook 분석 종료')
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

        '''
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
            print('사용자의 네이버블로그 계정 정보가 없습니다.')
            naverblogURL = None

        '''

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

            returnVal_facebook = start_crawling_facebook(userRealName, userCellPhNum, facebookURL, reqClient, startDate, endDate)


            roll = roll + 1

            #, returnVal_kakaostory, returnVal_naverblog
            print('페이스북 결과', returnVal_facebook)

            '''
            if returnVal_facebook[3] == True and returnVal_kakaostory[3]==True and returnVal_naverblog[3]==True:

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)


            elif returnVal_facebook[3] == True and returnVal_kakaostory[3] == True and returnVal_naverblog[3] == False:

                returnVal_naverblog[0] = 0
                returnVal_naverblog[1] = 0
                returnVal_naverblog[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)


            elif returnVal_facebook[3] == True and returnVal_kakaostory[3] == False and returnVal_naverblog[3] == True:

                returnVal_kakaostory[0] = 0
                returnVal_kakaostory[1] = 0
                returnVal_kakaostory[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            elif returnVal_facebook[3] == False and returnVal_kakaostory[3] == True and returnVal_naverblog[3] == True:

                returnVal_facebook[0] = 0
                returnVal_facebook[1] = 0
                returnVal_facebook[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            elif returnVal_facebook[3] == True and returnVal_kakaostory[3] == False and returnVal_naverblog[3] == False:

                returnVal_naverblog[0] = 0
                returnVal_naverblog[1] = 0
                returnVal_naverblog[2] = 0

                returnVal_kakaostory[0] = 0
                returnVal_kakaostory[1] = 0
                returnVal_kakaostory[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            elif returnVal_facebook[3] == False and returnVal_kakaostory[3] ==True  and returnVal_naverblog[3] == False:

                returnVal_facebook[0] = 0
                returnVal_facebook[1] = 0
                returnVal_facebook[2] = 0

                returnVal_naverblog[0] = 0
                returnVal_naverblog[1] = 0
                returnVal_naverblog[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            elif returnVal_facebook[3] == False and returnVal_kakaostory[3] ==False  and returnVal_naverblog[3] == True:

                returnVal_facebook[0] = 0
                returnVal_facebook[1] = 0
                returnVal_facebook[2] = 0

                returnVal_kakaostory[0] = 0
                returnVal_kakaostory[1] = 0
                returnVal_kakaostory[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            elif returnVal_facebook[3] == False and returnVal_kakaostory[3] == False and returnVal_naverblog[3] == False:

                returnVal_facebook[0] = 0
                returnVal_facebook[1] = 0
                returnVal_facebook[2] = 0

                returnVal_kakaostory[0] = 0
                returnVal_kakaostory[1] = 0
                returnVal_kakaostory[2] = 0

                returnVal_naverblog[0] = 0
                returnVal_naverblog[1] = 0
                returnVal_naverblog[2] = 0

                totalT = returnVal_facebook[0] + returnVal_kakaostory[0] + returnVal_naverblog[0]
                totalC = returnVal_facebook[1] + returnVal_kakaostory[1] + returnVal_naverblog[1]
                totalM = returnVal_facebook[2] + returnVal_kakaostory[2] + returnVal_naverblog[2]

                get_TotalScore(totalT, totalC, totalM, startDate, endDate, userRealName)

            '''

            #print('결과', returnVal_facebook, returnVal_kakaostory, returnVal_naverblog)
            #logger.debug('결과 : fb={}, kk={}, nb={}'.format(returnVal_facebook, returnVal_kakaostory, returnVal_naverblog) )

    else:
        print('크롤링이 완료되었습니다. ')

