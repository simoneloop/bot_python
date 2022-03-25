from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By



# Replace below path with the absolute path
browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe')
phones=["393494398593"]
#"393275748248","393494398593","393276269769"
message = "messaggio di prova, a numero sconosciuto"
for phone in phones:
    url = "https://web.whatsapp.com/send?phone="+ phone + "&text=" + message + "&app_absent=1"
    browser.get(url)
    time.sleep(10)
    done=False
    while not done:
        try:
            sender=browser.find_elements(By.CLASS_NAME,"_4sWnG")[0]
            if(sender):
                sender.click()
                done=True
        except:
            browser.get(url)
            time.sleep(10)
            print("ancora non esiste,non sapendo ricarico")


# Close browser
browser.close()