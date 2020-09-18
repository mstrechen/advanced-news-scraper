from functools import lru_cache
from selenium import webdriver


@lru_cache(maxsize=None)
def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(chrome_options=chrome_options)
