# scrapers/google_play_scraper.py

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_logging():
    """
    Sets up logging for the scraper.
    """
    logging.basicConfig(
        filename='google_play_scraper.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console

def incremental_scroll(driver, pause_time=1, scroll_increment=1000, max_scrolls=100):
    """
    Scrolls the page incrementally to ensure all dynamic content loads.
    
    :param driver: Selenium WebDriver instance
    :param pause_time: Time to wait after each scroll (in seconds)
    :param scroll_increment: Number of pixels to scroll each time
    :param max_scrolls: Maximum number of scroll attempts to prevent infinite loops
    """
    last_height = driver.execute_script("return window.pageYOffset + window.innerHeight;")
    total_height = driver.execute_script("return document.body.scrollHeight;")
    
    for scroll in range(max_scrolls):
        # Scroll down by the specified increment
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        logging.debug(f"Scrolled down by {scroll_increment} pixels: Scroll {scroll + 1}/{max_scrolls}")
        time.sleep(pause_time)
        
        # Calculate new scroll position and total height
        new_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        new_total_height = driver.execute_script("return document.body.scrollHeight;")
        
        logging.debug(f"Current Scroll Position: {new_scroll_position} | Total Page Height: {new_total_height}")
        
        # Check if we've reached the bottom of the page
        if new_scroll_position >= new_total_height:
            logging.debug("Reached the bottom of the page.")
            break
        
        # Optional: Log progress
        if (scroll + 1) % 10 == 0:
            logging.info(f"Completed {scroll + 1} scrolls out of {max_scrolls}")
    
    else:
        logging.warning(f"Reached maximum scroll attempts ({max_scrolls}) without exhausting content.")

def dismiss_popups(driver):
    """
    Identifies and dismisses pop-ups like cookie consent forms or sign-in prompts.
    """
    try:
        # Example: Dismiss cookie consent
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
        )
        consent_button.click()
        logging.debug("Dismissed cookie consent form.")
        time.sleep(2)
    except TimeoutException:
        logging.debug("No cookie consent form found.")
    except Exception as e:
        logging.error(f"Error dismissing cookie consent form: {e}")

def scrape_google_play():
    """
    Scrapes free games from the Google Play Store.
    Returns a list of dictionaries with 'title' and 'link'.
    """
    url = "https://play.google.com/store/games/category/GAME"
    logging.debug(f"Navigating to: {url}")

    # 1. Set up Chrome Options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/110.0.5481.178 Safari/537.36"
    )
    # Additional options to make headless less detectable
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    free_games = []
    seen_titles = set()

    try:
        # 2. Navigate to Google Play Games category
        driver.get(url)
        logging.debug("Navigated to Google Play Games category.")
        time.sleep(5)  # Allow initial page load

        # 3. Dismiss any pop-ups
        dismiss_popups(driver)

        # 4. Dynamic Scrolling
        incremental_scroll(driver, pause_time=2, scroll_increment=1000, max_scrolls=100)

        # 5. Save full page source for debugging
        with open('full_page_source_google_play.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        logging.debug("Saved full page source to 'full_page_source_google_play.html'")

        # 6. Locate all game cards
        game_cards = driver.find_elements(By.XPATH, "//div[@role='listitem']")
        logging.info(f"Found {len(game_cards)} game cards.")

        # 7. Iterate through each game card
        for index, card in enumerate(game_cards, start=1):
            try:
                # (A) Extract game title
                title_elem = card.find_element(By.XPATH, ".//div[@class='WsMG1c nnK0zc']")
                game_title = title_elem.text.strip().lower()

                if game_title in seen_titles:
                    logging.debug(f"Duplicate found: {game_title}. Skipping.")
                    continue
                seen_titles.add(game_title)

                # (B) Extract game link
                link_elem = card.find_element(By.XPATH, ".//a[@href]")
                game_link = link_elem.get_attribute("href")

                free_games.append({
                    "title": title_elem.text.strip(),
                    "link": game_link
                })

                logging.debug(f"#{index} FREE GAME: {title_elem.text.strip()} | Link: {game_link}")

            except NoSuchElementException:
                continue
            except StaleElementReferenceException:
                logging.debug(f"StaleElementReferenceException for card #{index}. Skipping.")
                continue
            except Exception as e:
                screenshot_name = f'error_google_play_card_{index}.png'
                driver.save_screenshot(screenshot_name)
                logging.error(f"Error parsing game card #{index}: {e}. Screenshot saved as '{screenshot_name}'")
                continue

    except TimeoutException:
        logging.error("Timeout: Google Play Store page took too long to load or items did not appear.")
    except Exception as ex:
        logging.error(f"Unexpected exception: {ex}")
    finally:
        driver.quit()

    logging.info(f"Found total of {len(free_games)} free games on Google Play Store.\n")
    return free_games

# Configure logging
setup_logging()

# Run the scraper locally for testing
if __name__ == "__main__":
    games = scrape_google_play()
    print("\nGoogle Play Store freebies found (if any):")
    for game in games:
        print(f" - {game['title']} => {game['link']}")
