from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils import img_loaded, make_archive
import os
import requests
import urllib.parse
import sys


DESKTOP = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
MIN_WIDTH = 720
DELAY = 20

query = urllib.parse.quote_plus(input('for search: '))
img_number = int(input('Number of Images: ').strip())
dest = input('enter output folder name: ')
directory = os.path.join(DESKTOP, dest)
if not os.path.exists(directory):
    os.makedirs(directory)


chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(f"https://yandex.kz/images/search?p={1}&text={query}&wp=wh16x9_1920x1080&isize=wallpaper&from=tabbar&lr=221")

result = WebDriverWait(driver, DELAY).until(
    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'a[class="serp-item__link"')))
result.click()

next_btn = WebDriverWait(driver, DELAY).until(
    expected_conditions.presence_of_element_located((By.CLASS_NAME, 'CircleButton_type_next')))

loaded = 0
attempts = 1

while loaded < img_number:
    try:
        el = WebDriverWait(driver, DELAY).until(img_loaded(MIN_WIDTH))
        img_url = el.get_attribute('src')

        img_path = directory + '\\pic(' + str(attempts) + ').jpg'

        while os.path.isfile(img_path):
            attempts += 1
            img_path = directory + '\\pic(' + str(attempts) + ').jpg'


        with open(img_path, 'wb') as handle:
            print("\n\nDownloading image %s" % str(loaded + 1))
            response = requests.get(img_url, stream=True)

            if not response.ok:
                print(response)

            total_length = response.headers.get('content-length')

            if total_length is None:  # no content length header
                handle.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for block in response.iter_content(1024):
                    if not block:
                        break

                    dl += len(block)
                    handle.write(block)
                    done_half = int(50 * dl / total_length)
                    done_full = int((dl / total_length) * 100)
                    offset = 1 if done_full == 100 else 2 if done_full > 9 else 3
                    sys.stdout.write("\r%s%s[%s>%s]" % (str(done_full) + '%', ' ' * offset, '=' * (done_half - 1), ' ' * (50 - done_half)))
                    sys.stdout.flush()


            loaded += 1

    except TimeoutException:
        print('\n')
        print(TimeoutException)
    finally:
        next_btn.click()
else:
    print('\n')

make_archive(dest)
driver.quit()
