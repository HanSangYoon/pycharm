#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options




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
driver.get('https://www.daum.net/')

user_id = 'urkuni'
user_pass = 'Gkstkddbs2@'

# id and password
loginID = driver.find_element_by_class_name('lab_login.lab_id')
driver.execute_script('arguments[0].style="display: none;"', loginID)

driver.find_element_by_name('id').send_keys(user_id)


#
# driver.find_element_by_name('pass').send_keys(user_pass)
#
# # try login : 로그인 버튼의 id 값이 아래의 범위 내에서 무작위로 변경되기 때문에 이에 대한 대응차원임.
# try:
#     driver.find_element_by_xpath('// *[ @ id = "u_0_2"]').click()
#     login_or_not = True
# except Exception as ex1:
#     print('로그인 버튼 id 값이 u_0_2 가 아닙니다.', ex1)
#
#     try:
#         driver.find_element_by_xpath('// *[ @ id = "u_0_3"]').click()
#         login_or_not = True
#     except Exception as ex2:
#         print('로그인 버튼 id 값이 u_0_3 이 아닙니다.', ex2)
#
#         try:
#             driver.find_element_by_xpath('// *[ @ id = "u_0_4"]').click()
#             login_or_not = True
#         except Exception as ex3:
#             print('로그인 버튼 id 값이 u_0_4 가 아닙니다.', ex3)
#
#             try:
#                 driver.find_element_by_xpath('// *[ @ id = "u_0_b"]').click()
#                 login_or_not = True
#             except Exception as ex4:
#                 print('로그인 버튼 id 값이 u_0_b 가 아닙니다.', ex4)
#
#                 try:
#                     driver.find_element_by_xpath('// *[ @ id = "u_0_d"]').click()
#                     login_or_not = True
#                 except Exception as ex5:
#                     print('로그인 버튼 id 값이 u_0_d 가 아닙니다.', ex5)
#
#                     try:
#                         driver.find_element_by_xpath('// *[ @ id = "u_0_e"]').click()
#                         login_or_not = True
#                     except Exception as ex6:
#                         print('로그인 버튼 id 값이 u_0_e 가 아닙니다.', ex6)
#
#                         try:
#                             driver.find_element_by_xpath('// *[ @ id = "u_0_f"]').click()
#                             login_or_not = True
#                         except Exception as ex7:
#                             print('로그인 버튼 id 값이 u_0_f 가 아닙니다.', ex7)
#
#                             try:
#                                 driver.find_element_by_xpath('// *[ @ id = "u_0_a"]').click()
#                                 login_or_not = True
#                             except Exception as ex8:
#                                 print('로그인 버튼 id 값이 u_0_a 가 아닙니다.로그인 실패입니다. 소스를 다시 분석해야 합니다.', ex8)
#                                 login_or_not = False
