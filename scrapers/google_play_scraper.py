from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_google_play():
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove this line if you want to see the browser window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
    
    # Added suggestions: Enable logging to debug potential issues
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--v=1')
    
    # Set up the Chrome WebDriver with the options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the Google Play Store Games on Sale page
    driver.get("https://play.google.com/store/apps/collection/promotion_3002a18_gamesonsale?hl=en")

    # Wait for the page to load
    try:
        # Wait until the elements with the game class are present
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Si6A0c'))
        )
    except TimeoutException:
        print("Page took too long to load.")
        driver.quit()
        return []

    # Added suggestion: Scroll function to dynamically load more games
    def scroll_page():
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(3)  # Adjust wait time as necessary

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Scroll down to load more games until no more new items are loaded
    scroll_page()

    # Find all free game elements
    games = driver.find_elements(By.CLASS_NAME, 'Si6A0c')

    free_games = []

    # Loop through the games and extract title, link, and price
    for game in games:
        try:
            link_element = game.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            title_element = game.find_element(By.CLASS_NAME, 'DdYX5').text.strip()
            price_elements = game.find_elements(By.CLASS_NAME, 'w2kbF')

            # Check if the game has a price of Free or $0.00
            if any(price_element.text.strip() in ["Free", "$0.00"] for price_element in price_elements):
                free_games.append({
                    'title': title_element,
                    'link': link_element
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

# Run the scraper
if __name__ == "__main__":
    scrape_google_play()
