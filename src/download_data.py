#!/usr/bin python3

# import packages
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# create service object
s = Service("/usr/local/bin/chromedriver")


# set driver specifics
options = webdriver.ChromeOptions()
prefs = {"download.default_directory":
"/Users/justinwilliams/projects/gun-violence/data"}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ['enable-logging'])
driver = webdriver.Chrome(service_log_path=s, options=options)

# specify url
url="https://www.gunviolencearchive.org/mass-shooting"

# set waittime
wait = WebDriverWait(driver, 10)

try:    
    # open browser
    driver.maximize_window()
    driver.get(url)

    # click export button
    export_xpath = '//*[@id="content"]/div/div/div/div[1]/ul/li[2]/a'
    export_button = wait.until(EC.element_to_be_clickable((By.XPATH, export_xpath)))
    export_button.click()

    # click download button
    dl_xpath = '//*[@id="block-system-main"]/div/a[1]'
    dl_button = wait.until(EC.element_to_be_clickable((By.XPATH, dl_xpath)))
    dl_button.click()

    # wait for download to comlete
    time.sleep(5)

except:
    print("something went wrong")



