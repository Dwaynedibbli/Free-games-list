# scrapers/prime_gaming_scraper.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, StaleElementReferenceException
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
    print(f"\n[DEBUG] Navigating to: {url}\n")

    # 1. Set up Headless Chrome Options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
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
    seen_titles = set()  # To avoid duplicates

    try:
        # 2. Navigate to the Prime Gaming home page
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        # 3. Dynamic Scrolling: Scroll until no new games load
        scroll_pause_time = 3
        max_scroll_attempts = 30
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"[DEBUG] Scrolled to bottom: Attempt {scroll_attempts + 1}")
            # Wait to load page
            time.sleep(scroll_pause_time)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same, assume no more content
                print("[DEBUG] Reached end of page.")
                break
            last_height = new_height
            scroll_attempts += 1

        # 4. Wait for game cards to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-card-details"))
        )

        # 5. Locate all game cards
        game_cards = driver.find_elements(By.CSS_SELECTOR, "div.item-card-details")
        print(f"[DEBUG] Found {len(game_cards)} game cards with class 'item-card-details'.")

        # 6. Iterate through each game card
        for index, card in enumerate(game_cards, start=1):
            try:
                # (A) Check for the presence of the "Claim" button
                claim_button = card.find_element(By.CSS_SELECTOR, 'button[data-a-target="FGWPOffer"]')
                
                # (B) If found, extract the game title
                title_elem = card.find_element(By.CSS_SELECTOR, "h3.tw-amazon-ember-bold")
                game_title = title_elem.get_attribute("title").strip()

                # Avoid duplicates
                if game_title in seen_titles:
                    print(f"[DEBUG] Duplicate found: {game_title}. Skipping.")
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
                    # Secondary attempt: Find any nested <a> tag
                    try:
                        nested_a = card.find_element(By.CSS_SELECTOR, "a[href]")
                        game_link = nested_a.get_attribute("href")
                        if not game_link.startswith("http"):
                            game_link = "https://gaming.amazon.com" + game_link
                    except NoSuchElementException:
                        # Fallback: Use the main Prime Gaming URL
                        game_link = url
                        print(f"[DEBUG] No specific link found for '{game_title}'. Using home URL as fallback.")

                prime_freebies.append({
                    "title": game_title,
                    "link": game_link
                })

                print(f"[DEBUG] #{index} FREEBIE: {game_title} | Link: {game_link}")

            except NoSuchElementException:
                # If "Claim" button not found, it's not a free game
                continue
            except StaleElementReferenceException:
                # Handle cases where the DOM has changed during scraping
                print(f"[DEBUG] StaleElementReferenceException for card #{index}. Skipping.")
                continue
            except Exception as e:
                print(f"[DEBUG] Error parsing game card #{index}: {e}")
                continue

    except TimeoutException:
        print("[ERROR] Timeout: Prime Gaming page took too long to load or items did not appear.")
    except Exception as ex:
        print(f"[ERROR] Unexpected exception: {ex}")
    finally:
        driver.quit()

    print(f"\n[DEBUG] Found total of {len(prime_freebies)} freebies on Prime Gaming.\n")
    return prime_freebies

# Run the scraper locally for testing
if __name__ == "__main__":
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found (if any):")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
