from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_epic():
    # Set up Chrome options to run headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")

    # Set up the Chrome WebDriver with the options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the Epic Games Store Free Games page
    driver.get("https://store.epicgames.com/en-US/free-games")

    # Wait for the page to load
    try:
        # Wait until the elements with the game class are present
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-2mlzob'))
        )
    except TimeoutException:
        print("Page took too long to load.")
        driver.quit()
        return []

    # Add sleep to ensure the content is loaded
    time.sleep(5)

    # Debugging: Print the page source to see if the elements are available
    print(driver.page_source)

    # Find all free game elements
    games = driver.find_elements(By.CLASS_NAME, 'css-2mlzob')

    free_games = []

    # Loop through the games and extract title and link
    for game in games:
        try:
            link_element = game.find_element(By.TAG_NAME, 'a')
            title_element = game.find_element(By.TAG_NAME, 'h6')

            # Skip games that are "Coming Soon"
            if "Coming Soon" in game.text:
                continue

            if link_element and title_element:
                title = title_element.text.strip()
                link = link_element.get_attribute('href')
                free_games.append({
                    'title': title,
                    'link': link
                })
        except Exception as e:
            print(f"Error processing a game: {e}")

    # Print the extracted free games for debugging
    if free_games:
        for game in free_games:
            print(f"Title: {game['title']}, Link: {game['link']}")
    else:
        print("No free games found.")

    # Close the browser
    driver.quit()

    return free_games
