from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException
)
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_google_play():
    """
    Scrapes discounted-to-free games from Google Play's 'On Sale' page.
    Filters by old != "$0.00" and new == "$0.00" and prints the full link.
    """

    # Set up headless Chrome options
    options = Options()
    options.add_argument("--headless")
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

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = "https://play.google.com/store/apps/collection/promotion_3002a18_gamesonsale?hl=en"
    print(f"Navigating to: {url}\n")

    discounted_free_games = []

    try:
        driver.get(url)
        time.sleep(5)  # Give the page time to load initial elements

        # Optional: attempt to click "I agree" if a cookie consent popup appears
        try:
            consent_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button//div[text()="I agree"]')
                )
            )
            consent_btn.click()
            time.sleep(3)
            print("[DEBUG] Clicked 'I agree' cookie popup.")
        except:
            print("[DEBUG] No cookie consent popup found.")

        # Scroll once to help reveal lazy-loaded elements
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Wait for <a class="Si6A0c Gy4nib"> anchors to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.Si6A0c.Gy4nib'))
        )

        # Find all anchor links for these games
        anchors = driver.find_elements(By.CSS_SELECTOR, 'a.Si6A0c.Gy4nib')
        print(f"[DEBUG] Found {len(anchors)} potential game anchors.\n")

        for anchor in anchors:
            # Extract the partial link
            partial_link = anchor.get_attribute("href")
            # Build the full link if it starts with "/store"
            if partial_link.startswith("/store"):
                link = "https://play.google.com" + partial_link
            else:
                link = partial_link

            try:
                old_price_elem = anchor.find_element(By.CSS_SELECTOR, 'span.JUF8md.ePXqnb')
                new_price_elem = anchor.find_element(By.CSS_SELECTOR, 'span.w2kbF.Q64Ric')
            except NoSuchElementException:
                # If we cannot find price elements, skip
                continue

            old_price = old_price_elem.text.strip()
            new_price = new_price_elem.text.strip()

            # Keep only if old != "$0.00" AND new == "$0.00"
            if old_price != "$0.00" and new_price == "$0.00":
                # Grab the title (e.g., <span class="sT93pb DdYX5 OnEJge ">)
                try:
                    title_elem = anchor.find_element(
                        By.XPATH,
                        './/span[contains(@class,"OnEJge")]'
                    )
                    title = title_elem.text.strip()
                except NoSuchElementException:
                    # If the above fails, fallback to any text in anchor
                    title = anchor.text.strip()

                discounted_free_games.append({
                    "title": title,
                    "old_price": old_price,
                    "new_price": new_price,
                    "link": link
                })

    except TimeoutException:
        print("ERROR: Timeout. The page took too long to load.")
    except Exception as ex:
        print(f"ERROR: An unexpected exception occurred: {ex}")
    finally:
        driver.quit()

    # Print results
    print(f"Found {len(discounted_free_games)} discounted-to-free games:")
    for idx, g in enumerate(discounted_free_games, start=1):
        print(f"{idx}. {g['title']} | Was {g['old_price']} → Now {g['new_price']} | Link: {g['link']}")

    return discounted_free_games

if __name__ == "__main__":
    scrape_google_play()
