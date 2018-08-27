#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

    print(driver.current_url)
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 2

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''

    last_height = driver.execute_script("return document.body.scrollHeight")
    print('last_height : ', last_height)
    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 10):

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
        autoScrolled_data_soup_html = bs(driver.page_source, 'html.parser')
        # print(autoScrolled_data_soup_html)
    # return bs(autoScrolled_data, 'html.parser')
    return autoScrolled_data_soup_html



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




#https://www.facebook.com/kpokem/about



'''
#페이지 스크롤 하면 하단의 체크인 부분을 가져올 수 있음.
yearOverviews_medly_friends     = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_friends')
yearOverviews_medly_photos      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_photos')
yearOverviews_medly_videos      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_videos')
yearOverviews_medly_map         = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_map')
yearOverviews_medly_sports      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_sports')
yearOverviews_medly_music       = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_music')
yearOverviews_medly_movies      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_movies')
yearOverviews_medly_tv          = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_tv')
yearOverviews_medly_books       = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_books')
yearOverviews_medly_games       = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_games')
yearOverviews_medly_likes       = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_likes')
yearOverviews_medly_events      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_events')
yearOverviews_medly_reviews     = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_reviews')
yearOverviews_medly_groups      = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_groups')
yearOverviews_medly_notes       = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_notes')
yearOverviews_medly_app_instapp   = detail_fb_abouts_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_app_instapp')

print(yearOverviews_medly_friends[0].text, ', ',
      yearOverviews_medly_photos[0].text, ', ',
      yearOverviews_medly_videos[0].text, ', ',
      yearOverviews_medly_map[0].text, ', ',
      yearOverviews_medly_sports[0].text, ', ',
      yearOverviews_medly_music[0].text
      )




, ', ',
      yearOverviews_medly_movies, ', ',
      yearOverviews_medly_tv, ', ',
      yearOverviews_medly_books, ', ',
      yearOverviews_medly_games, ', ',
      yearOverviews_medly_likes,', ',
      yearOverviews_medly_events,', ',
      yearOverviews_medly_reviews,', ',
      yearOverviews_medly_groups,', ',
      yearOverviews_medly_notes,', ',
      yearOverviews_medly_app_instapp
'''


# [개요]
detail_url_overview = 'https://www.facebook.com/kpokem/about?section=overview'
detail_fb_overview_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_overview)

about_overviewURL = '#pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div'

try:
    aboutOverview_middle_lists = detail_fb_overview_info_soup.select(about_overviewURL + ' > div:nth-of-type(1) > ul > li')
    # 개요 항목의 리스트 개수
    print('개요항목길이:', len(aboutOverview_middle_lists))

    # 개요 항목 리스트 추출
    for about_list in range(len(aboutOverview_middle_lists)):

        print(aboutOverview_middle_lists[about_list].text)
        # 여기서의 구체적인 값들은 '개요'가 아닌 각 큰 카테고리내에서 개별 선별 해야 함.

except Exception as e:
    print('개요 항목이 존재하지 않음.', e)

print('##############################################################')

try:
    aboutOverview_rightSide_lists = detail_fb_overview_info_soup.select(about_overviewURL + ' > div:nth-of-type(2) > ul > li')
    # 개요 항목 우측의 리스트 개수
    #print(len(aboutOverview_rightSide_lists))
    # 개요 항목 우측 리스트 추출
    for about_list_right in range(len(aboutOverview_rightSide_lists)):
        # 우측 리스트의 제목
        # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(1)
        title_aboutPage_list_right = detail_fb_overview_info_soup.select(
            about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type('+str(about_list_right+1)+') > div > div:nth-of-type(2) > span > div:nth-of-type(1)')

        # 우측 리스트의 내용
        # pagelet_timeline_medley_about > div:nth-of-type(2) > div > ul > li:nth-of-type(1) > div > div:nth-of-type(2) > div > div > div:nth-of-type(2) > ul > li > div > div:nth-of-type(2) > span > div:nth-of-type(2)
        contents_aboutPage_list_right = detail_fb_overview_info_soup.select(
            about_overviewURL + ' > div:nth-of-type(2) > ul > li:nth-of-type('+str(about_list_right+1)+') > div > div:nth-of-type(2) > span > div:nth-of-type(2)')


        #print(aboutOverview_rightSide_lists[about_list_right].text)
        print(title_aboutPage_list_right[0].text)
        print(contents_aboutPage_list_right[0].text)

except Exception as e:
    print('개요의 우측 항목이 존재하지 않음.', e)


# [경력 및 학력]
# https://www.facebook.com/kpokem/about?section=education
detail_url_education = 'https://www.facebook.com/kpokem/about?section=education'
detail_fb_education_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_education)
#about_educationURL = '#pagelet_eduwork > div > div'
aboutEducation_lists = detail_fb_education_info_soup.select('#pagelet_eduwork > div > div')
#print(len(aboutEducation_lists))

