# scrapers/prime_gaming_scraper.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_prime():
    """
    Scrapes Prime Gaming freebies (publicly visible) on Amazon’s Prime Gaming page
    WITHOUT a sign-in flow. Returns a list of dicts with 'title' and 'link'.
    """

    url = "https://gaming.amazon.com/home"
    print(f"[DEBUG] Navigating to {url}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    free_games = []

    try:
        driver.get(url)
        time.sleep(5)  # Let page elements load

        # Scroll once or multiple times if needed
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Wait for at least one card to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-card-details"))
        )

        # Grab all item-card containers
        cards = driver.find_elements(By.CSS_SELECTOR, "div.item-card-details")

        for card in cards:
            # Check for the 'free game' badge
            try:
                card.find_element(By.CSS_SELECTOR, '[data-a-target="badge-fgwp"]')
                # If we found this element, it's a free game
                is_free = True
            except NoSuchElementException:
                is_free = False

            if not is_free:
                continue

            # Title
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "h3.tw-amazon-ember-bold")
                title = title_elem.get_attribute("title").strip()
            except NoSuchElementException:
                title = "Unknown Title"

            # Link — no direct <a> if you're not signed in,
            # so we fallback to the main "Prime Gaming" URL or any other reference.
            link = url

            free_games.append({
                "title": title,
                "link": link
            })

    except TimeoutException:
        print("ERROR: Timeout. The page took too long or items did not appear.")
    except Exception as ex:
        print(f"ERROR: Unexpected issue: {ex}")
    finally:
        driver.quit()

    print(f"[DEBUG] Found {len(free_games)} freebies on Prime Gaming (no login).")
    for g in free_games:
        print(f" - {g['title']} | Link: {g['link']}")

    return free_games

if __name__ == "__main__":
    results = scrape_prime()
    print("\nPrime freebies found:")
    for game in results:
        print(f"{game['title']} -> {game['link']}")
