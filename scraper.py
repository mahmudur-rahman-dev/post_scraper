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
from sheets import SheetsService


def login_to_linkedin(email, password):
    chrome_driver_path = "/usr/bin/chromedriver"
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".btn__primary--large").click()

    time.sleep(15)

    return driver


def scrape_linkedin_posts(driver, company_url):
    driver.get(company_url)

    # Wait for the posts to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-shared-update-v2")))

    posts = []

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    post_containers = soup.find_all("div", class_="feed-shared-update-v2")
    for post in post_containers:
        post_content_elem = post.find("div", class_="feed-shared-update-v2__description-wrapper")

        if not post_content_elem:
            continue

        post_content = post_content_elem.get_text().strip()

        posts.append({
            "Post": post_content
        })
    return posts


email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

print(f"Email: {email}")
print(f"Password: {password}")

# company_url = "https://www.linkedin.com/company/accel-vc/posts/?feedView=all"
company_url = "https://www.linkedin.com/company/blackstonegroup/posts/?feedView=all"

driver = login_to_linkedin(email, password)


def write_posts_to_csv(posts, filename):
    cwd = os.getcwd()
    full_path = os.path.join(cwd, filename)

    with open(full_path, 'w', newline='') as csvfile:
        fieldnames = list(posts[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for post in posts:
            writer.writerow(post)


result = scrape_linkedin_posts(driver, company_url)
write_posts_to_csv(result, "linkedin_posts.csv")
# print(result)
print(len(result))

driver.quit()
