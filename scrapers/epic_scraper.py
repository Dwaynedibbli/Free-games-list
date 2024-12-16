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
    free_games = []
    try:
        # Wait until the elements with the game class are present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Free Now")]'))
        )

        # Add sleep to ensure the content is loaded
        time.sleep(5)

        # Find all free game elements by the visible "Free Now" button
        games = driver.find_elements(By.XPATH, '//span[contains(text(), "Free Now")]/ancestor::a')

        # Loop through the games and extract title and link
        for game in games:
            try:
                title = game.text.strip()  # Directly extracting the text from the <a> element
                link = game.get_attribute('href')

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

    except TimeoutException:
        print("Page took too long to load or elements were not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

    return free_games

# Run the scraper
if __name__ == "__main__":
    scrape_epic()