from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import subprocess
from selenium_stealth import stealth
#import undetected_chromedriver as uc
chrome_options = Options()

URL_OPERA = 'https://dantebus.com/concorsi/opera/189665';
chrome_options.add_argument("--headless")


options = Options()
# options.add_argument("start-minimized")
#options.add_argument("--headless")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)



while(True):
    try:
        #process = subprocess.Popen(["D:/bot_python/knights-web/windows/VPN.exe"])
        #time.sleep(5)
        service = Service(executable_path=ChromeDriverManager().install())
        #browser = webdriver.Chrome(service=service)
        browser = webdriver.Chrome(service=service, options=chrome_options)
        # stealth(browser,
        #         languages=["en-US", "en"],
        #         vendor="Google Inc.",
        #         platform="Win32",
        #         webgl_vendor="Intel Inc.",
        #         renderer="Intel Iris OpenGL Engine",
        #         fix_hairline=True,
        #         )
        browser.get(URL_OPERA);
        time.sleep(5)
        if(len(browser.find_elements(By.CLASS_NAME,"no-js"))>0):
            print("sono male")
            browser.close()
        coockie=browser.find_elements(By.CLASS_NAME,"iubenda-cs-accept-btn")
        if(coockie and len(coockie)>0):
            coockie[0].click()
            print("clicco cookie")
        time.sleep(5)
        popup=browser.find_elements(By.CLASS_NAME,"close-btn")
        if(popup and len(popup)>0):
            popup[0].click()
            print("clicco ads")
        time.sleep(5)

        try:

            browser.find_elements(By.TAG_NAME,"button")[0].click()
            print("clicco una volta")
            time.sleep(5)
            browser.find_elements(By.TAG_NAME, "button")[0].click()
            print("clicco due volte")
            time.sleep(5)
            browser.find_elements(By.TAG_NAME, "button")[0].click()
            print("clicco 3 volte")
            time.sleep(5)
        except:
            print("già votato")
        time.sleep(3)
        #process.terminate()
        browser.close()
    except:
        print("fallito")
        try:
            browser.close()
        except:
            print("non riesco a chiudere")

# options = uc.ChromeOptions()
#
#
# driver = uc.Chrome()
# driver.get( 'https://nowsecure.nl' )
# #options.headless = True
# while(True):
#     try:
#         #process = subprocess.Popen(["D:/bot_python/knights-web/windows/VPN.exe"])
#         #time.sleep(5)
#         service = Service(executable_path=ChromeDriverManager().install())
#         #browser = webdriver.Chrome(service=service)
#         browser = uc.Chrome(options=options)
#
#         browser.get(URL_OPERA);
#         time.sleep(5)
#
#         coockie=browser.find_elements(By.CLASS_NAME,"iubenda-cs-accept-btn")
#         if(coockie and len(coockie)>0):
#             coockie[0].click()
#             print("clicco cookie")
#         time.sleep(5)
#         popup=browser.find_elements(By.CLASS_NAME,"close-btn")
#         if(popup and len(popup)>0):
#             popup[0].click()
#             print("clicco ads")
#         time.sleep(5)
#
#         try:
#
#             browser.find_elements(By.TAG_NAME,"button")[0].click()
#             print("clicco una volta")
#             time.sleep(3)
#             browser.find_elements(By.TAG_NAME, "button")[0].click()
#             print("clicco due volte")
#             time.sleep(3)
#             browser.find_elements(By.TAG_NAME, "button")[0].click()
#             print("clicco 3 volte")
#             time.sleep(3)
#         except:
#             print("già votato")
#         time.sleep(3)
#         #process.terminate()
#         browser.close()
#     except:
#         print("fallito")
#         try:
#             browser.close()
#         except:
#             print("non riesco a chiudere")
#
