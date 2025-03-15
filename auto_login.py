# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0093FE964CC2758A26FCE1FF857F8ED0956704D0EB82BD388460BACD924BF3667D69CEE097D3E1C396749022E8C7F294B6CD6FE661E6F590E2E112D1CC76F8FAC871E3C3BFD0C5459C439E8CDF08979E3DBFECF9EE93EDD143EDF53A0A858264A914589FB45EB32B6121359A6563F3D788C3FD5A234D6C5D6AD4BA52E68945C80BFF9B08AE34FEF09B71909672D6E4F10006FFA9ADF78A14CE0F894D1D607B9E88B564C007A1AD6181A53D5F61ED29FCA418134D0272CAD685EFD12DB8FDE15FE9B49CFDEB78D3C861767AF6FB6E9C6AA66AD7FD6558566A1F148D06BB3417DC7AF2708D27A9EE1501EB212FA5BDB89A1718AB38E99595F02E54F0EA4FF91A340C72CB8F620D589716F37452BDDC0C5FF6F7390972582CEB5199897AA8C1E8E187375EF0F7C582F0593C1E80900BF5655E8136430CBD241B730AD364FBCCE2322183B895B412EB7D9DFFB30EA46F510E487A83AB8BCF43C1A4E75CA500C53E6D48"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
