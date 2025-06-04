# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import init_db, save_item
from config import TARGET_URL, USER_EMAIL, USER_PASSWORD
import time

class WebScraper:
    def __init__(self):
        # Set up Selenium WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        
        self.wait = WebDriverWait(self.driver, 5)
        
        # Initialize database session
        self.db_session = init_db()
    
    def scrape(self):
        # open browser with url
        self.driver.get(TARGET_URL)
        
        if self.open_page() == None: 
            self.close()
            return
        
        if self.check_logged_in_state() == None:
            self.close()
            return 
        
        
        
        
        

        print("Success!")
        # programm closed successfully
        self.close()
        
    
    def check_logged_in_state(self): 
        result = self.check_for_element_clickable(By.XPATH, '//button[.//span[text()="Freischalten"]]')
        if result == None: 
            print("signed in")
            # user is already signed in
            return True
        else: 
            # user is not signed in
            print("not signed in")
            result.click()
            textField = self.check_for_element_located(By.CSS_SELECTOR, 'input.enyo-input.onyx-input#app_LoginPage_inputUserLastname')
            if textField == None:
                return False
            textField.send_keys(USER_EMAIL)
            textField = self.check_for_element_located(By.CSS_SELECTOR, 'input.enyo-input.onyx-input#app_LoginPage_inputUserMembershipNumber')
            if textField == None:
                return False
            textField.send_keys(USER_PASSWORD)
            
            button = self.check_for_element_clickable(By.XPATH, '//button[contains(text(), "Freischalten")]')
            if button == None:
                return False
            button.click()
            return True
    
    
    
    
    
    
    
    
    
    
    
    
    
    def close(self):
        input_value = input("press q to quit (s for single page): ")
        self.driver.quit()
        self.db_session.close()
        
        
    def check_for_element_located(self, by: str, value: str):
        try: 
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            print("element found")
            return element
        except Exception as e:
            print(f"Element not found within timeout period. {e}")
            return None
    
    def check_for_element_clickable(self, by: str, value: str):
        try: 
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            print("element found")
            return element
        except Exception as e:
            print(f"Element not found within timeout period. {e}")
            return None
       
    def open_page(self):
        try: 
            # ensure the page is loaded
            self.wait.until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            # Switch to iframe first
            iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
                
            # Wait for the title to verify the page
            self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.subtitle.t24h_sub#app_WelcomePage_PageHeader_subtitle')
                )
            )
            return True
        except Exception as e:
            print(f"Page was not loaded correctly.")
            return None
        

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape()