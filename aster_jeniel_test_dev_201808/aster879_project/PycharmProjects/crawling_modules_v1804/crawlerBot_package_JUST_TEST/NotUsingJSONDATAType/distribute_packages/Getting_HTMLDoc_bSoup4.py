#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

def __getHTMLDoc_beautifulSoup4(driver, URL):

    driver.get(URL)
    html_src_chrome = driver.page_source
    soupHTMLDoc = bs(html_src_chrome, 'html.parser')

    return soupHTMLDoc
