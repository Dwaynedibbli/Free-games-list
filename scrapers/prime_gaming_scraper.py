import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
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
    options.add_argument("--headless")  # Uncomment for debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36"
    )
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def incremental_scroll(driver, pause_time=3, max_scrolls=100):
    """
    Scrolls the page incrementally to load all dynamic content.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    for scroll in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            logging.debug(f"Reached the bottom of the page after {scroll + 1} scrolls.")
            break
        last_height = new_height
    else:
        logging.warning("Maximum scrolls reached without reaching the end of content.")


def dismiss_popups(driver):
    """
    Dismisses popups like cookie consent forms or sign-in prompts.
    """
    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept') or contains(text(),'I Agree')]"))
        ).click()
        logging.debug("Dismissed cookie consent popup.")
    except TimeoutException:
        logging.debug("No cookie consent popup found.")

    try:
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Close') or contains(text(),'No Thanks')]"))
        ).click()
        logging.debug("Dismissed sign-in popup.")
    except TimeoutException:
        logging.debug("No sign-in popup found.")


def scrape_prime():
    """
    Scrapes Prime Gaming freebies on Amazon's Prime Gaming page.
    Returns a list of dictionaries containing 'title' and 'link'.
    """
    url = "https://gaming.amazon.com/home"
    logging.debug(f"Navigating to: {url}")
    driver = initialize_driver()
    freebies = []

    try:
        driver.get(url)
        time.sleep(5)
        dismiss_popups(driver)
        incremental_scroll(driver)

        # Save page source for debugging
        with open("prime_gaming_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        logging.debug("Saved page source for debugging.")

        # Locate claimable games
        claim_buttons = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Claim')]")
        logging.info(f"Found {len(claim_buttons)} 'Claim' buttons.")

        for idx, button in enumerate(claim_buttons, start=1):
            try:
                # Scroll the button into view and extract the game info
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)

                aria_label = button.get_attribute("aria-label")
                if not aria_label:
                    logging.debug(f"No aria-label found for button {idx}. Skipping.")
                    continue
                game_title = aria_label.replace("Claim ", "").strip()

                # Locate the link to the game
                try:
                    parent_link = button.find_element(By.XPATH, ".//ancestor::a[@href]")
                    game_link = parent_link.get_attribute("href")
                except NoSuchElementException:
                    game_link = "https://gaming.amazon.com/home"
                    logging.warning(f"Could not find a link for game '{game_title}'.")

                freebies.append({"title": game_title, "link": game_link})
                logging.debug(f"Added freebie: {game_title} => {game_link}")

            except Exception as e:
                logging.error(f"Error processing button {idx}: {e}")

    except Exception as e:
        logging.error(f"Failed to scrape Prime Gaming: {e}")
    finally:
        driver.quit()

    logging.info(f"Total freebies found: {len(freebies)}")
    return freebies


if __name__ == "__main__":
    setup_logging()
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found:")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
