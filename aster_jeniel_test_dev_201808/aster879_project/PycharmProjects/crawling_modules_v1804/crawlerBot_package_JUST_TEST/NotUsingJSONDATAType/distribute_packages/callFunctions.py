#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType.facebookCrawlerBot as facebookScrapBot


#facebook
userFacebookURL = 'kpokem'
username = '김동근'

if userFacebookURL is not None:
    loginCnt = 1
    print('페이스북 크롤링')
    returnValue_facebook = facebookScrapBot.login_facebook(loginCnt, userFacebookURL, username)

    if returnValue_facebook == True:
        print(str(loginCnt) +'차 시도 후, 페이스북 크롤링 성공')

    elif returnValue_facebook == False:

        loginCnt +=1
        returnValue_facebook = facebookScrapBot.login_facebook(loginCnt, userFacebookURL, username)

        if returnValue_facebook == True:
            print(str(loginCnt) +'차 시도 후, 페이스북 크롤링 성공')

        elif returnValue_facebook == False:

            loginCnt += 1
            returnValue_facebook = facebookScrapBot.login_facebook(loginCnt, userFacebookURL, username)

            if returnValue_facebook == True:
                print(str(loginCnt) + '차 시도 후, 페이스북 크롤링 성공')
            else:
                print('3차 시도에도 불구하고 페이스북 로그인 실패. --> 페이스북 크롤링봇의 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')
else:
    print('페이스북 크롤링을 위한 정보가 존재하지 않습니다.')

