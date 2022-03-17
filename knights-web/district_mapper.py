import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os



URL_TUTTITALIA='https://www.tuttitalia.it/'

if __name__ == '__main__':
    browser = webdriver.Chrome(r'C:\Users\simone\Desktop\chromedriver.exe');
    browser.get(URL_TUTTITALIA);
    browser.find_element_by_xpath('//*[@id="cookieChoiceDismiss"]').click();
    tabella_regioni=browser.find_elements_by_xpath('//*[@id="ar"]/div/div[1]/dl')[0]
    rows=tabella_regioni.find_elements(By.TAG_NAME, "dt")

    for r in rows:
        print(r.text)# tutte le regioni
    for j in range(len(rows)):
        tabella_regioni = browser.find_elements_by_xpath('//*[@id="ar"]/div/div[1]/dl')[0]
        rows = tabella_regioni.find_elements(By.TAG_NAME, "dt")
        if(rows[j].text!="Valle d'Aosta"):
            file=open(rows[j].text+'.txt',"w")
            rows[j].click();
            time.sleep(1)
            done=False
            while(not done):
                try:
                    tabella_province=browser.find_element_by_xpath('//*[@id="jk"]/table[2]/tbody');
                    done=True;
                except:
                    print("popup")
            province=tabella_province.find_elements(By.TAG_NAME,"tr")

            province.pop(0)
            province.pop(len(province)-1)
            print("n-province:", len(province))
            for i in range(len(province)):

                tabella_province = browser.find_element_by_xpath('//*[@id="jk"]/table[2]/tbody');
                provincia = tabella_province.find_elements(By.TAG_NAME, "tr")[i+1]
                done = False
                while (not done):
                    try:
                        link=provincia.find_element(By.TAG_NAME,"a")
                        file.write(link.text.upper())
                        link.click();

                        done = True;

                    except:
                        print("un qualche errore")
                time.sleep(1)
                tabella_comuni=browser.find_element_by_xpath('//*[@id="jk"]/table/tbody');
                tabella_comuni=tabella_comuni.find_element(By.TAG_NAME,"tr");
                comuni=tabella_comuni.find_elements(By.TAG_NAME,"tr");
                print("inizio comuni: ");
                for item in comuni:
                    file.write("\n"+item.text)
                    print(item.text)# tutti i comuni
                print("per un totale di",len(comuni),"comuni")
                file.write("\n");
                file.write("\n");
                browser.back();
                time.sleep(1);
            file.close();
            browser.back();
            time.sleep(1);