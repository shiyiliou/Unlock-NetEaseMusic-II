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
    browser.add_cookie({"name": "MUSIC_U", "value": "0039AFD9F2F2FC0FD319C591E9665C6FBF9E64040A3683FAE9D2D461B275CB114534AE29BE8A2E3A0B3755E74CB1264C9AEE2886BB19EBD7DE93BAE1A04D0260CCA7294536DB8CFAE44D79F5C559149027F8C20E0A214AEF485C6E1D6BA1B3D1D80F45B12CF5B43C1ECFD460436773275FB3ECBE861470B33CD860964227B3A4D7F59D75E5427D2E352B712633E8A1EC19DD4AAFA4E5D1DFFF156FE9F2D649BC1EE7881161B71F05CEA1321F6D252E079AFE651E97F2ECD959A8B4C795488589B2BBF22BA02A23C4FE6C20968068357FEF01490BD9131420A8AD7F94502DE5FBBE9B017970CBBFE84EC044B11827CC12454E6495ACB91A2C51F729EF7E85F1539268041E2639846DDDCD0837C8B751F518C88A7BCC8323B5CF3E1F729C31DB7787C92608297C1004DCFE7D0678BA698BC79B82344CECF2BB0395CFD8610B2E4F866C3F69D3DB3D0D2BF735FF6480CD272977BA9D9800FE89830DC8405C7145A127"})
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
