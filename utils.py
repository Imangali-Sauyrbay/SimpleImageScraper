from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import os
import shutil

def img_loaded(MIN_WIDTH):
    def __(driver):
        try:
            element = driver.find_element(By.CLASS_NAME, "MMImage-Origin")
            if int(element.get_attribute('naturalWidth')) >= MIN_WIDTH:
                return element
        except NoSuchElementException:
            return False
        return False
    return __

def make_archive(dest):
    if input('should make archive? (y/n): ').lower().startswith('y'):
        archive_name = os.path.expanduser(os.path.join('~', 'Desktop', input('enter output archive name: ')))
        root_dir = os.path.expanduser(os.path.join('~', 'Desktop', dest))
        shutil.make_archive(archive_name, 'zip', root_dir)