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
    SCROLL_PAUSE_TIME = 0.5

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


user_fbpage_id = 'kpokem'


#영화 수 정보 추가
driver.get('https://www.facebook.com/' + user_fbpage_id + '/movies')

movies_html = driver.page_source
movies_soup = bs(movies_html, 'html.parser')

movies_data = []
movies_data_dic = {}

movies_data_dic['영화내용개수'] = 0
movies_data_dic['영화제목'] = '표시할 영화 없음'

try:

    movies_all_cnt = movies_soup.select(
        '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a')

    print('movies_all_cnt :', len(movies_all_cnt))

    if len(movies_all_cnt) is not 0:

        for moviesKindTitleLength in range(len(movies_all_cnt)):

            moviesKind_title = movies_soup.select(
                '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type('+ str(
                    moviesKindTitleLength + 1 ) + ') > span:nth-of-type(1)')[0].text

            moviesKind_cnt = movies_soup.select(
                '#pagelet_timeline_medley_movies > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > a:nth-of-type('+ str(
                    moviesKindTitleLength + 1 ) + ') > span:nth-of-type(2)')[0].text

            print(moviesKind_title, ':', moviesKind_cnt)


    movies_all_list = movies_soup.select('#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')

    print('movies_all_list: ', len(movies_all_list))

    if len(movies_all_list) is not 0:
        for moviesKindLgth in range(len(movies_all_list)):

            movies_title = movies_soup.select(
                '#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                    moviesKindLgth + 1) + ') > div > div:nth-of-type(1) > a')[0].text

            moviesSaw_date = movies_soup.select(
                '#pagelet_timeline_medley_movies > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                    moviesKindLgth + 1) + ') > div > div:nth-of-type(1) > div:nth-of-type(1) > a > div > abbr > span')[0].text

            print(movies_title, ':', moviesSaw_date)

            '''
            예시)
            '''

            movies_data.append(movies_title.replace(" ", "") + ':'+ moviesSaw_date.replace(" ",""))
            #print(events_data)

        #print('@'.join(events_data) )

        movies_data_dic['영화내용개수'] = len(movies_all_list)
        movies_data_dic['영화제목'] = '_@'.join(movies_data)

        print(movies_data_dic['영화내용개수'], ', ', movies_data_dic['영화제목'])


    else:
        print('표시할 영화 없음')

        movies_data_dic['영화내용개수'] = 0
        movies_data_dic['영화제목'] = '표시할 영화 없음'

except Exception as e:
    print('영화 정보가 공개되지 않았습니다. ')
