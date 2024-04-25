import csv
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv
import random
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller as chromedriver



# Function to log in to LinkedIn
def login_to_feedly(email, password):
    chrome_driver_path = chromedriver.install()
    service = Service(chrome_driver_path)

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://feedly.com")

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "hs-eu-confirmation-button"))).click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="BaseButton_labelUppercase__G9aZP"]'))).click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[text()="Sign in with Email"]'))).click()

    # driver.find_element(By.NAME, "Sign in with Email").click()

    time.sleep(2)
    driver.find_element(By.ID, "login").send_keys(email)

    time.sleep(2)
    button = driver.find_element(By.XPATH, '//input[@class="button allow" and @value="Next"]')
    button.click()

    time.sleep(random.randint(5, 15))

    driver.find_element(By.ID, "password-input").send_keys(password)
    login_btn = driver.find_element(By.XPATH, '//input[@class="button allow" and @value="Login"]')
    login_btn.click()

    time.sleep(10)

    return driver


email = ''
password = ''
driver = login_to_feedly(email, password)


def write_posts_to_csv(posts, filename):
    cwd = os.getcwd()

    full_path = os.path.join(cwd, filename)

    with open(full_path, 'w', newline='') as csvfile:
        fieldnames = list(posts[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for post in posts:
            writer.writerow(post)


# result = scrape_linkedin_posts(driver, company_url)
# write_posts_to_csv(result, "linkedin_posts.csv")
# print(result)
# print(len(result))

driver.quit()