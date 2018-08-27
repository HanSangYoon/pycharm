import csv
import logging.handlers
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#https://www.facebook.com/hyoungwoo.kim.zermatt/about?lst=100006841668710


#현재시각 추출
currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)


#logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger('start_point_log')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

#fileHandler와 StreamHandler를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C://python_project/aster879_project/PycharmProjects/log/aster_sci_crawlerbot_logging_' + currTime, maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

#logging
logging.debug('start_point_log_crawler_module_debugging on' + currTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')

def login_facebook(userFacebookPageId, insertedUserName):
    start_time_all = time.time()

    returnValue_facebook = False

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {}
    prefs['profile.default_content_setting_values.notifications'] = 2
    chrome_options.add_experimental_option('prefs', prefs)
    driver_chrome = r"C:\python_project\aster879_project\PycharmProjects\chromedriver.exe"

    # go to Google and click the I'm Feeling Lucky button
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)

    # url
    driver.get('https://www.facebook.com')

    user_id = '821027746254'
    user_pass = '77882e2e'

    #김태호선임계정
    #user_id = 'idkimtheho@gmail.com'
    #user_pass = 'facP@ssw0rd'

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
                    driver.find_element_by_xpath('// *[ @ id = "u_0_d"]').click()
                    login_or_not = True
                except Exception as ex4:
                    print('로그인 버튼 id 값이 u_0_d 가 아닙니다.', ex4)

                    try:
                        driver.find_element_by_xpath('// *[ @ id = "u_0_b"]').click()
                        login_or_not = True
                    except Exception as ex5:
                        print('로그인 버튼 id 값이 u_0_b 가 아닙니다.', ex5)
                        login_or_not = False


    # calling next Function
    user_facebook_page_id = userFacebookPageId

    # for test user facebook page id
    directlyTypedUserName = insertedUserName

    #https://www.facebook.com/microscope83/about?
    driver.get('https://www.facebook.com/' + userFacebookPageId + '/about?' )
    returnResultDoc = autoScrollerInformationTAB(driver)
    logger.debug(returnResultDoc)


    end_time = time.time() - start_time_all
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)

    driver.close()




def autoScrollerInformationTAB(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    logger.debug(driver.current_url)

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 8):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')
    print('!@!@!@!@', autoScrolled_data_soup_html)

    try:
        time.sleep(2)

        medley_header_list = ['pagelet_timeline_medley_about', 'pagelet_timeline_medley_friends',
                              'pagelet_timeline_medley_map',
                              'pagelet_timeline_medley_photos', 'pagelet_timeline_medley_videos',
                              'pagelet_timeline_medley_sports', 'pagelet_timeline_medley_music',
                              'pagelet_timeline_medley_movies', 'pagelet_timeline_medley_tv',
                              'pagelet_timeline_medley_books', 'pagelet_timeline_medley_games',
                              'pagelet_timeline_medley_likes', 'pagelet_timeline_medley_fitness',
                              'pagelet_timeline_medley_groups', 'pagelet_timeline_medley_notes']

        cnt = 0
        for headerListLength in range(len(medley_header_list)):
            try:
                #검증용
                userContent_list_result = autoScrolled_data_soup_html.find_all('div', attrs={'id': medley_header_list[headerListLength]}).__doc__
                print('userContent_list_result :', userContent_list_result)

                acitivity_title = autoScrolled_data_soup_html.select('div#'+medley_header_list[headerListLength]+ ' > div:nth-of-type(1) > div:nth-of-type(1) > h3 > a')[0].text

                logger.debug('acitivity_title : {}'.format(acitivity_title))





                cnt += 1
            except Exception as e:
                logger.debug('{}가 없습니다.--> {}'.format(medley_header_list[headerListLength]), e)
        print('cnt :', cnt)

    except Exception as e:
        print('autoScrollerUserWrapperContents에서 userContentWrapper를 찾지 못했습니다. -> ', e)
        #userContent_list_result is None
        userContent_list_result = None

    return userContent_list_result




def autoScroller_MSCORE(User_site_url_addr, driver):
    driver.get(User_site_url_addr + '/photos_albums')

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    userContent_list_result = []

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup = bs(autoScrolled_data, 'html.parser')
        try:

            userContent_list_result = autoScrolled_data_soup.find_all('span', attrs={'class': '_2ieq _50f7'})
        except:
            print('해당 클래스 값이 없습니다.')

    pictureCntT = 0
    pictureCnt = 0
    for picture_index in userContent_list_result:
        pictureDiscribText = picture_index.text.split(' · ')

        matching = [s for s in pictureDiscribText if "항목" in s]
        pictureCnt = int(str(matching).split()[1].split('개')[0])

        pictureCntT += pictureCnt
    print('총 사진 수 : ', pictureCntT)

    return pictureCntT



#autoScroller관련 함수 =========================================================================

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')

    #return bs(autoScrolled_data, 'html.parser')
    return autoScrolled_data_soup_html



if __name__ == "__main__":

    login_facebook('microscope83', '한상윤')