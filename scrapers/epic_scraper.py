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
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-17st2kc'))
        )
    except TimeoutException:
        print("Page took too long to load.")
        driver.quit()
        return []

    # Add sleep to ensure the content is loaded
    time.sleep(5)

    # Find all free game elements
    games = driver.find_elements(By.CLASS_NAME, 'css-17st2kc')

    free_games = []

    # Loop through the games and extract title and link
    for game in games:
        try:
            link_element = game.find_element(By.CLASS_NAME, 'css-g3jcms')
            title_element = game.find_element(By.CLASS_NAME, 'eds_1ypbntd0')

            # Check if the game has a "Coming Soon" or "Free Next Week" status
            try:
                status_element = game.find_element(By.CLASS_NAME, 'css-82y1uz')
                status_text = status_element.text.strip().lower()
                if "coming soon" in status_text or "free next week" in status_text or "available" in status_text:
                    continue
            except:
                # If no "Coming Soon" status element found, proceed
                pass

            if link_element and title_element:
                title = title_element.text.strip()
                link = link_element.get_attribute('href')
                free_games.append({
                    'title': title,
                    'link': link
                })
        except Exception as e:
            print(f"Error processing a game: {e}")

    # Filter out games that have "Coming Soon" or "Free Next Week" in the title or status
    filtered_games = [game for game in free_games if not any(phrase in game['title'].lower() for phrase in ["coming soon", "free next week"])]

    # Print the extracted free games for debugging
    if filtered_games:
        for game in filtered_games:
            print(f"Title: {game['title']}, Link: {game['link']}")
    else:
        print("No free games found.")

    # Close the browser
    driver.quit()

    return filtered_games

# Run the scraper
if __name__ == "__main__":
    scrape_epic()
