# scrapers/humble_choice_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import sys
import os

# Adjust the import path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .save_to_file import save_data

def scrape_humble_choice():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get("https://www.humblebundle.com/membership")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "js-discover-game-slide"))
        )

        game_carousel = driver.find_element(By.CLASS_NAME, "discover-games")
        games = game_carousel.find_elements(By.CLASS_NAME, "js-discover-game-slide")

        for game in games:
            driver.execute_script("arguments[0].scrollIntoView();", game)
            time.sleep(1)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        game_titles = soup.find_all("div", class_="js-discover-game-slide")

        unique_titles = set()
        for game in game_titles:
            title = game.find("div", class_="human-name")
            if title:
                game_name = title.get_text(strip=True)
                unique_titles.add(game_name)

        # Prepare data for saving
        data = [{"title": title, "link": "https://www.humblebundle.com/membership"} for title in unique_titles]
        save_data(data, 'humble_choice_games.json')

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_humble_choice()
