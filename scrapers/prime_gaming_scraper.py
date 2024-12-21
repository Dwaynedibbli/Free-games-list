# scrapers/prime_gaming_scraper.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException
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

    # Initialize WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    prime_freebies = []

    try:
        # 2. Navigate to the Prime Gaming home page
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        # 3. Scroll to load dynamic content
        for scroll_index in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            print(f"[DEBUG] Scrolled {scroll_index + 1} time(s).")

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
                
                # (C) Attempt to find a direct link (if available)
                # Note: Since there's no direct <a> tag, we'll use the main Prime Gaming URL
                # Alternatively, you can simulate a click to capture dynamic URLs
                game_link = url  # Placeholder link
                
                # (D) Append to the freebies list
                prime_freebies.append({
                    "title": game_title,
                    "link": game_link  # Modify if a specific link can be extracted
                })

                print(f"[DEBUG] #{index} FREEBIE: {game_title} | Link: {game_link}")

            except NoSuchElementException:
                # If "Claim" button not found, it's not a free game
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
