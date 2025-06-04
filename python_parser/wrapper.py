import scraper

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def save_find_element(by: By, value: str): 
    try: 
        element = scraper.driver.find_element(by, value)
        return element
    except NoSuchElementException as e: 
        return None
    
def save_click(by: By, value: str):
    try: 
        item = scraper.driver.find_element(by, value)
        if item.is_displayed(): 
            item.click()
        else: 
            return False
        return True
    except NoSuchElementException as e: 
        return False
    except StaleElementReferenceException as e:
        return False
    
def save_send(by: By, value: str, text: str):
    try: 
        scraper.driver.find_element(by, value).send_keys(text)
        return True
    except NoSuchElementException as e: 
        return False
    
def exists(by: By, value: str):
    try: 
        scraper.driver.find_element(by, value)
        return True
    except NoSuchElementException as e: 
        return False
    
def exists_and_displayed(by: By, value: str):
    try: 
        element = scraper.driver.find_element(by, value)
        return element.is_displayed()
    except NoSuchElementException as e: 
        return False