for about_length_of_education_list in range(len(aboutEducation_lists)):
    work_history_lists_title = detail_fb_education_info_soup.select('#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > div > span')[0].text

    print(work_history_lists_title) #직장/전문기술/학력

    if '전문 기술' in work_history_lists_title:

        #print(work_history_lists_title, '길이: 1')
        work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > ul > li > div'
        work_history_lists = detail_fb_education_info_soup.select(work_history_lists_dir)

        print(work_history_lists_title, '길이: ', len(work_history_lists))

        print(work_history_lists[0].text)

    else:
        #print('else:', len(aboutEducation_lists))
        work_history_lists_dir = '#pagelet_eduwork > div > div:nth-of-type(' + str(about_length_of_education_list + 1) + ') > ul > li'
        work_history_lists = detail_fb_education_info_soup.select(work_history_lists_dir)
        for about_length_of_edu_detail in range(len(work_history_lists)):

            print(work_history_lists_title,'길이: ', len(work_history_lists))
            print('@', detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > a')[0].text)

            print('@', detail_fb_education_info_soup.select(work_history_lists_dir + ':nth-of-type(' + str(
                about_length_of_edu_detail + 1) + ') div > div > div > div > div:nth-of-type(2) > div > div')[0].text)


#[거주했던 장소]
#https://www.facebook.com/kpokem/about?section=living
detail_url_living = 'https://www.facebook.com/kpokem/about?section=living'
detail_fb_living_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_living)
aboutLiving_lists = detail_fb_living_info_soup.select('#pagelet_hometown > div > div')

for about_length_of_living_list in range(len(aboutLiving_lists)):
    #print('about_length_of_living_list : ', about_length_of_living_list)
    living_history_lists_title = detail_fb_living_info_soup.select('#pagelet_hometown > div > div:nth-of-type(' + str(about_length_of_living_list + 1) + ') > div > span')[0].text

    print('living_history_lists_title : ', living_history_lists_title) #거주지와 출신지/기타 살았던 곳/거주지

    living_history_lists_dir = '#pagelet_hometown > div > div:nth-of-type(' + str(about_length_of_living_list + 1) + ') > ul > li'
    living_history_lists = detail_fb_living_info_soup.select(living_history_lists_dir)

    if '거주지' in living_history_lists_title:
        if len(living_history_lists) == 1:
            print('거주지 출력 부분은 구조가 1 depth 깊음')

            for about_length_of_living_detail in range(len(living_history_lists)):
                print('len(living_history_lists) : ', len(living_history_lists))
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)

        else:
            print('거주지 출력 부분은 구조가 1 depth 깊음')
            for about_length_of_living_detail in range(len(living_history_lists)):
                print('len(living_history_lists) : ', len(living_history_lists))
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)

    else:
        if len(living_history_lists) == 1:

            for about_length_of_living_detail in range(len(living_history_lists)):
                print('len(living_history_lists) : ', len(living_history_lists))
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ' > div > div > div > div > div:nth-of-type(2) > div')[0].text)

        else:
            for about_length_of_living_detail in range(len(living_history_lists)):
                print('len(living_history_lists) : ', len(living_history_lists))
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > span > a')[0].text)
                print(detail_fb_living_info_soup.select(living_history_lists_dir + ':nth-of-type(' + str(about_length_of_living_detail + 1) + ') > div > div > div > div > div > div:nth-of-type(2) > div')[0].text)




    # No.4 [연락처 및 기본정보]-연락처 정보, 웹사이트 및 소셜 링크 정보, 기본 정보
    # https://www.facebook.com/userpageID/about?section=contact-info
    detail_url_contact = 'https://www.facebook.com/kpokem/about?section=contact-info&pnref=about'
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
        #aboutDataDic[user_pglet_contactData_title_01.replace(" ", "")] = ''

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
                    #aboutDataDic[key] = value

                    #aboutInfo[key] = value
                    conCycle += 1

            except:
                print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                #print('연락처 정보 수집 결과[Dictionary type]:', aboutInfo)

    # [웹사이트 및 소셜 링크]란
    if not user_pglet_contactData_title_01_2:
        print('사용자가 웹사이트 및 소셜 링크 정보를 등록하지 않았습니다.')

        # make Data
        #aboutDataDic[user_pglet_contactData_title_01_2.replace(" ", "")] = ''
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
                    #aboutDataDic[key] = value

                    # aboutInfo[key] = value
                    conWebCycle += 1

            except:
                print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                #logger.debug('웹사이트 및 소셜 링크 정보 수집 결과[Dictionary type]: {}'.format(aboutDataDic))

    # [기본 정보]란 취득
    if not user_pglet_basicData_title_01:
        print('사용자가 기본 정보를 등록하지 않았습니다.')

        # make Data
        #aboutDataDic[user_pglet_basicData_title_01.replace(" ", "")] = ''

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
                    #aboutDataDic[key] = value

                    baseCycle += 1

            except:
                print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                #print('기본 정보 수집 결과 [Dictionary type]: {}'.format(aboutDataDic))




