#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

# from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import facebookCrawlerBot_new as snsScrapBot
# from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType.worknet_just import facebookCrawlerBot_jeniel_GODOHWA as snsScrapBot
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    facebookCrawlerBot_jeniel as snsScrapBot


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'origin, x-requested-with, content-type, accept')
        self.send_header('Pragma', 'No-Cache')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Expires', 'Sun, 01 Jan 2014 00:00:00 GMT')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Cache-Control', 'post-check=0, pre-check=0, FALSE')
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()


    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.parsed_POST_data(post_data)

    def parsed_POST_data(self, post_data):
        #getParam = urllib.parse.unquote(post_data.decode('utf-8'))
        getParam = urllib.parse.unquote(post_data.decode())

        print('입력한 데이터: ', getParam)
        #http://172.30.1.33:8000/kakao_story=https%3A%2F%2Fstory.kakao.com%2F_9W0DZ3&naver_blog=https%3A%2F%2Fblog.naver.com%2Ftramper2&facebook=https%3A%2F%2Fwww.facebook.com%2Fdanny.woo.33&instagram=XXXX&username=%EA%B9%80%ED%83%9C%ED%98%B8
        # kakao_story=https%3A%2F%2Fstory.kakao.com%2F_9W0DZ3&
        # naver_blog=https%3A%2F%2Fblog.naver.com%2Ftramper2&
        # facebook=https%3A%2F%2Fwww.facebook.com%2Fdanny.woo.33&
        # instagram=&
        # username=%EA%B9%80%ED%83%9C%ED%98%B8

        userData = {}

        if getParam is not None:
            snsURL_ADDR_fromWeb = getParam.split('&')
            #print(snsURL_ADDR_fromWeb[0], snsURL_ADDR_fromWeb[1], snsURL_ADDR_fromWeb[2], snsURL_ADDR_fromWeb[3], snsURL_ADDR_fromWeb[4])
            #kakao_story=XXXX&naver_blog=XXXX&facebook=XXXX&instagram=XXXX&username=XXXX
            print('&로 나눠진 데이터 리스트:', snsURL_ADDR_fromWeb)

            if snsURL_ADDR_fromWeb[0]:
                kakaoStory_USERURL_tot= snsURL_ADDR_fromWeb[0].split("=")[1].replace(" ", "")
                try:
                    print('kakaoStory SNS 주소가 존재합니다.')
                    kakaoStory_USERURL_pre = kakaoStory_USERURL_tot.split('//')[1]
                    kakaoStory_USERURL = kakaoStory_USERURL_pre.split('/')[1]
                    userData['kakao_story'] = kakaoStory_USERURL
                except Exception as e:
                    print('kakaoStory SNS 주소가 존재하지 않습니다.', e)
                    kakaoStory_USERURL = None
            else:
                print('kakaoStory SNS 주소가 존재하지 않습니다.')
                kakaoStory_USERURL = None

            '''
            if snsURL_ADDR_fromWeb[1]:
                naverBlog_USERURL_tot= snsURL_ADDR_fromWeb[1].split("=")[1].replace(" ", "")

                try:
                    print('naverBlog SNS 주소가 존재합니다.')
                    naverBlog_USERURL_pre = naverBlog_USERURL_tot.split('//')[1]
                    naverBlog_USERURL = naverBlog_USERURL_pre.split('/')[1]
                    userData['naver_blog'] = naverBlog_USERURL
                except Exception as e:
                    print('naverBlog SNS 주소가 존재하지 않습니다.', e)
                    naverBlog_USERURL = None
            else:
                print('naverBlog SNS 주소가 존재하지 않습니다.')
                naverBlog_USERURL = None
            '''
            naverBlog_USERURL = None

            if snsURL_ADDR_fromWeb[2]:

                #type 01 : facebook=https://www.facebook.com/danny.woo.33
                #type 02 : facebook=https://www.facebook.com/profile.php?id=100008174415045

                if 'profile' in snsURL_ADDR_fromWeb[2]:
                    print('문자형식의 페이지ID 값을 갖지 않은 사용자 입니다.')

                    facebook_USERURL_tot = snsURL_ADDR_fromWeb[2].split("=")[2].replace(" ", "")
                    facebook_USERURL = facebook_USERURL_tot

                    print('1', facebook_USERURL_tot)
                    print('2', facebook_USERURL)

                    userData['facebook'] = facebook_USERURL


                else:
                    facebook_USERURL_tot = snsURL_ADDR_fromWeb[2].split("=")[1].replace(" ", "")

                    try:
                        print('facebook SNS 주소가 존재합니다.')
                        facebook_USERURL_pre = facebook_USERURL_tot.split('//')[1]
                        facebook_USERURL = facebook_USERURL_pre.split('/')[1]
                        userData['facebook'] = facebook_USERURL
                    except Exception as e:
                        print('facebook SNS 주소가 존재하지 않습니다.', e)
                        facebook_USERURL = None

            else:
                print('facebook SNS 주소가 존재하지 않습니다.')
                facebook_USERURL = None


            if snsURL_ADDR_fromWeb[3]:
                instagram_USERURL_tot= snsURL_ADDR_fromWeb[3].split("=")[1].replace(" ", "")

                try:
                    instagram_USERURL_pre = instagram_USERURL_tot.split('//')[1]
                    instagram_USERURL = instagram_USERURL_pre.split('/')[1]
                    print('instagram SNS 주소가 존재합니다.')
                    userData['instagram_USERURL'] = instagram_USERURL
                except Exception as e:
                    print('instagram SNS 주소가 존재하지 않습니다.', e)
                    instagram_USERURL = None
            else:
                print('instagram SNS 주소가 존재하지 않습니다.')
                instagram_USERURL = None

            if snsURL_ADDR_fromWeb[4]:
                print('사용자 이름이 존재합니다.', snsURL_ADDR_fromWeb[4])
                try:
                    userName = snsURL_ADDR_fromWeb[4].split("=")[1].replace(" ", "")
                    userData['username'] = userName
                except Exception as e:
                    print('사용자 이름이 존재하지 않습니다.', e)
                    userName = None
            else:
                print('사용자 이름이 존재하지 않습니다.')
                userName = None


            #print('전달 받은 계정정보 값 :', kakaoStory_USERURL, naverBlog_USERURL, facebook_USERURL, instagram_USERURL, userName)
            print('전달 받은 계정정보 값 :', kakaoStory_USERURL, facebook_USERURL, instagram_USERURL, userName)
            print('user Data : ', userData)

            tot_TSCORE = 0
            tot_CSCORE = 0
            tot_MSCORE = 0
            userSNSRank = ''

            #FACEBOOK
            if facebook_USERURL is not None:
                try:
                    #CrawlingByFacebookCrawlBot
                    ResultDict1 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName, 'jeniel')

                    if ResultDict1['trueOrFalse'] == True:
                        print('페이스북 크롤링 성공, Score : ', ResultDict1['tcmScore']['T_SCORE'], ResultDict1['tcmScore']['C_SCORE'], ResultDict1['tcmScore']['M_SCORE'])

                        tot_TSCORE += ResultDict1['tcmScore']['T_SCORE']
                        tot_CSCORE += ResultDict1['tcmScore']['C_SCORE']
                        tot_MSCORE += ResultDict1['tcmScore']['M_SCORE']

                        print('facebook : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

                        jsonData = {'TSCORE': ResultDict1['tcmScore']['T_SCORE'], 'CSCORE':ResultDict1['tcmScore']['C_SCORE'], 'MSCORE':ResultDict1['tcmScore']['M_SCORE'], 'DETAILINFO':ResultDict1['tcmScore']['DETAIL'] }
                        data = json.dumps(jsonData).encode("utf-8")
                        data1 = json.dumps(jsonData).encode("utf-16")
                        print('data 값:', data)
                        self.wfile.write(data)
                        print('data  전달 끝')

                        return
                    else:
                        print('페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                except Exception as ex_facebook:
                    print('페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook)

                    try:
                        ResultDict2 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName, 'jeniel')
                        if ResultDict2 == True:
                            print('2차 페이스북 크롤링 성공, Score : ', ResultDict2['tcmScore'])
                            tot_TSCORE += ResultDict2['tcmScore']['T_SCORE']
                            tot_CSCORE += ResultDict2['tcmScore']['C_SCORE']
                            tot_MSCORE += ResultDict2['tcmScore']['M_SCORE']

                            data = json.dumps(ResultDict2['tcmScore'])
                            print('data 값:', data)
                            self.wfile.write(data).encode()
                            print('data  전달 끝')

                            return
                        else:
                            print('2차 페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')
                    except Exception as ex_facebook2:
                        print('2차 페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook2)


            '''
            #KAKAOSTORY
            if kakaoStory_USERURL and facebook_USERURL is not None:
                if kakaoStory_USERURL:
                    returnValue_kakaostory = kakaostoryScrapBot.crawling_singleData_KakaoStoryCrawlerBot(
                        kakaoStory_USERURL, userName, facebook_USERURL)

                    print('returnValue_kakaostory : ', returnValue_kakaostory)

                    if returnValue_kakaostory[0] == True:
                        print('카카오스토리 크롤링 성공')

                        tot_TSCORE += int(returnValue_kakaostory[1]['kk_TSCORE'])
                        tot_CSCORE += int(returnValue_kakaostory[1]['kk_CSCORE'])
                        tot_MSCORE += int(returnValue_kakaostory[1]['kk_MSCORE'])

                        print('kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

                    else:
                        print('카카오스토리 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

                elif kakaoStory_USERURL is not None:
                    facebook_USERURL = ''
                    if kakaoStory_USERURL:
                        returnValue_kakaostory = kakaostoryScrapBot.crawling_singleData_KakaoStoryCrawlerBot(
                            kakaoStory_USERURL, userName, facebook_USERURL)
                        print('returnValue_kakaostory : ', returnValue_kakaostory)

                        if returnValue_kakaostory == True:
                            print('카카오스토리 크롤링 성공')

                            tot_TSCORE += returnValue_kakaostory[1]['kk_TSCORE']
                            tot_CSCORE += returnValue_kakaostory[1]['kk_CSCORE']
                            tot_MSCORE += returnValue_kakaostory[1]['kk_MSCORE']

                            print('kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

                        else:
                            print('카카오스토리 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')
                else:
                    # kakaoStory_USERURL is None:
                    returnValue_kakaostory = kakaostoryScrapBot.crawling_CSVdata_KakaoStoryCrawlerBot(facebook_USERURL)
                    print('returnValue_kakaostory : ', returnValue_kakaostory)
                    if returnValue_kakaostory[0] == True:
                        print('카카오스토리 크롤링 성공')

                        tot_TSCORE += returnValue_kakaostory[1]['kk_TSCORE']
                        tot_CSCORE += returnValue_kakaostory[1]['kk_CSCORE']
                        tot_MSCORE += returnValue_kakaostory[1]['kk_MSCORE']

                        print('kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)
                    else:
                        print('카카오스토리 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

            else:
                returnValue_kakaostory = kakaostoryScrapBot.crawling_CSVdata_KakaoStoryCrawlerBot()
                print('returnValue_kakaostory : ', returnValue_kakaostory[0])
                print('currDate : ', returnValue_kakaostory[1])

                if returnValue_kakaostory[0] == True:
                    print('카카오스토리 크롤링 성공')

                    tot_TSCORE += returnValue_kakaostory[1]['kk_TSCORE']
                    tot_CSCORE += returnValue_kakaostory[1]['kk_CSCORE']
                    tot_MSCORE += returnValue_kakaostory[1]['kk_MSCORE']

                    print('kakao: ', tot_TSCORE, tot_CSCORE, tot_MSCORE)
                else:
                    print('카카오스토리 크롤링 봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

            #INSTAGRAM
            if instagram_USERURL is not None:
                print('인스타그램 크롤링')
                returnValue_instagram = instagramScrapBot.CrawlingByInstagramCrawlBot(instagram_USERURL, userName, facebook_USERURL)

                if returnValue_instagram[0] == True:
                    print('인스타그램 크롤링 성공')
                    tot_TSCORE += returnValue_instagram[1]['insta_TSCORE']
                    tot_CSCORE += returnValue_instagram[1]['insta_CSCORE']
                    tot_MSCORE += returnValue_instagram[1]['insta_MSCORE']

                    print('instagram : ', tot_TSCORE, tot_CSCORE, tot_MSCORE)

                else:
                    print('인스타그램 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')
            else:
                print('인스타그램 크롤링을 위한 계정정보가 존재하지 않습니다.')
                # 사용자 등급 : userSnsRank

            if (tot_TSCORE <= 600 and tot_TSCORE > 500) and (tot_CSCORE <= 1000 and tot_CSCORE > 850) and (
                    tot_MSCORE <= 400 and tot_MSCORE > 350):
                userSNSRank = 'A+'
            elif (tot_TSCORE <= 500 and tot_TSCORE > 400) and (tot_CSCORE <= 850 and tot_CSCORE > 700) and (
                    tot_MSCORE <= 350 and tot_MSCORE > 300):
                userSNSRank = 'A-'
            elif (tot_TSCORE <= 400 and tot_TSCORE > 350) and (tot_CSCORE <= 700 and tot_CSCORE > 550) and (
                    tot_MSCORE <= 300 and tot_MSCORE > 250):
                userSNSRank = 'B+'
            elif (tot_TSCORE <= 350 and tot_TSCORE > 300) and (tot_CSCORE <= 550 and tot_CSCORE > 400) and (
                    tot_MSCORE <= 250 and tot_MSCORE > 200):
                userSNSRank = 'B-'
            elif (tot_TSCORE <= 300 and tot_TSCORE > 250) and (tot_CSCORE <= 400 and tot_CSCORE > 300) and (
                    tot_MSCORE <= 200 and tot_MSCORE > 150):
                userSNSRank = 'C+'
            elif (tot_TSCORE <= 250 and tot_TSCORE > 200) and (tot_CSCORE <= 300 and tot_CSCORE > 200) and (
                    tot_MSCORE <= 150 and tot_MSCORE > 100):
                userSNSRank = 'C-'
            elif (tot_TSCORE <= 200 and tot_TSCORE > 100) and (tot_CSCORE <= 200 and tot_CSCORE > 100) and (
                    tot_MSCORE <= 100 and tot_MSCORE > 50):
                userSNSRank = 'D+'
            elif (tot_TSCORE <= 100 and tot_TSCORE > 0) and (tot_CSCORE <= 100 and tot_CSCORE > 0) and (
                    tot_MSCORE <= 50 and tot_MSCORE > 1):
                userSNSRank = 'D-'

                print('userSNS_Rank :', userSNSRank)

            # DB insert
            try:
                # Server Connection to MySQL
                databaseConnection = mysqlConnection.DatabaseConnection_origin()
                databaseConnection.update_totalTCM_Record(
                    str(tot_TSCORE),
                    str(tot_CSCORE),
                    str(tot_MSCORE),
                    userSNSRank,
                    facebook_USERURL
                )
            except Exception as e_maria:
                print('[ Error ] MariaDB About information Insertion :', e_maria)
            '''
        else:
            print("전달받은 데이터가 없습니다. ")

#httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

#jeniel
httpd = HTTPServer(('172.30.1.20', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()