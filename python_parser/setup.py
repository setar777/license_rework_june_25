
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
# import errors from selenium 
from selenium.common.exceptions import NoSuchElementException

import pickle
import time 

import scraper
import wrapper


def open_browser(): 
    # open browser 
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium")
    scraper.driver = webdriver.Chrome(options=chrome_options)
    try: 
        coockies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in coockies:
            scraper.driver.add_cookie(cookie)
        print("Cookies loaded")
    except FileNotFoundError:
        print("No cookies found")
        
    scraper.driver.implicitly_wait(1)
    scraper.driver.get("https://t24.theorie24.de/2025-01-v400/")
    scraper.driver.implicitly_wait(1)
    return

def setup(): 
    # open browser with cookies
    open_browser()
    
    return
    # switch to the iframe 
    iframe = wrapper.save_find_element(By.CSS_SELECTOR, "iframe") 
    if iframe is None:  
        print("e1: iframe not found")
        return
    scraper.driver.switch_to.frame(iframe)
    
    if wrapper.save_find_element(By.ID, "MainMenuContainer_button6") is None:
        # Training
        time.sleep(2)
        wrapper.save_click(By.ID, "MainMenuContainer_button")
        # Alle Fragen & Themen
        time.sleep(0.5)
        wrapper.save_click(By.ID, "MainMenuContainer_button8") 
        # Alle Fragen & Themen
        time.sleep(0.5)
        wrapper.save_click(By.ID, "app_ChapterPage_PageFooter_buttonchapterread") 
        # signed in
        scraper.start() 
    else:
        # not signed in 
        signIn()

        

def signIn(): 
    # locate unlock button and click
    if wrapper.save_click(By.ID, "MainMenuContainer_button6") is False:
        print("e2: unlock button not found")
        return
    
    if wrapper.save_send(By.ID, "app_LoginPage_inputUserLastname", "fdominik4@gmail.com") is False:
        print("e3: email field not found")
        return
    
    if wrapper.save_send(By.ID, "app_LoginPage_inputUserMembershipNumber", "Engel11@@") is False:
        print("e4: password field not found")
        return

    if wrapper.save_click(By.ID, "app_LoginPage_button") is False:
        print("e5: login button not found")
        return
    
    scraper.driver.implicitly_wait(2)
    
    pickle.dump(scraper.driver.get_cookies(), open("cookies.pkl", "wb"))
    print(scraper.driver.get_cookies())
    
    


setup()