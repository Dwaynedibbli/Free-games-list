import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def setup_logging():
    """
    Sets up logging for the scraper.
    """
    logging.basicConfig(
        filename='prime_gaming_debug.log',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # Log to console as well


def initialize_driver():
    """
    Initializes the Selenium WebDriver with the necessary options.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def incremental_scroll(driver, pause_time=2, max_scrolls=50):
    """
    Incrementally scrolls the page to ensure all dynamic content is loaded.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    for scroll in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logging.debug("No more content to load after scrolling.")
            break
        last_height = new_height
    else:
        logging.warning("Max scrolls reached without exhausting content.")


def scrape_prime():
    """
    Scrapes Prime Gaming freebies and ensures no duplicate entries.
    """
    url = "https://gaming.amazon.com/home"
    logging.debug(f"Navigating to: {url}")

    driver = initialize_driver()
    freebies = {}

    try:
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        incremental_scroll(driver)

        # Locate claimable items
        claim_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Claim')]")
        logging.info(f"Found {len(claim_buttons)} 'Claim' buttons.")

        for button in claim_buttons:
            try:
                # Scroll to the button
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)

                # Extract game title from the button's aria-label
                aria_label = button.get_attribute("aria-label")
                if not aria_label:
                    continue
                game_title = aria_label.replace("Claim ", "").strip()

                # Find the link to the game
                parent_element = button.find_element(By.XPATH, "./ancestor::a[@href]")
                game_link = parent_element.get_attribute("href")

                # Add to the dictionary to avoid duplicates
                if game_title not in freebies:
                    freebies[game_title] = game_link
                    logging.debug(f"Added freebie: {game_title} => {game_link}")
                else:
                    logging.debug(f"Duplicate freebie skipped: {game_title}")

            except NoSuchElementException:
                logging.warning("Could not locate parent link for a button.")
                continue

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()

    logging.info(f"Total unique freebies found: {len(freebies)}")
    return [{"title": title, "link": link} for title, link in freebies.items()]


if __name__ == "__main__":
    setup_logging()
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found:")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
