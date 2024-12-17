from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def scrape_google_play():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://play.google.com/store/apps/collection/promotion_3002a18_gamesonsale?hl=en")

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'Si6A0c')))
    except TimeoutException:
        print("Page took too long to load.")
        driver.quit()
        return []

    def scroll_page():
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(3):  # Adjust the range for more or fewer scrolls
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 3.5))  # Random sleep between scrolls
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    scroll_page()

    games = driver.find_elements(By.CLASS_NAME, 'Si6A0c')
    free_games = []
    for game in games:
        try:
            link_element = game.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            title_element = game.find_element(By.CLASS_NAME, 'DdYX5').text.strip()
            price_elements = game.find_elements(By.CLASS_NAME, 'w2kbF')

            if any(price_element.text.strip() in ["Free", "$0.00"] for price_element in price_elements):
                free_games.append({
                    'title': title_element,
                    'link': link_element
                })
        except Exception as e:
            print(f"Error processing a game: {e}")

    if free_games:
        for game in free_games:
            print(f"Title: {game['title']}, Link: {game['link']}")
    else:
        print("No free games found.")

    driver.quit()
    return free_games

if __name__ == "__main__":
    scrape_google_play()