# scrapers/prime_gaming_scraper.py

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
        filename='prime_gaming_scraper.log',
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG
    )
    logging.getLogger().addHandler(logging.StreamHandler())  # Also log to console


def incremental_scroll(driver, pause_time=3, max_scrolls=100):
    """
    Scrolls the page to load all dynamic content until no new content is loaded.
    
    :param driver: Selenium WebDriver instance
    :param pause_time: Time to wait after each scroll (in seconds)
    :param max_scrolls: Maximum number of scroll attempts to prevent infinite loops
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    logging.debug(f"Initial page height: {last_height}")

    for scroll in range(1, max_scrolls + 1):
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logging.debug(f"Scrolled to bottom: Attempt {scroll}/{max_scrolls}")
        time.sleep(pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        logging.debug(f"New page height after scroll {scroll}: {new_height}")

        if new_height == last_height:
            logging.debug("No new content loaded after scrolling. Ending scroll.")
            break
        last_height = new_height
    else:
        logging.warning(f"Reached maximum scroll attempts ({max_scrolls}) without exhausting content.")


def get_all_button_texts(driver):
    """
    Retrieves and logs all button texts on the page for debugging purposes.
    """
    buttons = driver.find_elements(By.TAG_NAME, "button")
    logging.info(f"Total buttons found: {len(buttons)}")
    for index, button in enumerate(buttons, start=1):
        try:
            text = button.text.strip()
            logging.debug(f"Button {index}: '{text}'")
        except Exception as e:
            logging.error(f"Error retrieving text for button {index}: {e}")


def dismiss_popups(driver):
    """
    Identifies and dismisses pop-ups like cookie consent forms or sign-in prompts.
    """
    try:
        # Dismiss cookie consent
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept') or contains(text(),'I Agree')]"))
        )
        consent_button.click()
        logging.debug("Dismissed cookie consent form.")
        time.sleep(2)
    except TimeoutException:
        logging.debug("No cookie consent form found.")
    except Exception as e:
        logging.error(f"Error dismissing cookie consent form: {e}")

    try:
        # Close sign-in prompt if any
        signin_close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Close') or contains(text(),'No Thanks')]"))
        )
        signin_close_button.click()
        logging.debug("Closed sign-in prompt.")
        time.sleep(2)
    except TimeoutException:
        logging.debug("No sign-in prompt found.")
    except Exception as e:
        logging.error(f"Error closing sign-in prompt: {e}")


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
    # Uncomment the next line to see the browser in action (for debugging)
    # options.add_argument("--headless")  
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
        logging.debug("Navigated to Prime Gaming homepage.")
        time.sleep(5)  # Allow initial page load

        # 3. Dismiss any pop-ups
        dismiss_popups(driver)

        # 4. Dynamic Scrolling
        incremental_scroll(driver, pause_time=3, max_scrolls=100)

        # 4a. Optional: Get all button texts for debugging
        # Uncomment the next line if you need to log all button texts
        # get_all_button_texts(driver)

        # 5. Save full page source for debugging
        with open('full_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        logging.debug("Saved full page source to 'full_page_source.html'")

        # 6. Locate all "Claim" buttons using data-a-target attribute
        claim_buttons = driver.find_elements(By.CSS_SELECTOR, "button[data-a-target='FGWPOffer']")
        logging.info(f"Found {len(claim_buttons)} 'Claim' buttons.")

        if not claim_buttons:
            logging.warning("No 'Claim' buttons found. The page structure might have changed.")
            return prime_freebies

        # 7. Iterate through each "Claim" button to extract game details
        for index, button in enumerate(claim_buttons, start=1):
            try:
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)  # Allow any lazy-loaded content to appear

                # Extract the game title from the aria-label attribute
                aria_label = button.get_attribute("aria-label")
                if not aria_label:
                    logging.debug(f"Button {index} has no aria-label. Skipping.")
                    continue
                game_title = aria_label.replace("Claim ", "").strip()

                # Extract the game link
                try:
                    parent_a = button.find_element(By.XPATH, ".//ancestor::a[@href]")
                    game_link = parent_a.get_attribute("href")
                    if not game_link.startswith("http"):
                        game_link = "https://gaming.amazon.com" + game_link
                except NoSuchElementException:
                    # If no ancestor <a> tag is found, use the main URL as a fallback
                    game_link = url
                    logging.debug(f"Unable to extract specific link for '{game_title}'. Using home URL as fallback.")

                # Avoid duplicates
                if game_title.lower() in seen_titles:
                    logging.debug(f"Duplicate found: {game_title}. Skipping.")
                    continue
                seen_titles.add(game_title.lower())

                # Append to the freebies list
                prime_freebies.append({
                    "title": game_title,
                    "link": game_link
                })

                logging.debug(f"#{index} FREEBIE: {game_title} | Link: {game_link}")

            except NoSuchElementException as e:
                logging.error(f"Error parsing game card #{index}: {e}")
                continue
            except StaleElementReferenceException as e:
                logging.error(f"StaleElementReferenceException for game card #{index}: {e}")
                continue
            except Exception as e:
                # Capture screenshot for debugging
                screenshot_name = f'error_card_{index}.png'
                driver.save_screenshot(screenshot_name)
                logging.error(f"Unexpected error parsing game card #{index}: {e}. Screenshot saved as '{screenshot_name}'")
                continue

    except TimeoutException:
        logging.error("Timeout: Prime Gaming page took too long to load or elements did not appear.")
    except Exception as ex:
        logging.error(f"Unexpected exception: {ex}")
    finally:
        driver.quit()

    logging.info(f"Found total of {len(prime_freebies)} freebies on Prime Gaming.\n")
    return prime_freebies


# Configure logging
setup_logging()


# Run the scraper locally for testing
if __name__ == "__main__":
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found (if any):")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
