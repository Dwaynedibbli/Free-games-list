from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_google_play():
    options = Options()
    # Recommended flags to help avoid issues in headless/CI environments:
    options.add_argument("--headless")  # or "--headless=new" (on newer Chrome versions)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-features=site-per-process")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/85.0.4183.121 Safari/537.36"
    )

    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    try:
        driver.get("https://play.google.com/store/apps/collection/promotion_3002a18_gamesonsale?hl=en")
        
        # Wait for the games to load on the page
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Si6A0c'))  # May need adjustment if DOM changes
        )
        
        # Extract game details
        games = driver.find_elements(By.CLASS_NAME, 'Si6A0c')
        free_games = []

        for game in games:
            title = game.find_element(By.CLASS_NAME, 'b8cIId').text.strip()  # Adjust if class name changes
            link = game.find_element(By.TAG_NAME, 'a').get_attribute('href')
            free_games.append({'title': title, 'link': link})

        # Output the results (debug print)
        for game in free_games:
            print(f"Title: {game['title']}, Link: {game['link']}")

    except TimeoutException:
        print("The page took too long to load or elements did not appear.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

    return free_games

if __name__ == "__main__":
    scrape_google_play()
