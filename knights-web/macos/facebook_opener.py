#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import xlsxwriter
import pandas as pd
import re
import asyncio
from selenium.webdriver.chrome.options import Options
browser = webdriver.Chrome("/Users/simonelopez/Documents/chromedriver/chromedriver");
facebook_url="https://it-it.facebook.com/"
email_="danyfilomarino@hotmail.it"

if __name__ == '__main__':
    browser.get(facebook_url)
    time.sleep(1)
    popup_btns=browser.find_elements(By.TAG_NAME,"button")
    #popup_btn=browser.find_elements(By.CLASS_NAME,"_42ft _4jy0 _9xo6 _4jy3 _4jy1 selected _51sy")
    time.sleep(2)
    print("popup",len(popup_btns))
    popup_btns[len(popup_btns)-2].click()
    time.sleep(1)
    data=browser.find_elements(By.CLASS_NAME,"_6lux")
    email=data[0].find_element(By.ID,"email")

    email.send_keys(email_)
    time.sleep(1)
    pswr=data[1].find_element(By.ID,"pass")
    pswr.send_keys("generata")
    time.sleep(1)
    btn=browser.find_elements(By.CLASS_NAME,"_6ltg")[0]
    btn.click()
    time.sleep(6)
