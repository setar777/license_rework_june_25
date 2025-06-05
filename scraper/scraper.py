# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from database import init_db, save_item
from config import TARGET_URL
from selenium.webdriver.common.keys import Keys
from private import USER_EMAIL, USER_PASSWORD
from selenium.common.exceptions import StaleElementReferenceException
import time
import re 

class WebScraper:
    def __init__(self):
        # Set up Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=selenium")
        self.driver = webdriver.Chrome(options=chrome_options)
        #self.driver.maximize_window()
        
        self.wait = WebDriverWait(self.driver, 5)
        self.waitFast = WebDriverWait(self.driver, 1)
        
        # Initialize database session
        self.db_session = init_db()
    
    def scrape(self):
        # open browser with url
        self.driver.get(TARGET_URL)
        
        print("open_page()")
        if self.open_page() == None: 
            self.close()
            return
        print("check_logged_in_state()")
        if self.check_logged_in_state() == None:
            self.close()
            return 
            
        
        print("navigate to list")
        if(self.start_gefahrenlehre() == None):
            self.close()
            return 
        
        print("scraping")
        if(self.scraping() == None):
            self.close()
            return
            
        
        print("Success!")
        # programm closed successfully
        self.close()
        
    
    def scraping(self):
        # this starts inside the questions and runs recursivly until all questions are finished 
        data = { }
        #
        #
        #
        # Question
        element1 = self.check_for_element_located_string(By.XPATH, "//div[@id='app_TestingPage_CoreTestingDisplay_t24qtext']")
        if element1 == None: return None
        data["question_text"] = element1
        # Points 
        element2 = self.check_for_element_located_string(By.XPATH, "//div[@id='app_TestingPage_CoreTestingDisplay_t24qpointslabel']")
        if element2 == None: return None
        data["point_value"] = int(element2.replace("Punkte: ", "")) 
        # Question Identifier
        element3 = self.check_for_element_located_string(By.XPATH, "//div[@id='app_TestingPage_CoreTestingDisplay_t24qbasiclabel']")
        if element3 == None: return None
        data["question_uid"] = element3
        
        # Answers 
        # --- 1
        element4 = self.check_for_element_located_string(By.XPATH, "//span[@id='app_TestingPage_CoreTestingDisplay_t24answer1_answertext']")
        if element4 == None: return None
        data["answer_1_text"] = element4
        # --- 2
        element5 = self.check_for_element_located_string(By.XPATH, "//span[@id='app_TestingPage_CoreTestingDisplay_t24answer2_answertext']")
        if element5 == None: return None
        data["answer_2_text"] = element5
        # --- 3
        element6 = self.check_for_element_located_string(By.XPATH, "//span[@id='app_TestingPage_CoreTestingDisplay_t24answer3_answertext']")
        if element6 == None: return None
        data["answer_3_text"] = element6
    
        
        # click first answer and continue
        button1 = self.check_for_element_clickable(By.XPATH, "//*[@id='app_TestingPage_CoreTestingDisplay_t24answer1_control']")
        if button1 == None: return None
        button1.click()
        self.driver.implicitly_wait(2)
        button = self.check_for_element_clickable(By.XPATH, "//button[@id='app_TestingPage_CoreTestingDisplay_t24btnnext']")
        if button == None: return None
        button.click()
        self.driver.implicitly_wait(2)
        time.sleep(1)
    
        # hint button
        button = self.check_for_element_clickable(By.XPATH, "//div[@id='app_TestingPage_CoreTestingDisplay_t24xlabel4x']")
        if button == None: return None
        button.click()
        self.driver.implicitly_wait(2)
        # get hint 
        element7 =self.check_for_element_located(By.XPATH, "//div[@id='alert']")
        if(element7 == None): return None
        data["hint_text"] = element7.text.replace("\nOK", "").replace("Erklärung zur Frage\n", "")
        # close hint
        self.driver.implicitly_wait(2)
        body_element = self.driver.find_element(By.TAG_NAME, 'body')
        body_element.send_keys(Keys.ESCAPE)

        # get correct answers
        data["answer_1_value"] = self.check_correct("//div[@id='app_TestingPage_CoreTestingDisplay_t24answer1_t24qachkCorrect']")
        data["answer_2_value"] = self.check_correct("//div[@id='app_TestingPage_CoreTestingDisplay_t24answer2_t24qachkCorrect']")
        data["answer_3_value"] = self.check_correct("//div[@id='app_TestingPage_CoreTestingDisplay_t24answer3_t24qachkCorrect']")
        
        print(data)
        save_item(self.db_session, data)
        return True
    
    def check_correct(self, id: str):
        # get correct answers 
        x =self.check_for_element_located(By.XPATH, id)
        if(x == None): return None
        style = x.get_attribute("style")
        print(style)
        if style:
            match = re.search(r'background:\s*url\([\'"]?(.*?)\'?"\)', style)
            if match:
                image_url = match.group(1)
                return image_url == "./assets/corr_optquestion_2.gif"
            else:
                return False
        else: 
            return False
    
    def start_gefahrenlehre(self):
        print("Training")
        result = self.check_for_element_clickable(By.XPATH, '//button[.//span[text()="Training"]]')
        if result == None:
            return None
        result.click()
        print("Alle Fragen & Themen")
        result = self.check_for_element_clickable(By.XPATH, '//button[.//span[text()="Alle Fragen & Themen"]]')
        if result == None:
            return None
        result.click()
        print("Gefahrenlehre")
        result = self.check_for_element_clickable(By.XPATH, '//div[@id="app_ChapterPage_catTree_node_caption"][contains(., "Gefahrenlehre")]')
        if result == None:
            return None
        result.click()
        print("Filter")
        result = self.check_for_element_clickable(By.XPATH, "//button[@id='app_ChapterPage_t24selbtn1']")
        if result == None:
            return None
        result.click()
        print("Kein Filter - Alle Fragen")
        result = self.check_for_element_clickable(By.XPATH, "//button[@id='app_ChapterPage_filterQuestionSelector_btnFilterMode1']")
        if result == None:
            return None
        result.click()
        print("Fragen üben")
        result = self.check_for_element_clickable(By.XPATH, "//button[@id='app_ChapterPage_PageFooter_buttonchapterpractice']")
        if result == None:
            return None
        result.click()
        time.sleep(2)
        return True
    
      

    
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
        if(input_value == "r"):
            self.scraping()
            self.close()
        else:     
            self.driver.quit()
            self.db_session.close()
        
        
    def check_for_element_located(self, by: str, value: str):
        max_retries = 5
        for i in range(max_retries):
            try: 
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                return element
            except Exception as e:
                return None
            except StaleElementReferenceException as e:
                self.driver.implicitly_wait(0.5)
                if i == max_retries - 1:
                    return None
                
    def check_for_element_located_string(self, by: str, value: str):
        max_retries = 5
        for i in range(max_retries):
            try: 
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                return element.text
            except Exception as e:
                return None
            except StaleElementReferenceException as e:
                self.driver.implicitly_wait(0.5)
                if i == max_retries - 1:
                    return None
    
    def check_for_element_clickable(self, by: str, value: str):
        max_retries = 5
        for i in range(max_retries):
            try: 
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                return element
            except Exception as e:
                return None
            except StaleElementReferenceException as e:
                self.driver.implicitly_wait(0.5)
                if i == max_retries - 1:
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