import os
import logging
import requests
import uuid
import datetime
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.db_config import get_db
from config.proxy_config import PROXY_URL, PROXY_USERNAME, PROXY_PASSWORD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_twitter_trends():
    """Scrape Twitter trends using Selenium."""
    # Securely fetch credentials
    USERNAME = os.getenv("TWITTER_USERNAME")
    PASSWORD = os.getenv("TWITTER_PASSWORD")
    if not USERNAME or not PASSWORD:
        logger.error("Twitter credentials are not set in environment variables.")
        return None

    # Configure Selenium to use ProxyMesh
    chrome_options = Options()
    chrome_options.add_argument(f"--proxy-server={PROXY_URL}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Uncomment for headless mode
    # chrome_options.add_argument("--headless")

    logger.info("Setting up Chrome WebDriver with ProxyMesh...")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to Twitter login page
        logger.info("Navigating to the Twitter login page...")
        driver.get("https://twitter.com/i/flow/login")

        # Enter username/email
        logger.info("Waiting for the username input...")
        username_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Phone, email, or username"]'))
        )
        username_input.send_keys(USERNAME)
        logger.info("Username entered.")

        # Click the "Next" button
        logger.info("Clicking the 'Next' button...")
        next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/..'))
        )
        next_button.click()

        # Enter password
        logger.info("Waiting for the password input...")
        password_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Password"]'))
        )
        password_input.send_keys(PASSWORD)
        logger.info("Password entered.")

        # Click the "Log in" button
        logger.info("Clicking the 'Log in' button...")
        login_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Log in"]/..'))
        )
        login_button.click()

        # Wait for successful login
        logger.info("Waiting for login to complete...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="Home"]'))
        )
        logger.info("Login successful!")

        # Scrape trending topics
        logger.info("Scraping 'Trending' section...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Timeline: Trending now"]'))
        )
        trends = driver.find_elements(By.XPATH, '//div[@aria-label="Timeline: Trending now"]//span')[:5]
        trend_names = [trend.text for trend in trends]
        logger.info("Trends scraped: %s", trend_names)

        # Fetch current proxy IP
        logger.info("Fetching current proxy IP...")
        try:
            ip_response = requests.get(
                "http://ipinfo.io", proxies={"http": PROXY_URL, "https": PROXY_URL}, timeout=10
            )
            ip_response.raise_for_status()
            current_ip = ip_response.json().get("ip", "Unknown")
            logger.info(f"Current IP using proxy: {current_ip}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching IP address: {e}")
            current_ip = "Unknown"

        # Save trends to database
        logger.info("Storing data in MongoDB...")
        db = get_db()
        unique_id = str(uuid.uuid4())
        data = {
            "_id": unique_id,
            "trends": trend_names,
            "timestamp": datetime.datetime.now(),
            "ip_address": current_ip,
        }
        db.trends.insert_one(data)
        logger.info("Data successfully saved to the database.")

        return data

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        logger.debug(traceback.format_exc())
        return None

    finally:
        driver.quit()
        logger.info("Driver quit.")

if __name__ == "__main__":
    trends_data = scrape_twitter_trends()
    if trends_data:
        logger.info("Trends data: %s", trends_data)
    else:
        logger.error("Failed to scrape trends.")
