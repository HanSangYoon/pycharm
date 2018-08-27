#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import facebookCrawlerBot_new as snsScrapBot
#from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import instagramCrawlerBot as instagramScrapBot
#from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import kakaostoryCrawlerBot as kakaostoryScrapBot
#from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import naverBlogCrawlerBot as naverblogScrapBot
#from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import worknetCrawlerBot as worknetScrapBot

#facebook
# 외부에서 데이터를 받아야 함. 아래 설정은 임의 설정임
#facebook_USERURL = 'hyoungwoo.kim.zermatt'
facebook_USERURL = 'kpokem'
userName = '김동근'
#instagram_USERURL = 'dasolmom_'
#kakaoStory_USERURL = 'happyleader'
#naverBlog_USERURL = 'pcn1970'

#instagram
instagram_USERURL = 'therock'
#instagram_USERURL = 'dasolmom_'

#kakaostory
kakaoStory_USERURL = 'happyleader'

#naverBlog
naverBlog_USERURL = 'pcn1970'

# facebook crawling
if facebook_USERURL is not None:
    try:
        # CrawlingByFacebookCrawlBot
        # ResultDict1 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName)
        ResultDict1 = snsScrapBot.CrawlingByFacebookCrawlBot(1, facebook_USERURL, userName)

        if ResultDict1 == True:
            print('페이스북 크롤링 성공')
        else:
            print('페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

    except Exception as ex_facebook:

        print('페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook)
        print()

        try:
            # ResultDict2 = snsScrapBot.login_facebook(self, 1, facebook_USERURL, userName)
            ResultDict2 = snsScrapBot.CrawlingByFacebookCrawlBot(1, facebook_USERURL, userName)

            if ResultDict2 == True:
                print('2차 페이스북 크롤링 성공')
            else:
                print('2차 페이스북 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')


        except Exception as ex_facebook2:
            print('2차 페이스북 크롤링이 내부 요인에 의해 중지 되었습니다. -> ', ex_facebook2)

'''
# instagram Crawling
try:
    print('인스타그램 크롤링')
    returnValue_instagram = instagramScrapBot.CrawlingByInstagramCrawlBot(instagram_USERURL)

    if returnValue_instagram == True:
        print('인스타그램 크롤링 성공')
    else:
        print('인스타그램 크롤링이 내부 요인에 의해 결과 값이 제대로 전달되지 않았습니다.')

except Exception as ex_insta:
    print('인스타그램 크롤링이 내부 요인에 의해 중지되었습니다. -> ', ex_insta)


#userNaverBlogURL = 'pcn1970'
'''

# kakaoStory Tscore 항목

# naverBlog Tscore 항목

# instagram Tscore 항목

# No.4 통합된 Dictionary Type Data로 TScore 산출
# tScore_result = calculateTScore(tScoreRelated_TotalData)
