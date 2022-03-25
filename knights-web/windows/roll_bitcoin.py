from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import pickle
url='https://freebitco.in/?op=signup_page#'
browser=webdriver.Chrome(r'C:\Users\simone\.wdm\drivers\chromedriver\win32\89.0.4389.23\chromedriver.exe')
browser.get(url)
one_hour=3600
email="salamander.d.natsu@gmail.com"
password="ryumille12"
logged=False
exist=False
if(not exist):
    while(not logged):
        try:
            # browser.find_element_by_class_name("login_menu_button active").click()
            # browser.find_element_by_name("LOGIN").click()
            browser.find_element_by_id("login_form_btc_address").send_keys(email)
            browser.find_element_by_id("login_form_password").send_keys(password)
            logged=True
        except:
            print("not logged")
    browser.find_element_by_id("login_button").click()
    pickle.dump(browser.get_cookies(), open("cookies.pkl", "wb"))
else:
    cookies = pickle.load(open("cookies.pkl", "rb"))
    print(cookies)
    for cookie in cookies:
        browser.add_cookie(cookie)
while(True):
    try:
        browser.find_element_by_class_name("close-reveal-modal").click()
    except:
        print("non trovo la x della pubblicità")
        time.sleep(2)
    try:
        # element=browser.find_element_by_id("free_play_sound")
        # if(not element==None):

        browser.find_element_by_xpath("/html/body/div[24]").click()
    except:
        print("non trovo vuoto")
        time.sleep(2)
    try:
        browser.find_element_by_id("play_without_captchas_button").click()
    except:
        print("non trovo il play_without_captchas_button")
        time.sleep(2)

    try:
        browser.find_element_by_id("free_play_form_button").click()
    except:
        print("non trovo il rerol_free_button")
        time.sleep(2)