#[가족 및 결혼/연애 상태]
#https://www.facebook.com/kpokem/about?section=relationship
detail_url_relationship = 'https://www.facebook.com/kpokem/about?section=relationship'
detail_fb_relationship_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_relationship)
aboutRelationship_lists = detail_fb_relationship_info_soup.select('#pagelet_relationships > div')

for about_length_of_Relationships_list in range(len(aboutRelationship_lists)):

    try:
        #결혼/연애 상태
        relationship_marriage_status_title = detail_fb_relationship_info_soup.select('#pagelet_relationships > div:nth-of-type(' + str(about_length_of_Relationships_list + 1) + ') > div > span')[0].text
        print('relationship_marriage_status_title : ', relationship_marriage_status_title)

        relationship_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(about_length_of_Relationships_list + 1) + ') > ul > li'

        relationship_lists = detail_fb_relationship_info_soup.select(relationship_lists_dir)
        #print('##', len(relationship_lists))

        if len(relationship_lists) == 1:
            try:
                #결혼/연애상태의 대상자가 존재할 때
                relationship_list_name = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[0].text
                relationship_list_status = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[0].text
                print('relationship name & status : ', relationship_list_name, ', ',relationship_list_status )
            except Exception:
                # 결혼/연애상태의 대상자가 존재하지 않을 때
                relationship_list_name = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type(1) > div > div:nth-of-type(2) > div > div:nth-of-type(2) > span')[0].text
                print('relationship name : ', relationship_list_name)
        else:
            #결혼/연애상태의 대상자 수가 복수일 때
            for length_lists in range(len(relationship_lists)):
                relationship_list_name = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type('+ str(length_lists+1)+') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[0].text
                relationship_list_status = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type('+ str(length_lists+1)+') > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[0].text
                print('relationship name & status : ', relationship_list_name, ', ',relationship_list_status )


    except Exception:
        #가족
        relationship_family_status_title = detail_fb_relationship_info_soup.select('#pagelet_relationships > div:nth-of-type(' + str(about_length_of_Relationships_list + 1) + ') > div > div > span')[0].text
        print('relationship_family_status_title : ', relationship_family_status_title)

        relationship_lists_dir = '#pagelet_relationships > div:nth-of-type(' + str(about_length_of_Relationships_list + 1) + ') > div > ul > li'
        relationship_lists = detail_fb_relationship_info_soup.select(relationship_lists_dir)


        if len(relationship_lists) == 1:
            relationship_list_name = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > a')[0].text
            relationship_list_staus = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type(1) > div > div > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[0].text
            print('relationship name & status : ', relationship_list_name, ', ',relationship_list_status )
        else:
            for length_lists in range(len(relationship_lists)):
                relationship_list_name = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type('+ str(length_lists+1)+') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(1) > span > a')[0].text
                relationship_list_status = detail_fb_relationship_info_soup.select(relationship_lists_dir + ':nth-of-type('+ str(length_lists+1)+') > div > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div:nth-of-type(2)')[0].text
                print('relationship name & status : ', relationship_list_name, ', ',relationship_list_status )


