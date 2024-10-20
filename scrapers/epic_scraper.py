from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

def scrape_epic():
    # Set up Chrome options to run headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the Chrome WebDriver with the options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the Epic Games Store Free Games page
    driver.get("https://store.epicgames.com/en-US/free-games")

    # Wait for the page to load
    try:
        # Wait until the elements with the game class are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-2mlzob'))
        )
    except TimeoutException:
        print("Page took too long to load.")
        driver.quit()
        return []

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

    # Close the browser
    driver.quit()

    return free_games
