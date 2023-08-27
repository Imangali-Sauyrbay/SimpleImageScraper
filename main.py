from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from shutil import make_archive
import os
import urllib.parse
import re

DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
MIN_WIDTH = 720
DELAY = 30

query = urllib.parse.quote_plus(input('for search: '))
pages_input = input('page(number or number range 1-3): ').strip()
pages = []

while True:
    if re.match(r"^\d+-\d+$", pages_input) is not None:
        start, end = pages_input.split(sep="-")
        start = int(start)
        end = int(end)
        if (start < end):
            pages = [x for x in range(start, end + 1)]
            break
    if re.match(r"^\d+$", pages_input) is not None:
        pages.append(int(pages_input))
        break
    pages_input = input('page(number or number range 1-3) Input Valid Value!: ').strip()


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

urls = []
pics = []

for page in pages:
    driver.get(f"https://yandex.kz/images/search?p={page}&text={query}&wp=wh16x9_1920x1080&isize=wallpaper&from=tabbar&lr=221")
    results = WebDriverWait(driver, DELAY).until(
        expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[class="serp-item__link"')))
    for result in results:
        urls.append(result.get_attribute('href'))


def img_loaded(driver):
    try:
        element = driver.find_element(By.CLASS_NAME, "MMImage-Origin")
        if int(element.get_attribute('naturalWidth')) >= MIN_WIDTH:
            return element
    except NoSuchElementException:
        return False
    return False

fails = 0
for url in urls:
    driver.get(url)
    try:
        el = WebDriverWait(driver, DELAY).until(img_loaded)
        img_url = el.get_attribute('src')
        pics.append(img_url)
    except TimeoutException:
        fails += 1
        print(TimeoutException)
    print(f"{str(len(pics))}/{str(len(urls) - fails)}")


dest = input('enter output folder name: ')
directory = os.path.join(DESKTOP, dest)
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(len(pics)):
    with open(directory + '\\pic(' + str(i + 1) + ').jpg', 'wb') as handle:
        response = requests.get(pics[i], stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


if input('should make archive? (y/n): ').lower().startswith('y'):
    archive_name = os.path.expanduser(os.path.join('~', 'Desktop', input('enter output archive name: ')))
    root_dir = os.path.expanduser(os.path.join('~', 'Desktop', dest))
    make_archive(archive_name, 'zip', root_dir)

driver.quit()