#[자세한 소개]
#https://www.facebook.com/kpokem/about?section=bio
detail_url_bio = 'https://www.facebook.com/kpokem/about?section=bio'
detail_fb_bio_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_bio)

#bio와 Quotes는 기본으로 출력함
about_Bio_title = detail_fb_bio_info_soup.select('#pagelet_bio > div > div > span')[0].text        #누구누구님의 정보
about_Bio_contents = detail_fb_bio_info_soup.select('#pagelet_bio > div > ul > li > span')[0].text #내용 또는 표시할 추가 정보 없음
print('bio : ',about_Bio_title, ', ', about_Bio_contents)

try:
    about_Pronounce = detail_fb_bio_info_soup.select('#pagelet_pronounce')
except Exception as e:
    print('pagelet_pronounce 정보가 없습니다.')

try:
    about_nicknames = detail_fb_bio_info_soup.select('#pagelet_nicknames')
except Exception as e:
    print('pagelet_nicknames 정보가 없습니다. ')


#bio와 Quotes는 기본으로 출력함
about_Quotes_title = detail_fb_bio_info_soup.select('#pagelet_quotes > div > div > span')[0].text
about_Quotes_contents = detail_fb_bio_info_soup.select('#pagelet_quotes > div > ul > li > div > div > span')[0].text

print('quotes : ',about_Quotes_title, ', ', about_Quotes_contents)


#[중요 이벤트]
#https://www.facebook.com/kpokem/about?section=year-overviews
detail_url_yearOverviews = 'https://www.facebook.com/kpokem/about?section=year-overviews'
detail_fb_yearOverviews_info_soup = __getHTMLDoc_beautifulSoup4(driver, detail_url_yearOverviews)

yearOverviews_medly_about_title   = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > div > span')[0].text    #중요 이벤트
yearOverviews_medly_about_contents_lists   = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li')

for list_length in range(len(yearOverviews_medly_about_contents_lists)):

    yearOverviews_medly_about_contents_detail_01   = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type('+str(list_length+1)+') > div > div:nth-of-type(1) > span')[0].text   #년도
    yearOverviews_medly_about_contents_detail_list   = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type('+str(list_length+1)+') > div > div:nth-of-type(2) > ul > li')

    #print(len(yearOverviews_medly_about_contents_detail_list))

    for detail_list_length in range(len(yearOverviews_medly_about_contents_detail_list)):
        yearOverviews_medly_about_contents_detail_02 = detail_fb_yearOverviews_info_soup.select(
        '#timeline-medley > div > div#pagelet_timeline_medley_about > div > div > ul > li > div > div:nth-of-type(2) > div > div > ul > li:nth-of-type(' + str(
            list_length + 1) + ') > div > div:nth-of-type(2) > ul > li:nth-of-type('+str(detail_list_length+1)+') > div > div > a > span')[0].text  # 내용
        print(yearOverviews_medly_about_contents_detail_01,', ',yearOverviews_medly_about_contents_detail_02)

driver.close()



'''
#페이지 스크롤 하면 하단의 체크인 부분을 가져올 수 있음.
yearOverviews_medly_friends     = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_friends')
yearOverviews_medly_photos      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_photos')
yearOverviews_medly_videos      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_videos')
yearOverviews_medly_map         = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_map')
yearOverviews_medly_sports      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_sports')
yearOverviews_medly_music       = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_music')
yearOverviews_medly_movies      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_movies')
yearOverviews_medly_tv          = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_tv')
yearOverviews_medly_books       = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_books')
yearOverviews_medly_games       = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_games')
yearOverviews_medly_likes       = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_likes')
yearOverviews_medly_events      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_events')
yearOverviews_medly_reviews     = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_reviews')
yearOverviews_medly_groups      = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_groups')
yearOverviews_medly_notes       = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_notes')
yearOverviews_medly_app_instapp   = detail_fb_yearOverviews_info_soup.select('#timeline-medley > div > div#pagelet_timeline_medley_app_instapp')
'''













