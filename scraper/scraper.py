# scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import init_db, save_item
from config import TARGET_URL
import time

class WebScraper:
    def __init__(self):
        # Set up Selenium WebDriver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        
        # Initialize database session
        self.db_session = init_db()
    
    def scrape(self):
        try:
            # Navigate to the target URL
            self.driver.get(TARGET_URL)
            
            # Wait for page to load (adjust selector as needed)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.content"))
            )
            
            # Example: Scrape some data (adjust selectors based on your target site)
            items = self.driver.find_elements(By.CSS_SELECTOR, "div.item")
            
            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, "h2.title").text
                    description = item.find_element(By.CSS_SELECTOR, "div.desc").text
                    url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    # Prepare data for database
                    item_data = {
                        'title': title,
                        'description': description,
                        'url': url
                    }
                    
                    # Save to database
                    save_item(self.db_session, item_data)
                    print(f"Saved item: {title}")
                    
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue
                
        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            self.close()
    
    def close(self):
        self.driver.quit()
        self.db_session.close()

if __name__ == "__main__":
    scraper = WebScraper()
    scraper.scrape()