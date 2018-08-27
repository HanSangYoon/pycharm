#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import logging.handlers
import time

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import \
    Getting_HTMLDoc_bSoup4 as Get_HTML_bs
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mongoDB_conn
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection

global hereWork

'''
class Getting_TrustScore(hereWork):

    def __init__(self):
        self.hereWorkVal = hereWork
    #hereWork = 'FaceBook'
'''
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
fileHandler = logging.handlers.RotatingFileHandler('C:/python_project/log/' + hereWork + '_crawlerbot_logging_' + currTime + '_Tscore', maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

#logging
logger.debug(hereWork + '_crawlerbot_debugging on' + currTime)
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')

#T Score 관련 항목 정보 추출
def getTrustScore(fb_pageID, UserName, loginCount, web_driver):


    timeLine_url = 'https://www.facebook.com/' + fb_pageID

    #No.1 PROFILE --> 이름(이름 일치 여부), 소개글, 프로필 정보를 통해서 전체 Tscore를 산출하여 return
    profileInfoDictTypeData = getProfileData(fb_pageID, timeLine_url, UserName, loginCount, web_driver)

    #No.2 ABOUTINFO --> 개요/경력 및 학력/거주했던 장소/연락처 및 기본 정보/가족 및 결혼 연애상태/자세한 소개 추출
    aboutInfoDictTypeData = getAboutInfoData(fb_pageID, loginCount, web_driver)

    #No.3 데이터 통합
    tScoreRelated_TotalData = dict(profileInfoDictTypeData, **aboutInfoDictTypeData)

    #facebook Tscore 항목
    #print('페이스북 T-score 항목 추출 결과 출력 : ', tScoreRelated_TotalData)
    logger.debug('페이스북 항목 추출 결과 출력 : {} '.format(tScoreRelated_TotalData))

    tScore_result = calculateTScore(tScoreRelated_TotalData)



#function No.01 ###########################################################################
# https://www.facebook.com/userpageID
def getProfileData(fbPageID, User_timeLine_site_url_addr, insertedName, lgnCnt, driver):

    #data 담을 그릇
    profileDic = {}
    profileInfoList = []

    fb_tmln_soup= Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, User_timeLine_site_url_addr)

    # get applicant's name
    usernamefromResume = insertedName.replace(' ', '')
    profileDic[hereWork + '_페이지ID'] = fbPageID

    #이름 일치 여부
    try:
        user_name = fb_tmln_soup.select('#fb-timeline-cover-name > a')[0].text.replace(' ', '')
        logger.debug('페이스북 상의 사용자 이름 : {}'.format(user_name))
        print('페이스북 상의 사용자 이름 : ', user_name)

        #profileDic[hereWork + '_' + user_name] = user_name

    except:
        logger.debug('페이스북 사용자 이름을 가져올 수 없습니다.')
        user_name = usernamefromResume
        print('페이스북 상의 사용자 이름 : ', user_name)


    if user_name == usernamefromResume:
        #print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')
        # 페이스북 사용자 이름과 이력서의 신청인 이름이 일치하므로, 이력서 상의 이름을 사용자의 이름으로 한다.
        logger.debug('[이름 일치]facebook user name => {} , 이력서 상의 이름 => {}'.format(user_name, usernamefromResume))
        profileDic['사용자이름'] = user_name
        #field : userName

    else:
        #print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')
        # 페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않으므로, 이력서 상의 이름을 사용자의 이름으로 한다.
        logger.debug('[이름 불-일치]facebook user name => {} , 이력서 상의 이름 => {}'.format(user_name, usernamefromResume))
        profileDic['사용자이름'] = user_name
        profileDic['사용자이름_이력서'] = usernamefromResume
        # field : userName_resume


    # 페이스북 타임라인 좌측 상단의 프로필(소개글) https://www.facebook.com/facebook_PageID?
    try:
        # 타임라인 프로필 내 소개글 존재 여부
        intro_text_title = fb_tmln_soup.select(
            'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > span')
        if not intro_text_title:

            logger.debug('타임라인 프로필 내 소개글이 존재하지 않습니다.')
        else:
            # 출력 내용 : '소개'
            logger.debug(intro_text_title[0].text)

            try:
                # 타임라인 프로필 내 소개글
                # make Data : profileDic[소개]
                intro_text_detail = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div#profile_intro_card_bio > div > div > div > span')

                profileDic[intro_text_title[0].text.replace(' ', '')] = intro_text_detail[0].text.replace(' ', '')

            except Exception as ew:
                # make Data [소개:소개글]
                logger.debug('소개글 게시판 HTML 구조가 변경되어 다시 검색합니다. {}'.format(ew))
                intro_text_detail2 = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div > div')
                intro_text_detail = intro_text_detail2

                profileDic[intro_text_title[0].text.replace(' ', '')] = intro_text_detail[0].text.replace(' ', '')

            logger.debug('타임라인 프로필 내 소개글 => {}'.format(profileDic))
            #예:) {'FaceBook_페이지ID': 'kpokem', '사용자이름': '김형우', '소개': '응급의학과의사.이불밖을나오는순간부터당신은다칠수있습니다.'}

    except Exception as e:
        logger.error('페이스북 타임라인 프로필(소개글)이 존재하지 않습니다.=> {}'.format(e))

        profileDic['소개'] = ''

    # 페이스북 타임라인 좌측 상단의 프로필(세부 프로필 내용, 공개 여부에 따라 항목 개수가 상이함) https://www.facebook.com/facebook_PageID?
    try:
        profile_lists_origin            = fb_tmln_soup.select('div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')
        profile_list_detail_texts_old   = fb_tmln_soup.select('div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
        lengthOfProfileList             = len(profile_lists_origin)
        lengthOfDetailListText          = len(profile_list_detail_texts_old)
        originalHTMLDOMRegion           = 'div#intro_container_id > div:nth-of-type(2) >'
        alteredHTMLDOMRegion            = 'div#intro_container_id > div:nth-of-type(1) >'

        # DOM 구조 변경에 따른 경로 수정
        if lengthOfProfileList == 0:

            # 경로가 변경되었을 경우, 경로 변경
            profile_lists_assem         = fb_tmln_soup.select(alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            originalHTMLDOMRegion       = alteredHTMLDOMRegion
            logger.debug('DOM 구조 변경에 따른 경로 수정 감지 후, 프로필 영역 개수 확인 => {}'.format(len(profile_lists_assem)))

        else:
            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_lists_assem       = fb_tmln_soup.select(originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')


        if lengthOfDetailListText == 0:

            # 경로가 변경되었을 경우, 경로 변경
            profile_list_detail_texts = fb_tmln_soup.select(alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            originalHTMLDOMRegion = alteredHTMLDOMRegion
            logger.debug('문서의 구조 변경이 감지됨.')

        else:
            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_detail_texts = fb_tmln_soup.select(originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')


        if not profile_list_detail_texts:
            logger.debug('사용자가 프로필 정보를 등록하지 않았습니다.')

        else:
            logger.debug('프로필 정보 : {}'.format(profile_list_detail_texts[0].text))

        prf = 0

        profileDic['프로필길이'] = str(len(profile_lists_assem))

        try:
            while prf < len(profile_lists_assem):
                key = '프로필_0' + str(int(prf + 1))
                print('key : ', key)

                value = fb_tmln_soup.select(
                    originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        int(prf + 1)) + ') > div > div > div > div')[0].text.replace(" ", "")
                print('value : ', value)

                logger.debug('{} : {}'.format(key, value))

                profileDic[key] = value
                profileInfoList.append(value)

                prf += 1

        except:
            logger.debug('더이상 가져올 수 있는 정보가 없습니다.')

    except Exception as e:
        logger.error('프로필 정보 취득 중 오류-> {}'.format(e))

    logger.debug('프로필 : {}'.format(profileDic))

    #Only For MariaDB insertion
    profileDic['프로필정보'] = '@'.join(profileInfoList)


    # 1. DB Connection === profileDic INSERT 하기 [MongoDB]=======================================
    currDate = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(
        time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min) + '-' + str(time.localtime().tm_sec)

    profileDic['페이스북프로필정보입력시간'] = currDate

    #MariaDB
    #DB insert 시 data는 dictionary의 value 값을 넣어야 함. 6개의 데이터 입력
    logger.debug('Facebook_페이지ID: {}, 사용자이름: {}, 소개: {}, 프로필길이: {}, 프로필정보:{}, 입력시간: {}'.format(
        profileDic[hereWork + '_페이지ID'], profileDic['사용자이름'], profileDic['소개'],profileDic['프로필길이'], profileDic['프로필정보'], profileDic['페이스북프로필정보입력시간']))

    try:
        # Server Connection to MySQL:
        databaseConnection = mysqlConnection.DatabaseConnection()
        databaseConnection.insert_profile_record(profileDic[hereWork + '_페이지ID'], profileDic['사용자이름'], profileDic['소개'],
                                             profileDic['프로필길이'], profileDic['프로필정보'], profileDic['페이스북프로필정보입력시간'])

        logger.debug('프로필저장_완료')

    except Exception as e_maria:
        logger.error('[ Error ] MariaDB Proifile information Insertion => {}'.format(e_maria))

    # 프로필 정보 저장 완료
    return profileDic

# function No.02 ##########################################################################
def getAboutInfoData(userPageId, loginCnt, driver):

    aboutDataDic = {}
    #aboutOverViewDataDic = {}
    #overViewDataList = []

    # No.1 [개요]
    detail_url_overview = 'https://www.facebook.com/' + userPageId + '/about?section=overview'
    detail_fb_overview_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_overview)

    about_overviewURL = '#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div'

    try:
        aboutOverview_middle_lists = detail_fb_overview_info_soup.select(
            about_overviewURL + ' > div:nth-of-type(1) > ul > li')

        #개요 항목 리스트 갯수
        print('개요 항목 리스트 갯수 : ', len(aboutOverview_middle_lists) )
        '''
        # 개요 항목 리스트 추출
        for about_list in range(len(aboutOverview_middle_lists)):
            logger.debug('개요항목 : {} '.format(aboutOverview_middle_lists + ':nth-of-type(' + str(about_list + 1) + ')')[0].text)
            overview_key = 'overview_l_0' + str(about_list +1)
            overview_value = aboutOverview_middle_lists[about_list].text
            aboutOverViewDataDic[overview_key] = overview_value
            print(overview_value)

            #List에 개요데이터 취합
            overViewDataList.append(overview_value)
        '''
        ##List의 개요데이터를 텍스트로 변환하여 aboutDataDic['개요정보']의 value 값으로 할당
        #maria : fb_overview_info
        #aboutDataDic['개요정보'] = '@'.join(overViewDataList)
        #print("aboutDataDic['개요정보'] : ", aboutDataDic['개요정보'])

    except Exception as e:
        logger.error('개요 항목이 존재하지 않음. -> {}'.format(e))
        #aboutDataDic['개요정보'] = ''

    try:
        aboutOverview_rightSide_lists = detail_fb_overview_info_soup.select(about_overviewURL + ' > div:nth-of-type(2) > ul > li')
        # 개요 항목 우측의 리스트 개수
        # print(len(aboutOverview_rightSide_lists))
        # 개요 항목 우측 리스트 추출
        for about_list_right in range(len(aboutOverview_rightSide_lists)):
            # 우측 리스트의 제목: 전화번호, 주소, 소셜링크, 웹사이트, 생일
            # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(1)
            aboutPage_list_right_title = detail_fb_overview_info_soup.select(
                about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                    about_list_right + 1) + ') > div > div:nth-of-type(2) > span > div:nth-of-type(1)')

            # 우측 리스트의 내용
            # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(2)
            aboutPage_list_right_contents = detail_fb_overview_info_soup.select(
                about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                    about_list_right + 1) + ') > div > div:nth-of-type(2) > span > div:nth-of-type(2)')

            # print(aboutOverview_rightSide_lists[about_list_right].text)
            #logger.debug('개요 우측 제목 : {} , 내용 : {}'.format(aboutPage_list_right_title[0].text, aboutPage_list_right_contents[0].text))

            #make Data
            aboutDataDic[aboutPage_list_right_title[0].text.replace(" ", "") + '정보'] = aboutPage_list_right_contents[0].text.replace(" ", "")
            #logger.debug('개요출력 테스트 {}:{}'.format(aboutPage_list_right_title[0].text.replace(" ", ""), aboutPage_list_right_contents[0].text.replace(" ", "")))

            #예:) aboutDataDic['전화번호정보'],aboutDataDic['주소정보'],aboutDataDic['소셜링크정보'],aboutDataDic['웹사이트정보'],aboutDataDic['생일정보']
            #print("개요항목 우측 리스트 값들 : ", aboutDataDic['전화번호정보'] ,aboutDataDic['주소정보'] ,aboutDataDic['소셜링크정보'] ,aboutDataDic['웹사이트정보'] ,aboutDataDic['생일정보'])

    except Exception as e:
        logger.error('개요 항목이 존재하지 않음. -> {}'.format(e))
        try:
            #개요 우측의 정보 입력란이 없을 경우
            aboutDataDic['전화번호정보'] = ''
            aboutDataDic['주소정보'] = ''
            aboutDataDic['소셜링크정보'] = ''
            aboutDataDic['웹사이트정보'] = ''
            aboutDataDic['생일정보'] = ''

        except Exception as e_moreDetail:
            logger.error('정보를 담을 딕셔너리가 더 생성되어야 합니다. in getAboutInfoData() : {}'.format(e_moreDetail))

    #개요 완료
    print('##############################################################')


    try:
        # No.2 [경력 및 학력]
        # https://www.facebook.com/userpageID/about?section=education
        detail_url_education = 'https://www.facebook.com/' + userPageId + '/about?section=education'
        detail_fb_education_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_education)
        # about_educationURL = '#pagelet_eduwork > div > div'
        aboutEducation_lists = detail_fb_education_info_soup.select('#pagelet_eduwork > div > div')
        # print(len(aboutEducation_lists))


        for about_length_of_education_list in range(len(aboutEducation_lists)):
            work_history_lists_title = detail_fb_education_info_soup.select(
                '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > div > span')[0].text

            logger.debug(work_history_lists_title)  # 직장/전문기술/학력

            if '전문 기술' in work_history_lists_title:
                try:
                    special_work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > ul > li > div'
                    special_work_history_lists = detail_fb_education_info_soup.select(special_work_history_lists_dir)

                    logger.debug('TestPrint:{}'.format(detail_fb_education_info_soup.select(special_work_history_lists_dir)[0].text))
                    print('TestPrint:', detail_fb_education_info_soup.select(special_work_history_lists_dir)[0].text)

                    # make Data
                    aboutDataDic['전문기술정보길이'] = str(len(special_work_history_lists))
                    aboutDataDic['전문기술'] = detail_fb_education_info_soup.select(special_work_history_lists_dir)[0].text

                    #전문기술
                    aboutDataDic['전문기술정보'] = detail_fb_education_info_soup.select(special_work_history_lists_dir)[0].text.replace(" ", "").replace(" · ", "_")
                    print("aboutDataDic['전문기술정보']", aboutDataDic['전문기술정보'])

                except Exception as e_special:
                    print('전문기술 추출 중 에러', e_special)
                    logger.error('전문기술 추출 중 에러:{}'.format(e_special))

            #직장_01/직장_02/직장_03/...
            elif '직장' in work_history_lists_title:
                aboutDataWorkList = []

                try:

                    work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(
                        about_length_of_education_list + 1) + ') > ul > li'
                    work_history_lists = detail_fb_education_info_soup.select(work_history_lists_dir)

                    for about_length_of_edu_detail in range(len(work_history_lists)):
                        logger.debug(detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text)

                        logger.debug(detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text)

                        work_history_title = detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text

                        work_history_contents_pre = detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2) > div')[0].text

                        work_history_contents = '(' + work_history_contents_pre.replace(" ", "").replace("·", "").replace("~", "_") + ')'

                        # make Data
                        aboutDataDic['직장정보길이'] = str(len(work_history_lists))
                        aboutDataDic['근무지_0' + str(about_length_of_edu_detail + 1)] = \
                        detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div ')[0].text

                        aboutDataDic['근무정보_0' + str(about_length_of_edu_detail + 1)] = detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text

                        aboutDataWorkList.append(work_history_title.replace(" ", ""))
                        aboutDataWorkList.append(work_history_contents.replace(" ", ""))

                    # 직장
                    # For Only MariaDB Insertion
                    aboutDataDic['직장이력'] = '@'.join(aboutDataWorkList)
                    print("aboutDataDic['직장이력']", aboutDataDic['직장이력'])

                except Exception as e_workInfo:
                    print('직장 정보 추출 중 에러 발생')
                    logger.error('직장 정보 추출 중 에러 발생:{}'.format(e_workInfo))


            #/학력_01/학력_02/학력_03/...
            else:
                aboutDataEduList = []

                try:
                    edu_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > ul > li'
                    edu_history_lists = detail_fb_education_info_soup.select(edu_history_lists_dir)

                    for about_length_of_edu_detail in range(len(edu_history_lists)):
                        logger.debug(detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text)

                        logger.debug(detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text)


                        edu_history_lists_title = detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text

                        edu_history_lists_contents_pre = detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text

                        edu_history_lists_contents = '(' + edu_history_lists_contents_pre.replace(" ", "").replace("·", "").replace("~", "_") + ')'

                        #make Data
                        aboutDataDic['학력정보길이'] = str(len(edu_history_lists))
                        aboutDataDic['학력이력_0' + str(about_length_of_edu_detail+1)] = detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text

                        aboutDataDic['학력이력상세정보_0' + str(about_length_of_edu_detail + 1)] = \
                        detail_fb_education_info_soup.select(edu_history_lists_dir + ':nth-of-type(' + str(
                            about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text

                        aboutDataEduList.append(edu_history_lists_title.replace(" ", ""))
                        aboutDataEduList.append(edu_history_lists_contents)

                    #학력
                    # For Only MariaDB Insertion
                    aboutDataDic['학력정보'] = '@'.join(aboutDataEduList)
                    print("aboutDataDic['학력정보']", aboutDataDic['학력정보'])
                except Exception as e_eduHistory:
                    print('학력 정보 추출 중 에러 발생')
                    logger.error('학력 정보 추출 중 에러 발생:{}'.format(e_eduHistory))

    except Exception as e:
        print('at 477 : ', e)
        logger.error(e)

    #경력 및 학력 단계 완료
    print('##############################################################')
    try:
        # No.3 [거주했던 장소]
        # https://www.facebook.com/userpageID/about?section=living
        detail_url_living = 'https://www.facebook.com/' + userPageId + '/about?section=living'
        detail_fb_living_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_living)
        aboutLiving_lists = detail_fb_living_info_soup.select('#pagelet_hometown > div > div')

        for about_length_of_living_list in range(len(aboutLiving_lists)):
            # print('about_length_of_living_list : ', about_length_of_living_list)
            living_history_lists_title = detail_fb_living_info_soup.select('#pagelet_hometown > div > div:nth-of-type(' + str(about_length_of_living_list + 1) + ') > div > span')[0].text

            # 거주지와 출신지/기타 살았던 곳/거주지
            logger.debug('living_history_lists_title : {}'.format(living_history_lists_title))

            living_history_lists_dir = '#pagelet_hometown > div > div:nth-of-type(' + str(about_length_of_living_list + 1) + ') > ul > li'
            living_history_lists = detail_fb_living_info_soup.select(living_history_lists_dir)

            aboutDataLivingList = []

            #거주지와 출신지
            if '거주지' in living_history_lists_title:

                if len(living_history_lists) == 1:
                    #for about_length_of_living_detail in range(len(living_history_lists)):
                    #logger.debug('len(living_history_lists) : ', len(living_history_lists))
                    logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)    #현재 거주지 '값', 출신지 '값', ~에 이사의 '값',
                    logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)     #'현재 거주지'

                    living_history_title = detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > div')[0].text
                    living_history_contents_pre = detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text

                    living_history_contents = '(' + living_history_contents_pre.replace(" ", "").replace("·", "").replace("~", "_") + ')'


                    #make Data
                    #living_history_lists_title.replace(" ", "") : 거주지,
                    aboutDataDic[living_history_lists_title.replace(" ", "")] = detail_fb_living_info_soup.select(living_history_lists_dir +' > div > div > div > div > div > div:nth-of-type(2) > div')[0].text.replace(" ", "") +"(" + detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + ")"
                    #aboutDataDic['거주지와출신지']

                    #예:) 서울(현재거주지)
                    aboutDataDic['거주지정보'] = detail_fb_living_info_soup.select(living_history_lists_dir +' > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text.replace(" ", "")

                    aboutDataLivingList.append(living_history_title.replace(" ", ""))
                    aboutDataLivingList.append(living_history_contents.replace(" ", "").replace("·", ""))

                    aboutDataDic['거주지정보'] = '@'.join(aboutDataLivingList)
                    #aboutDataDic['주소정보'] = '@'.join(aboutDataLivingList)

                    print("aboutDataDic['거주지정보']", aboutDataDic['거주지정보'])

                else:
                    for about_length_of_living_detail in range(len(living_history_lists)):
                        #logger.debug('len(living_history_lists) : ', len(living_history_lists))
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)

                        #make Data
                        if about_length_of_living_detail == 0:
                            aboutDataDic[living_history_lists_title.replace(" ", "") + '@거주지'] = detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")"
                            # aboutDataDic['거주지와출신지@거주지']

                        elif about_length_of_living_detail == 1:
                            aboutDataDic[living_history_lists_title.replace(" ", "") + '@출신지'] = \
                            detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(
                                about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")"
                            # aboutDataDic['거주지와출신지@출신지']

                            aboutDataDic['출신지정보'] = detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text


                        #For Only MariaDB Insertion
                        aboutDataLivingList.append(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")" )

                    aboutDataDic['거주지정보'] = '@'.join(aboutDataLivingList)
                    #aboutDataDic['주소정보'] = '@'.join(aboutDataLivingList)
                    # 예:) 서울(현재거주지)_제주도제주(출신지)

                    print("aboutDataDic['거주지정보']", aboutDataDic['거주지정보'])


            #기타 살았던 곳
            else:
                # 기타 살았던 곳: 1개
                if len(living_history_lists) == 1:

                    for about_length_of_living_detail in range(len(living_history_lists)):
                        #logger.debug('len(living_history_lists) : ', len(living_history_lists))
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text)

                        #make Data
                        #예:) 제주도제주(1990년1월에이사)
                        aboutDataDic[living_history_lists_title.replace(" ", "")] = detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")"
                        #aboutDataDic['기타살았던곳']


                        # For Only MariaDB Insertion
                        aboutDataLivingList.append(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")" )

                    aboutDataDic['기타거주지정보'] = '@'.join(aboutDataLivingList)
                    #aboutDataDic['주소정보'] = '@'.join(aboutDataLivingList)
                    print("aboutDataDic['기타거주지정보']", aboutDataDic['기타거주지정보'])

                # 기타 살았던 곳: 복수개
                else:
                    for about_length_of_living_detail in range(len(living_history_lists)):
                        #logger.debug('len(living_history_lists) : ', len(living_history_lists))
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                        logger.debug(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)

                        #make Data
                        aboutDataDic[living_history_lists_title.replace(" ", "")] = detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")"

                        # For Only MariaDB Insertion
                        aboutDataLivingList.append(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text + "(" + detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text + ")" )

                    aboutDataDic['기타거주지정보'] = '@'.join(aboutDataLivingList)
                    print("aboutDataDic['기타거주지정보']", aboutDataDic['기타거주지정보'])

    except Exception as e:
        print(e)
    #거주했던 장소 완료

    try:
        # No.4 [연락처 및 기본정보]-연락처 정보, 웹사이트 및 소셜 링크 정보, 기본 정보
        # https://www.facebook.com/userpageID/about?section=contact-info
        detail_url_contact = 'https://www.facebook.com/' + userPageId + '/about?section=contact-info&pnref=about'
        detail_fb_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_contact)

        user_pglet_contactData_title_01_1=''
        user_pglet_contactData_title_01_2 = ''
        user_pglet_contactData_title_01_3 = ''

        # [제목] [연락처 및 기본정보]-[연락처 정보]란 제목
        try:
            user_pglet_contactData_title_01_1 = detail_fb_info_soup.select('#pagelet_contact > div > div:nth-of-type(1) > div > span')
        except Exception as e:
            logger.error('[연락처 및 기본정보]-[연락처 정보]란 제목 ERROR  :{}'.format(e))

        # [제목] [연락처 및 기본정보]-[웹사이트 및 소셜 링크]란 제목
        try:
            user_pglet_contactData_title_01_2 = detail_fb_info_soup.select('#pagelet_contact > div > div:nth-of-type(2) > div > div > span')
        except Exception as e:
            logger.error('[연락처 및 기본정보]-[웹사이트 및 소셜 링크]란 제목 ERROR  :{}'.format(e))

        # [제목] [연락처 및 기본정보]-[기본 정보]란 제목
        try:
            user_pglet_basicData_title_01_3 = detail_fb_info_soup.select('#pagelet_basic > div > div > span')
        except Exception as e:
            logger.error('[연락처 및 기본정보]-[기본 정보]란 제목 ERROR  :{}'.format(e))


        user_pglet_data = detail_fb_info_soup.select('div#pagelet_contact > div > div')
        #logger.debug('user_pglet_data = {}'.format(user_pglet_data))

        length_user_pglet_data = len(user_pglet_data)

        if length_user_pglet_data == 0:
            logger.debug('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : {}'.format(length_user_pglet_data))
            logger.debug('페이스북 접속이 원할하지 않아 다시 시도해야 합니다.')

            if loginCnt <= 2:
                userInfoDetailDic = False
                return userInfoDetailDic
            else:
                logger.debug('페이스북 크롤링을 재 구동하여야 합니다. 작동을 중지합니다.')
                driver.close()

        else:
            aboutDataContactList = []

            # [연락처 정보]란 취득
            logger.debug('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : {}'.format(length_user_pglet_data))

            if not user_pglet_contactData_title_01_1:
                logger.debug('사용자가 연락처 정보를 등록하지 않았습니다.')

                # make Data
                aboutDataDic[user_pglet_contactData_title_01_1.replace(" ", "")] = ''
                aboutDataDic['연락처정보'] = ''

            else:
                # pagelet_contact
                if '연락처' in user_pglet_contactData_title_01_1[0].text:
                    logger.debug(user_pglet_contactData_title_01_1[0].text)  # 연락처 정보

                    # [연락처 정보]란 하단 세부 정보 타이틀 : 예)휴대폰/주소/Facebook 들 중 존재하는 세부제목
                    pagelet_contact_dir_list = 'div#pagelet_contact > div > div:nth-of-type(1) > ul > li'

                    # [연락처 정보]란 하단 세부 정보 타이틀 갯수
                    length_of_contList = len(detail_fb_info_soup.select(pagelet_contact_dir_list))

                    conCycle = 0
                    # [연락처 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                    try:
                        # 하단 세부 정보 길이 만큼 loop 실행해 key:value 생성
                        while conCycle < length_of_contList:
                            userContactInfoListTitle = detail_fb_info_soup.select(
                                pagelet_contact_dir_list + ':nth-of-type(' + str(
                                    int(conCycle + 1)) + ') > div > div:nth-of-type(1)')[0].text
                            #예:) 휴대폰


                            # [연락처 정보]란_title
                            key = userContactInfoListTitle.replace(" ", "")
                            # print('연락처 정보_title: ', key)

                            # [연락처 정보]란_value
                            value = detail_fb_info_soup.select(
                                pagelet_contact_dir_list + ':nth-of-type(' + str(
                                    int(conCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[
                                0].text.replace(" ", "")

                            aboutDataDic[key.replace(" ", "")] = value
                            #aboutDataDic['휴대폰'], aboutDataDic['주소'], aboutDataDic['Facebook']

                            # For Only MariaDB Insertion
                            aboutDataContactList.append(value)

                            conCycle += 1

                        #aboutDataDic['연락처정보'] = '@'.join(aboutDataContactList)
                        print("aboutDataDic['연락처정보'] :", aboutDataDic['연락처정보'])

                    except:
                        logger.debug('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                        #logger.debug('연락처 정보 수집 결과[Dictionary type]: {}'.format(aboutDataDic))


            # [웹사이트 및 소셜 링크]란
            if not user_pglet_contactData_title_01_2:
                logger.debug('사용자가 웹사이트 및 소셜 링크 정보를 등록하지 않았습니다.')

                # make Data
                aboutDataDic[user_pglet_contactData_title_01_2.replace(" ", "")] = ''
                aboutDataDic['웹사이트및소셜링크정보'] = ''
            else:
                # pagelet_contact
                if '웹사이트' in user_pglet_contactData_title_01_2[0].text:
                    logger.debug(user_pglet_contactData_title_01_2[0].text)  # 웹사이트 및 소셜 링크 정보

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
                            #예:) 웹사이트


                            # [웹사이트 및 소셜 링크]란 title
                            key = userContactWebInfoListTitle.replace(" ", "")
                            logger.debug('웹사이트 및 소셜 링크 정보_title: {}'.format(key))

                            # [웹사이트 및 소셜 링크]란 value
                            value = detail_fb_info_soup.select(
                                pagelet_contact_webSite_dir_list + ':nth-of-type(' + str(
                                    int(conWebCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span > ul')[0].text.replace(" ", "")

                            # make Data
                            aboutDataDic[key.replace(" ", "")] = value
                            #aboutDataDic['웹사이트'], aboutDataDic['소셜링크']

                            # For Only MariaDB Insertion
                            aboutDataContactList.append(value)

                            #aboutInfo[key] = value
                            conWebCycle += 1


                        aboutDataDic['연락처정보및웹사이트및소셜링크정보'] = '@'.join(aboutDataContactList)
                        print("aboutDataDic['웹사이트및소셜링크정보'] :", aboutDataDic['웹사이트및소셜링크정보'])

                    except:
                        logger.debug('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                        #logger.debug('웹사이트 및 소셜 링크 정보 수집 결과[Dictionary type]: {}'.format(aboutDataDic))

            # [기본 정보]란 취득
            if not user_pglet_basicData_title_01_3:
                logger.debug('사용자가 기본 정보를 등록하지 않았습니다.')

                # make Data
                aboutDataDic[user_pglet_basicData_title_01_3.replace(" ", "")] = ''

                aboutDataDic['기본정보란정보'] = ''

            else:
                # pagelet_basic
                if '기본' in user_pglet_basicData_title_01_3[0].text:
                    logger.debug(user_pglet_basicData_title_01_3[0].text)  # 기본 정보

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
                            #생일/음력생일/성별/혈액형/종교관

                            # [기본 정보]란 value
                            value = detail_fb_info_soup.select(
                                pagelet_basic_dir_list + ':nth-of-type(' + str(
                                    int(baseCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[
                                0].text.replace(" ", "")

                            # make Data
                            aboutDataDic[key.replace(" ", "")] = value
                            #aboutDataDic['생일'], aboutDataDic['음력생일'], aboutDataDic['성별'], aboutDataDic['혈액형'], aboutDataDic['종교관']

                            # For Only MariaDB Insertion
                            aboutDataContactList.append(value)

                            baseCycle += 1

                        aboutDataDic['기본정보란정보'] = '@'.join(aboutDataContactList)
                        print("aboutDataDic['기본정보란정보'] :", aboutDataDic['기본정보란정보'])

                    except:
                        logger.debug('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                        #logger.debug('기본 정보 수집 결과 [Dictionary type]: {}'.format(aboutDataDic))

    except Exception as e:
        print(e)

    #연락처 및 기본정보 완료


    try:
        # No.5 [가족 및 결혼/연애 상태]
        # https://www.facebook.com/userpageID/about?section=relationship
        detail_url_relationship = 'https://www.facebook.com/' + userPageId + '/about?section=relationship'
        detail_fb_relationship_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_relationship)
        aboutRelationship_lists = detail_fb_relationship_info_soup.select('#pagelet_relationships > div')

        for about_length_of_Relationships_list in range(len(aboutRelationship_lists)):

            try:
                # 결혼/연애 상태
                relationship_marriage_status_title = detail_fb_relationship_info_soup.select(
                    '#pagelet_relationships > div:nth-of-type(' + str(
                        about_length_of_Relationships_list + 1) + ') > div > span')[0].text
                logger.debug('relationship_marriage_status_title : {}'.format(relationship_marriage_status_title))  #결혼/연애 상태

                relationship_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(
                    about_length_of_Relationships_list + 1) + ') > ul > li'

                relationship_lists = detail_fb_relationship_info_soup.select(relationship_lists_dir)

                #결혼/연애 상태 의 대상자 수 판별
                if len(relationship_lists) == 1:

                    try:
                        # 결혼/연애상태의 대상자가 존재할 때
                        # 대상자 이름
                        relationship_list_name = detail_fb_relationship_info_soup.select(
                            relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                            0].text

                        # 기혼/미혼
                        relationship_list_status = detail_fb_relationship_info_soup.select(
                            relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                            0].text
                        logger.debug('relationship name & status : {}, {}'.format(relationship_list_name, relationship_list_status))

                        #make Data
                        aboutDataDic[relationship_marriage_status_title.replace("/", "").replace(" ", "")] = relationship_list_name + '(' + relationship_list_status + ')'
                        #aboutDataDic['결혼연애상태']

                        #결혼/연애 상태
                        #예) aboutDataDic['결혼연애상태'] = 남수현(기혼)

                        aboutDataDic['결혼연애상태정보'] = relationship_list_name + '(' + relationship_list_status + ')'


                    except Exception:
                        # 결혼/연애상태의 대상자가 존재하지 않을 때
                        relationship_list_name = detail_fb_relationship_info_soup.select(
                            relationship_lists_dir + ':nth-of-type(1) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > span')[0].text
                        logger.debug('relationship name : {}'.format(relationship_list_name))

                        #make Data
                        aboutDataDic[relationship_marriage_status_title.replace("/", "").replace(" ", "")] = ''
                        #aboutDataDic['결혼연애상태'] = ''

                        aboutDataDic['결혼연애상태정보'] = ''

                else:
                    # 결혼/연애상태의 대상자 수가 복수일 때

                    aboutDataMarriageList = []
                    for length_lists in range(len(relationship_lists)):
                        relationship_list_name = detail_fb_relationship_info_soup.select(
                            relationship_lists_dir + ':nth-of-type(' + str(
                                length_lists + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                            0].text
                        relationship_list_status = detail_fb_relationship_info_soup.select(
                            relationship_lists_dir + ':nth-of-type(' + str(
                                length_lists + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                            0].text

                        logger.debug(
                            'relationship name & status : {}, {}'.format(relationship_list_name, relationship_list_status))

                        #make Data
                        aboutDataDic[relationship_marriage_status_title.replace("/", "").replace(" ", "")+'_0'+str(about_length_of_Relationships_list + 1)] = relationship_list_name + '(' + relationship_list_status + ')'
                        #결혼/연애 상태 -> 결혼연애상태

                        aboutDataMarriageList.append( relationship_list_name + '(' + relationship_list_status + ')' )

                    aboutDataDic['결혼연애상태정보'] = '@'.join(aboutDataMarriageList)
                    print("aboutDataDic['결혼연애상태정보'] :", aboutDataDic['결혼연애상태정보'])



            except Exception:
                # 가족
                relationship_family_status_title = detail_fb_relationship_info_soup.select(
                    '#pagelet_relationships > div:nth-of-type(' + str(
                        about_length_of_Relationships_list + 1) + ') > div > div > span')[0].text
                logger.debug('relationship_family_status_title : {}'.format(relationship_family_status_title))

                relationship_family_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(
                    about_length_of_Relationships_list + 1) + ') > div > ul > li'
                relationship_family_lists = detail_fb_relationship_info_soup.select(relationship_family_lists_dir)


                if len(relationship_family_lists) == 1:
                    relationship_family_list_name = detail_fb_relationship_info_soup.select(
                        relationship_family_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[
                        0].text
                    relationship_family_list_status = detail_fb_relationship_info_soup.select(
                        relationship_family_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                        0].text
                    logger.debug(
                        'relationship name & status : {},{}'.format(relationship_family_list_name, relationship_family_list_status))

                    # make Data
                    aboutDataDic[relationship_family_status_title.replace(" ", "")] = relationship_family_list_name + '(' + relationship_family_list_status + ')'
                    # 가족
                else:

                    aboutDataFamilyList = []

                    for length_lists in range(len(relationship_family_lists)):
                        relationship_family_list_name = detail_fb_relationship_info_soup.select(
                            relationship_family_lists_dir + ':nth-of-type(' + str(
                                length_lists + 1) + ') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > span > a')[
                            0].text
                        relationship_family_list_status = detail_fb_relationship_info_soup.select(
                            relationship_family_lists_dir + ':nth-of-type(' + str(
                                length_lists + 1) + ') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[
                            0].text
                        logger.debug(
                            'relationship name & status : {}, {}'.format(relationship_family_list_name, relationship_family_list_status))

                        #make Data
                        aboutDataDic[relationship_family_status_title.replace(" ", "")+'_0'+str(about_length_of_Relationships_list + 1)] = relationship_family_list_name + '(' + relationship_family_list_status + ')'
                        #가족

                        aboutDataFamilyList.append( relationship_family_list_name + '(' + relationship_family_list_status + ')' )

                    aboutDataDic['가족정보'] = '@'.join(aboutDataFamilyList)
                    print("aboutDataDic['가족정보'] :", aboutDataDic['가족정보'])

    except Exception as e:
        print(e)

    #가족 및 결혼/연애 상태 완료


    try:
        # No.6 [자세한 소개]
        # https://www.facebook.com/userpageID/about?section=bio
        detail_url_bio = 'https://www.facebook.com/' + userPageId + '/about?section=bio'
        detail_fb_bio_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_bio)

        # bio와 Quotes는 기본으로 출력함
        about_Bio_title = detail_fb_bio_info_soup.select('#pagelet_bio > div > div > span')[0].text  # 예) 김동근님의 정보
        about_Bio_contents = detail_fb_bio_info_soup.select('#pagelet_bio > div > ul > li > span')[
            0].text  # 내용 또는 표시할 추가 정보 없음
        logger.debug('bio : {}, {}'.format(about_Bio_title, about_Bio_contents))

        #make Data
        aboutDataDic[about_Bio_title.replace(" ", "")] = about_Bio_contents.replace(" ", "").replace(".", "")
        aboutDataDic['자세한소개정보_개인'] = about_Bio_contents

        try:
            about_Pronounce = detail_fb_bio_info_soup.select('#pagelet_pronounce')
        except Exception as e:
            logger.debug('pagelet_pronounce 정보가 없습니다.')

        try:
            about_nicknames = detail_fb_bio_info_soup.select('#pagelet_nicknames')
        except Exception as e:
            logger.debug('pagelet_nicknames 정보가 없습니다. ')


        # bio와 Quotes는 기본으로 출력함
        about_Quotes_title = detail_fb_bio_info_soup.select('#pagelet_quotes > div > div > span')[0].text
        about_Quotes_contents = detail_fb_bio_info_soup.select('#pagelet_quotes > div > ul > li > div > div > span')[0].text

        logger.debug('quotes : {}, {}'.format(about_Quotes_title, about_Quotes_contents))

        #make Data
        aboutDataDic[about_Quotes_title.replace(" ", "")] = about_Quotes_contents   # 예) 좋아하는 문구
        aboutDataDic['자세한소개정보_좋아하는문구'] = about_Quotes_contents.replace(" ", "").replace("·", "")

    except Exception as e:
        print(e)


    try:
        # No.7 [중요 이벤트]
        # https://www.facebook.com/kpokem/about?section=year-overviews
        detail_url_yearOverviews = 'https://www.facebook.com/' + userPageId + '/about?section=year-overviews'
        detail_fb_yearOverviews_info_soup = Get_HTML_bs.__getHTMLDoc_beautifulSoup4(driver, detail_url_yearOverviews)
        yearOverviews_medly_about_title = detail_fb_yearOverviews_info_soup.select('div#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div > div > span')[0].text  # 중요 이벤트
        yearOverviews_medly_about_contents_lists = detail_fb_yearOverviews_info_soup.select(
            'div#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li')

        aboutDataYearEvents = []

        for list_length in range(len(yearOverviews_medly_about_contents_lists)):
            yearOverviews_medly_about_contents_detail_01 = detail_fb_yearOverviews_info_soup.select(
                '#timeline-medley > div > div#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
                    list_length + 1) + ') > div > div:nth-of-type(1) > span')[0].text  # 년도

            yearOverviews_medly_about_contents_detail_list = detail_fb_yearOverviews_info_soup.select(
                'div#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(list_length + 1) + ') > div > div:nth-of-type(2) > ul > li')

            # print(len(yearOverviews_medly_about_contents_detail_list))
            for detail_list_length in range(len(yearOverviews_medly_about_contents_detail_list)):
                yearOverviews_medly_about_contents_detail_contents = detail_fb_yearOverviews_info_soup.select(
                    'div#pagelet_timeline_medley_about > div:nth-of-type(2) > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
                        list_length + 1) + ') > div > div:nth-of-type(2) > ul > li:nth-of-type(' + str(
                        detail_list_length + 1) + ') > div > div > a > span')[0].text  # 내용

                logger.debug('{},{}'.format(yearOverviews_medly_about_contents_detail_01,yearOverviews_medly_about_contents_detail_contents))
                aboutDataDic[yearOverviews_medly_about_title.replace(" ", "") + '_0' + str(list_length+1)] = '(' + yearOverviews_medly_about_contents_detail_01.replace(" ", "") + ')' + yearOverviews_medly_about_contents_detail_contents + '_@'
                aboutDataYearEvents.append( '(' + yearOverviews_medly_about_contents_detail_01.replace(" ", "") + ')' + yearOverviews_medly_about_contents_detail_contents + '_@@@' )

        aboutDataDic['중요이벤트'] = '@'.join(aboutDataYearEvents)
        print("aboutDataDic['중요이벤트'] :", aboutDataDic['중요이벤트'])

    except Exception as e:
        print(e)


    # return 직전 최종 값 확인
    logger.debug('페이스북 정보 탭 > 연락처 및 기본 정보 -> {}'.format(aboutDataDic))

    # DB Insert
    # 1. DB Connection === profileDic INSERT 하기 [MongoDB]=======================================
    currDate = str(time.localtime().tm_year) + '-' + str(time.localtime().tm_mon) + '-' + str(
        time.localtime().tm_mday) + '-' + str(time.localtime().tm_hour) + '-' + str(time.localtime().tm_min) + '-' + str(time.localtime().tm_sec)

    aboutDataDic['페이스북개요정보입력시간'] = currDate
    aboutDataDic['페이스북고유주소'] = aboutDataDic['Facebook'].split('.')[1].replace('com/', '')
    #MariaDB
    #DB insert 시 data는 dictionary의 value 값을 넣어야 함. 6개의 데이터 입력

    #http://facebook.com/kpokem


    try:
        # Server Connection to MySQL:
        databaseConnection = mysqlConnection.DatabaseConnection()
        #aboutDataDic['전화번호정보'], aboutDataDic['주소정보'], aboutDataDic['소셜링크정보'], aboutDataDic['웹사이트정보'], aboutDataDic['생일정보'], aboutDataDic['중요이벤트']

        databaseConnection.update_aboutInfo_record( aboutDataDic['전문기술정보길이'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['전문기술정보'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['직장정보길이'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['직장이력'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['학력정보길이'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['학력정보'].replace(" ","").replace(".", ""),
                                                    aboutDataDic['출신지정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['거주지정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['기타거주지정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['휴대폰'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['Facebook'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['웹사이트'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['소셜링크'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['연락처정보및웹사이트및소셜링크정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['음력생일'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['성별'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['혈액형'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['종교관'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['기본정보란정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['결혼연애상태정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['가족정보'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['자세한소개정보_좋아하는문구'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", ""),
                                                    aboutDataDic['페이스북고유주소'].replace(" ","").replace("(", "{").replace(")", "}").replace(".", "")
                                                    )



    except Exception as e_maria:
        print('db error in getting Tscore module:', e_maria)
        logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

    return aboutDataDic


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



#T Score 산출
def calculateTScore(returnedResultDict):

    print('calculateTScore 진입')

    t_score_count = 0

    '''
    returnedResultDict.keys() 출력값
    dict_keys(['FaceBook_페이지ID', '사용자이름', '소개', '프로필길이', '프로필_01', '프로필_02', '프로필_03', '프로필정보', '페이스북프로필정보입력시간', '직장정보길이', '근무지_01', '근무정보_01', '근무지_02', '근무정보_02', '근무지_03', '근무정보_03', '직장이력', '전문기술정보길이', '전문기술', '전문기술정보', '학력정보길이', '학력이력_01', '학력이력상세정보_01', '학력이력_02', '학력이력상세정보_02', '학력정보', '거주지와출신지@거주지', '거주지와출신지@출신지', '출신지정보', '거주지정보', '기타살았던곳', '기타거주지정보', '거주지', '휴대폰', '주소', 'Facebook', '웹사이트', '소셜링크', '연락처정보및웹사이트및소셜링크정보', '생일', '음력생일', '성별', '혈액형', '종교관', '기본정보란정보', '결혼연애상태', '결혼연애상태정보', '가족_02', '가족정보', '김동근님의정보', '자세한소개정보_개인', '좋아하는문구', '자세한소개정보_좋아하는문구', '페이스북개요정보입력시간', '페이스북고유주소'])
    '''

    for search_t in returnedResultDict.keys():

        try:
            #성별
            if '성별' in search_t:
                search_t_value = returnedResultDict.get(search_t, [])

                if '남성' in search_t_value:
                    t_score_count = 0
                    logger.debug('성별 정보 검색 중...')
                    logger.debug('가산 근거 : 남성일 경우 근속 기간이 여성보다 길기 때문에 10점이 가산 됩니다.')
                    t_score_count += 10

                elif '여성' in search_t_value:
                    t_score_count_detail = 0
                    logger.debug('성별 정보 검색 중...')
                    logger.debug('가산 근거 : 여성일 경우 근속 기간이 남성보다 짧기 때문에 5점이 가산 됩니다.')
                    t_score_count_detail += 5
                    t_score_count += t_score_count_detail
            #good

            #근무지
            if '직장이력' in search_t:
                logger.debug('직장 이력 및 근무지 정보 검색 중...')

                search_t_value = returnedResultDict.get(search_t, [])
                returnScore = readCSV(search_t_value) #직장이력의 값
                print('500대 기업 비교 후 직장 이력 가산 점수 : ', returnScore)

                if '서울' in search_t_value:
                    logger.debug('가산 근거 : 근무지가 서울일 경우 15점이 가산 됩니다.')
                    t_score_count += 10

                elif '경기' in search_t_value:
                    logger.debug('가산 근거 : 근무지가 경기일 경우 10점이 가산됩니다.')
                    t_score_count += 5

                elif '병원' in search_t_value:
                    logger.debug('가산 근거 : 근무지가 경기일 경우 10점이 가산됩니다.')
                    t_score_count += 5

                else:
                    logger.debug('가산 근거 : 근무지가 비-수도권일 경우 5점이 가산됩니다.')
                    t_score_count += 3

                totalWorkScore = t_score_count + returnScore
                print('직장 정보 제공 가산점 :', totalWorkScore)

            # 학력사항 정보 검색
            if '학력이력' or '학력정보' in search_t:

                search_t_value = returnedResultDict.get(search_t, [])

                #졸업자
                if '졸업' in search_t_value:

                    #대학원 졸업자
                    if '대학원' in search_t_value:
                        logger.debug('대학원 소재지 정보 검색 중...')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' \
                                or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' \
                                or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' \
                                or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' \
                                or '한성대' or '서경대' or '성공회대' in search_t_value:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    #대학교 졸업자
                    elif '대학교' or 'Univ' or 'univ'in search_t_value:
                        logger.debug('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    #고등학교 졸업자
                    elif '고등학교' or 'High' or 'high' in search_t_value:
                        logger.debug('고등학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0

                        if '외국어' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '과학' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '민족사관' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '특성' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특성화고등학교일 경우 8점이 가산 됩니다.')
                            t_score_count_detail += 8
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 고등학교가 일반 고등학교일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail

                    #전문대학 졸업자
                    else:
                        logger.debug('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        t_score_count_detail += 3
                        t_score_count += t_score_count_detail

                #비 졸업자(졸업예정자)
                elif '예정' in search_t_value:

                    # 대학원 졸업예정자
                    if '대학원' or 'Gradu' or 'gradu' in search_t_value:
                        logger.debug('대학원 소재지 정보 검색')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    # 대학교 졸업예정자
                    elif '대학교' in search_t_value:
                        logger.debug('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    # 고등학교 졸업예정자
                    elif '고등학교' in search_t_value:
                        logger.debug('고등학교 소재지 정보 검색')
                        t_score_count_detail = 0

                        if '외국어' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '과학' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '민족사관' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '특성' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특성화고등학교일 경우 8점이 가산 됩니다.')
                            t_score_count_detail += 8
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 고등학교가 일반 고등학교일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail

                    # 전문대학 졸업예정자
                    else:
                        logger.debug('대학(2~3년제 대학) 소재지 정보 검색')
                        t_score_count_detail = 0
                        t_score_count_detail += 3
                        t_score_count += t_score_count_detail


                #비 졸업자
                else:
                    if '대학원' or 'Gradu' or 'gradu' in search_t_value:
                        logger.debug('대학원 소재지 정보 검색')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학원 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    # 대학교 졸업자
                    elif '대학교' or 'Univ' or 'univ' in search_t_value:
                        logger.debug('대학교 소재지 정보 검색')
                        t_score_count_detail = 0

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 서울일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 대학교 소재지가 경기일 경우 5점이 가산됩니다.')
                            t_score_count_detail += 5
                            t_score_count += t_score_count_detail

                    # 고등학교 졸업자
                    elif '고등학교' or 'High' or 'high' in search_t_value:
                        logger.debug('고등학교 소재지 정보 검색')
                        t_score_count_detail = 0

                        if '외국어' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '과학' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '민족사관' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특수목적고등학교일 경우 15점이 가산 됩니다.')
                            t_score_count_detail += 15
                            t_score_count += t_score_count_detail
                        elif '특성' in search_t:
                            logger.debug('가산 근거 : 출신 고등학교가 특성화고등학교일 경우 8점이 가산 됩니다.')
                            t_score_count_detail += 8
                            t_score_count += t_score_count_detail
                        else:
                            logger.debug('가산 근거 : 출신 고등학교가 일반 고등학교일 경우 10점이 가산 됩니다.')
                            t_score_count_detail += 10
                            t_score_count += t_score_count_detail

                    # 전문대학 졸업자
                    else:
                        logger.debug('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        t_score_count_detail += 3
                        t_score_count += t_score_count_detail

        except Exception as e_addr:
            logger.error( 'T SCORE EXCEPTION : {}'.format(e_addr) )

    logger.debug('T SCORE :', t_score_count)
    returnedResultDict['TSCORE'] = t_score_count
    returnedResultDict['CSCORE'] = 0
    returnedResultDict['MSCORE'] = 0

    try:
        # Server Connection to MySQL:
        databaseConnection = mysqlConnection.DatabaseConnection()
        #aboutDataDic['전화번호정보'], aboutDataDic['주소정보'], aboutDataDic['소셜링크정보'], aboutDataDic['웹사이트정보'], aboutDataDic['생일정보'], aboutDataDic['중요이벤트']

        databaseConnection.update_tcm_score( returnedResultDict['TSCORE'].replace(" ","").replace(".", ""),
                                             returnedResultDict['CSCORE'].replace(" ","").replace(".", ""),
                                             returnedResultDict['MSCORE'].replace(" ","").replace(".", ""),
                                             returnedResultDict['페이스북고유주소'].replace(" ","").replace(".", "")
                                                    )



    except Exception as e_maria:
        print('db error in getting Tscore module:', e_maria)
        logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

    return t_score_count
