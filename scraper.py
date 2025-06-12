# Working code for text extraction from tweets

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import os

def get_stealth_driver():
    options = webdriver.ChromeOptions()
    
    # Essential stealth settings
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(110,115)}.0.0.0 Safari/537.36")
    
    # Remove automation indicators
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Remove webdriver flag
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        
        return driver
    except Exception as e:
        print(f"❌ Chrome setup failed: {e}")
        return None

def scrape_x_profile(username, max_tweets=500):
    driver = get_stealth_driver()
    driver.maximize_window()
    if not driver:
        return pd.DataFrame()
    
    try:
        print(f"🌐 Loading x.com/{username} (be patient - may take 1-2 minutes)...")
        driver.get(f"https://x.com/{username}")
        
        # Critical - extended random delay to appear human
        time.sleep(random.uniform(45, 75))
        
        # Check for blocking
        if "unsupported browser" in driver.page_source.lower():
            print("❌ X.com blocked the request - try these solutions:")
            print("1. MANUALLY login to x.com in Chrome first")
            print("2. Remove '--no-sandbox' flag")
            print("3. Run browser in non-headless mode")
            return pd.DataFrame()
        
        # Scroll and collect
        tweets = []
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        
        while len(tweets) < max_tweets and scroll_attempts < 10:
            tweet_elements = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//article[.//div[@data-testid="tweetText"]]'))
            )
            
            for tweet in tweet_elements[len(tweets):]:
                try:
                    text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                    if text and text not in tweets:
                        tweets.append(text)
                        if len(tweets) >= max_tweets:
                            break
                except:
                    continue
            
            # Human-like scrolling
            scroll_px = random.randint(800, 1200)
            driver.execute_script(f"window.scrollBy(0, {scroll_px})")
            time.sleep(random.uniform(3, 7))
            
            # Check if we've reached the end
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
            last_height = new_height
        
        if tweets:
            output_dir = "data/csv"
            
            # Build full file path
            file_path = os.path.join(output_dir, f"{username}_tweets.csv")
            df = pd.DataFrame(tweets, columns=['Text'])
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"✅ Success! Saved {len(df)} tweets to {file_path}")  # 👈 Updated path in message
            return df
        else:
            print("❌ No tweets found - possible reasons:")
            print("- Account is private")
            print("- X.com changed its HTML structure")
            print("- Need longer wait time")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)[:200]}...")
        return pd.DataFrame()
    finally:
        if driver:
            driver.quit()


#for testing purposes
if __name__ == "__main__":
    # Accounts likely to be public
    accounts = ["Cristiano","justinbieber","x", "XSupport", "elonmusk", "Snowden", "NatGeo"] 
    
    for account in accounts:
        print(f"\nAttempting @{account}...")
        result = scrape_x_profile(account)
        if not result.empty:
            print(f"📝 Sample tweet: {result.iloc[0]['Text'][:80]}...")
            break