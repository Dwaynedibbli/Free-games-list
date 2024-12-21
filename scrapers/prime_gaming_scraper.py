# scrapers/prime_gaming_scraper.py

import time
import re
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


def scrape_prime():
    """
    Scrapes Prime Gaming freebies on Amazon’s Prime Gaming page.
    Identifies free games by the presence of a "Claim" button.
    Returns a list of dictionaries with 'title' and 'link'.
    """
    url = "https://gaming.amazon.com/home"
    logging.debug(f"Navigating to: {url}")

    # 1. Set up Chrome Options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode; comment out for debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=AutomationControlled")
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

    prime_freebies = []
    seen_titles = set()  # To track unique game titles

    try:
        # 2. Navigate to Prime Gaming home page
        driver.get(url)
        time.sleep(5)  # Allow initial page load

        # 3. Handle "Load More" buttons if present (optional)
        # Uncomment and adjust if Prime Gaming uses "Load More" buttons
        """
        try:
            while True:
                load_more_button = driver.find_element(By.CSS_SELECTOR, 'button.load-more')
                load_more_button.click()
                logging.debug("Clicked 'Load More' button.")
                time.sleep(3)  # Wait for content to load
        except NoSuchElementException:
            logging.debug("No more 'Load More' buttons found.")
        """

        # 4. Dynamic Scrolling: Scroll until all games are loaded
        scroll_pause_time = 3
        max_scroll_attempts = 50  # Increased to ensure full page load
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logging.debug(f"Scrolled to bottom: Attempt {scroll_attempts + 1}")
            # Wait to load page
            time.sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, assume no more content
                logging.debug("Reached end of page.")
                break
            last_height = new_height
            scroll_attempts += 1

        # 5. Wait for game cards to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-card-details"))
        )

        # 6. Locate all game cards
        game_cards = driver.find_elements(By.CSS_SELECTOR, "div.item-card-details")
        logging.info(f"Found {len(game_cards)} game cards with class 'item-card-details'.")

        # 7. Iterate through each game card
        for index, card in enumerate(game_cards, start=1):
            try:
                # (A) Check for the presence of the "Claim" button
                claim_button = card.find_element(By.CSS_SELECTOR, 'button[data-a-target="FGWPOffer"]')

                # (B) If found, extract the game title
                title_elem = card.find_element(By.CSS_SELECTOR, "h3.tw-amazon-ember-bold")
                game_title = title_elem.get_attribute("title").strip()

                # Avoid duplicates
                if game_title in seen_titles:
                    logging.debug(f"Duplicate found: {game_title}. Skipping.")
                    continue
                seen_titles.add(game_title)

                # (C) Extract the game link
                # Primary attempt: Find a parent <a> tag
                try:
                    parent_a = card.find_element(By.XPATH, ".//ancestor::a[@href]")
                    game_link = parent_a.get_attribute("href")
                    if not game_link.startswith("http"):
                        game_link = "https://gaming.amazon.com" + game_link
                except NoSuchElementException:
                    # Secondary attempt: Find any nested <a> tag within the card
                    try:
                        nested_a = card.find_element(By.CSS_SELECTOR, "a[href]")
                        game_link = nested_a.get_attribute("href")
                        if not game_link.startswith("http"):
                            game_link = "https://gaming.amazon.com" + game_link
                    except NoSuchElementException:
                        # Tertiary attempt: Extract from 'onclick' attribute of the 'Claim' button
                        try:
                            onclick_attr = claim_button.get_attribute("onclick")
                            match = re.search(r"window\.location\.href='(.*?)'", onclick_attr)
                            if match:
                                game_link = match.group(1)
                            else:
                                game_link = url  # Fallback
                        except Exception as e:
                            # Fallback: Use the main Prime Gaming URL
                            game_link = url
                            logging.debug(f"Unable to extract specific link for '{game_title}'. Using home URL as fallback.")

                # (D) Append to the freebies list
                prime_freebies.append({
                    "title": game_title,
                    "link": game_link
                })

                logging.debug(f"#{index} FREEBIE: {game_title} | Link: {game_link}")

            except NoSuchElementException:
                # If "Claim" button not found, it's not a free game
                continue
            except StaleElementReferenceException:
                # Handle cases where the DOM has changed during scraping
                logging.debug(f"StaleElementReferenceException for card #{index}. Skipping.")
                continue
            except Exception as e:
                logging.error(f"Error parsing game card #{index}: {e}")
                continue

    except TimeoutException:
        logging.error("Timeout: Prime Gaming page took too long to load or items did not appear.")
    except Exception as ex:
        logging.error(f"Unexpected exception: {ex}")
    finally:
        driver.quit()

    logging.info(f"Found total of {len(prime_freebies)} freebies on Prime Gaming.\n")
    return prime_freebies


# Configure logging
logging.basicConfig(
    filename='prime_gaming_scraper.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

# Run the scraper locally for testing
if __name__ == "__main__":
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found (if any):")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
