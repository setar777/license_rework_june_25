from selenium import webdriver

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from smart_open import open
import wrapper
import requests

import pymysql

driver: webdriver.Chrome

import time

current_question_id : str | None
database = {}
database_index = 0

def start():
    # check if video question 
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nScraper started...\n\n")
    input_value = ""
    print(pymysql.__version__)
    # get question id 
    global current_question_id 
    current_question_id = wrapper.save_find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qbasiclabel").get_attribute('innerHTML')
    print(current_question_id)
    database[current_question_id] = { "qid": database_index } 
    
    while input_value != "q":
        input_value = input("press q to quit (s for single page): ")
        continue
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if(input_value == "r"): 
            print(database)
            continue
        if(input_value != "s"): 
            continue
        
        
        if True and wrapper.exists_and_displayed(By.XPATH, "//button[contains(@class, 't24btnvideo')]"): 
            # video question 
            print("video question")
            video_checks()
            print("video checks completed " + current_question_id)
        
        if True and wrapper.exists_and_displayed(By.XPATH, "//img[contains(@id, 'app_TestingPage_CoreTestingDisplay_t24qpicimg')]"): 
            print("has thumbnail") 
            image_check()
            print("image check completed " + current_question_id)
        
        info_check()
        
        hint_check()
        
        point_check()
        
        question_check()
        
        answer_check()
        
        
        

def video_checks(): 
    # download thumbnail
    thumbnail_img = wrapper.save_find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qpicimg")
    if thumbnail_img is None: 
        print("thumbnail not found")
        return
    url = thumbnail_img.get_attribute('src')
    print('url: ' + url)
    try: 
        filename = url.replace("https://t24.theorie24.de/2025-01-v400/data/img/images/", "").replace("-", "_").replace(".", "_").replace("_jpg", ".jpg")
        img_data = requests.get(url).content
        with open("images/" + filename, "wb") as handler:
            handler.write(img_data)
    except Exception as e:
        print(e) 
        return None
    
    # video starten
    wrapper.save_click(By.XPATH, "//button[contains(@class, 't24btnvideo')]") 
    # get video 
    time.sleep(1)
    video = wrapper.save_find_element(By.XPATH, "//video[contains(@id, 'jp_video')]")
    
    video_url = video.get_attribute('src')
    filename = video_url.replace("https://www.theorie24.de/live_images/_current_ws_2024-10-01_2025-04-01/videos/", "").replace("-", "_").replace(".", "_").replace("_m4v", ".m4v")
    
    def stream_uri(uri_in, uri_out, chunk_size=1 << 18): 
        with open(uri_in, "rb") as fin, open(uri_out, "wb") as fout:
            while chunk := fin.read(chunk_size):
                fout.write(chunk)
    
    stream_uri(video_url, "videos/" + filename)
    
    time.sleep(0.5)
    
    # video beenden
    wrapper.save_click(By.ID, "app_FullscreenVideoPage_appCoreVideoDisplayElement_btnClose")
    # zur aufgabenstellung
    time.sleep(1)
    wrapper.save_click(By.ID, "app_TestingPage_CoreTestingDisplay_t24videoskip")

    return True

def image_check(): 
    thumbnail_img = wrapper.save_find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qpicimg")
    if thumbnail_img is None: 
        print("thumbnail not found")
        return
    url = thumbnail_img.get_attribute('src')
    print('url: ' + url)
    try: 
        filename = url.replace("https://t24.theorie24.de/2025-01-v400/data/img/images/", "").replace("-", "_").replace(".", "_").replace("_jpg", ".jpg")
        img_data = requests.get(url).content
        with open("images/" + filename, "wb") as handler:
            handler.write(img_data)
    except Exception as e:
        print(e) 
        return None

def info_check(): 
    time.sleep(0.5)
    # get details 
    wrapper.save_click(By.XPATH, "//span[contains(@id, 'app_TestingPage_CoreTestingDisplay_t24qinfolabel1')]")
    time.sleep(0.2)
    infos = driver.find_elements(By.XPATH, "//div[contains(@class, 'msgBoxQuestionCategory')]")
    database[current_question_id]["details"] = []
    for i in infos: 
        database[current_question_id]["details"].append(i.get_attribute('innerHTML'))
    time.sleep(0.1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def hint_check():
    time.sleep(0.5)
    wrapper.save_click(By.ID, "app_TestingPage_CoreTestingDisplay_t24xlabel4x")
    time.sleep(0.5)
    test = driver.find_elements(By.XPATH, "//div[contains(@class, 'enyo-popup onyx-popup customalert')]")
    database[current_question_id]["hints"] = []
    for t in test: 
        try: 
            paragraphs = t.find_elements(By.TAG_NAME, "p")
            for p in paragraphs: 
                database[current_question_id]["hints"].append(p.get_attribute('innerHTML'))
        except Exception as e:
            pass
    time.sleep(0.1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def point_check():
    points = int(driver.find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qpointslabel").get_attribute('innerHTML').replace("Punkte: ", ""))
    database[current_question_id]['points'] = points

def question_check():        
    questionText = wrapper.save_find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qtext").get_attribute('innerHTML')
    database[current_question_id]['question'] = questionText

def answer_check():
    answerTable = driver.find_element(By.ID, "app_TestingPage_CoreTestingDisplay_t24qanswers")
    answerTexts = []
    answerDiv = answerTable.find_elements(By.CLASS_NAME, "t24atext")[0]
    answerSpan = answerDiv.find_elements(By.XPATH, "//span[contains(@id, 'answertext')]")
    checkboxes = answerDiv.find_elements(By.XPATH, "//div[contains(@style, 'assets/btn_optquestion_')]") # 
    for item in answerSpan:
        text = item.get_attribute('innerHTML')
        answerTexts.append(text)
        
    # only unique items
    assert len(checkboxes) == len(answerTexts) / 2
        
    answerMap = {}
    index = 0
    # create a for loop that iterates through every other item in the answersTexts list
    for i in range(0, len(answerTexts), 2):
        checked = checkboxes[index].get_attribute('style').__contains__("btn_optquestion_2.gif")
        answerMap[index] = { "text": answerTexts[i], "checked":  checked }
        index += 1
    
    database[current_question_id]['answers'] = answerMap    

        
def downloadImage(url, questionId): 
    print("Downloading url: " + url)
    try: 
        with open("images/" + questionId.replace(".", "_").replace("-", "_") + ".jpg", "wb") as handler:
            response = requests.get(url, stream=True)
            if not response.ok:
                print(response)
            for block in response.iter_content(1024):
                if not block:
                    break
            handler.write(block)
    except Exception as e:
        print(e) 
        return None
    return True



def clickButton(): 
    try: 
        button = driver.find_element(By.ID, id)
        button.click()
        driver.implicitly_wait(2)
    except: 
        print("Button not found")
        pass
    


