# scrapers/prime_gaming_scraper.py

import os
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

def incremental_scroll(driver, pause_time=2, scroll_increment=1000, max_scrolls=100):
    """
    Scrolls the page incrementally to ensure all dynamic content loads.

    :param driver: Selenium WebDriver instance
    :param pause_time: Time to wait after each scroll (in seconds)
    :param scroll_increment: Number of pixels to scroll each time
    :param max_scrolls: Maximum number of scroll attempts to prevent infinite loops
    """
    last_height = driver.execute_script("return window.pageYOffset + window.innerHeight;")
    total_height = driver.execute_script("return document.body.scrollHeight;")
    
    for scroll in range(1, max_scrolls + 1):
        # Scroll down by the specified increment
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        logging.debug(f"Scrolled down by {scroll_increment} pixels: Scroll {scroll}/{max_scrolls}")
        time.sleep(pause_time)
        
        # Calculate new scroll position and total height
        new_scroll_position = driver.execute_script("return window.pageYOffset + window.innerHeight;")
        new_total_height = driver.execute_script("return document.body.scrollHeight;")
        
        logging.debug(f"Current Scroll Position: {new_scroll_position} | Total Page Height: {new_total_height}")
        
        # Check if we've reached the bottom of the page
        if new_scroll_position >= new_total_height:
            logging.debug("Reached the bottom of the page.")
            break
        
        # Log progress every 10 scrolls
        if scroll % 10 == 0:
            logging.info(f"Completed {scroll} scrolls out of {max_scrolls}")
    
    else:
        logging.warning(f"Reached maximum scroll attempts ({max_scrolls}) without exhausting content.")

def click_load_more(driver):
    """
    Clicks the 'Load More' button until it's no longer present.
    """
    while True:
        try:
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Load More') or contains(text(),'Show More')]"))
            )
            load_more_button.click()
            logging.debug("Clicked 'Load More' button.")
            time.sleep(2)  # Wait for content to load
        except TimeoutException:
            logging.debug("No more 'Load More' buttons found.")
            break
        except Exception as e:
            logging.error(f"Error clicking 'Load More' button: {e}")
            break

def dismiss_popups(driver):
    """
    Identifies and dismisses pop-ups like cookie consent forms or sign-in prompts.
    """
    try:
        # Dismiss cookie consent
        consent_button = WebDriverWait(driver, 5).until(
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
        # Close sign-in prompt
        signin_close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Close') or contains(text(),'No Thanks')]"))
        )
        signin_close_button.click()
        logging.debug("Closed sign-in prompt.")
        time.sleep(2)
    except TimeoutException:
        logging.debug("No sign-in prompt found.")
    except Exception as e:
        logging.error(f"Error closing sign-in prompt: {e}")

def login_amazon(driver, email, password):
    """
    Automates the Amazon login process.
    
    :param driver: Selenium WebDriver instance
    :param email: Amazon account email
    :param password: Amazon account password
    """
    try:
        driver.get("https://www.amazon.com/ap/signin")
        logging.debug("Navigated to Amazon sign-in page.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        ).send_keys(email)
        driver.find_element(By.ID, "continue").click()
        logging.debug("Entered email and clicked continue.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        ).send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()
        logging.debug("Entered password and submitted login form.")
        time.sleep(5)  # Wait for login to complete

        # Verify login by checking presence of account element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nav-link-accountList"))
        )
        logging.debug("Successfully logged into Amazon account.")
    except Exception as e:
        logging.error(f"Error during Amazon login: {e}")

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
    options.add_argument("--headless")
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
        # 2. Log in to Amazon
        email = os.getenv("AMAZON_EMAIL")
        password = os.getenv("AMAZON_PASSWORD")
        
        if not email or not password:
            logging.error("Amazon credentials not found. Please set AMAZON_EMAIL and AMAZON_PASSWORD as GitHub Secrets.")
            return prime_freebies
        
        login_amazon(driver, email, password)

        # 3. Navigate to Prime Gaming home page
        driver.get(url)
        logging.debug("Navigated to Prime Gaming homepage.")
        time.sleep(5)  # Allow initial page load

        # 4. Dismiss any pop-ups
        dismiss_popups(driver)

        # 5. Dynamic Scrolling
        incremental_scroll(driver, pause_time=3, scroll_increment=1000, max_scrolls=100)

        # 6. Handle "Load More" buttons if present
        click_load_more(driver)

        # 7. Save full page source for debugging
        with open('full_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        logging.debug("Saved full page source to 'full_page_source.html'")

        # 8. Wait for game cards to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.item-card-details"))
        )

        # 9. Locate all game cards
        game_cards = driver.find_elements(By.CSS_SELECTOR, "div.item-card-details")
        logging.info(f"Found {len(game_cards)} game cards with class 'item-card-details'.")

        # 10. Iterate through each game card
        for index, card in enumerate(game_cards, start=1):
            try:
                # (A) Check for the presence of the "Claim" button
                claim_button = card.find_element(By.XPATH, ".//button[contains(text(),'Claim')]")

                # (B) If found, extract the game title
                title_elem = card.find_element(By.CSS_SELECTOR, "h3.tw-amazon-ember-bold")
                game_title = title_elem.get_attribute("title").strip().lower()  # Normalize title

                # Avoid duplicates
                if game_title in seen_titles:
                    logging.debug(f"Duplicate found: {game_title}. Skipping.")
                    continue
                seen_titles.add(game_title)

                # (C) Extract the game link
                try:
                    parent_a = card.find_element(By.XPATH, ".//ancestor::a[@href]")
                    game_link = parent_a.get_attribute("href")
                    if not game_link.startswith("http"):
                        game_link = "https://gaming.amazon.com" + game_link
                except NoSuchElementException:
                    try:
                        nested_a = card.find_element(By.CSS_SELECTOR, "a[href]")
                        game_link = nested_a.get_attribute("href")
                        if not game_link.startswith("http"):
                            game_link = "https://gaming.amazon.com" + game_link
                    except NoSuchElementException:
                        try:
                            onclick_attr = claim_button.get_attribute("onclick")
                            match = re.search(r"window\.location\.href='(.*?)'", onclick_attr)
                            if match:
                                game_link = match.group(1)
                            else:
                                game_link = url  # Fallback
                        except Exception as e:
                            game_link = url
                            logging.debug(f"Unable to extract specific link for '{game_title}'. Using home URL as fallback.")

                # (D) Append to the freebies list
                prime_freebies.append({
                    "title": title_elem.text.strip(),
                    "link": game_link
                })

                logging.debug(f"#{index} FREEBIE: {title_elem.text.strip()} | Link: {game_link}")

            except NoSuchElementException:
                # If "Claim" button not found, it's not a free game
                continue
            except StaleElementReferenceException:
                # Handle cases where the DOM has changed during scraping
                logging.debug(f"StaleElementReferenceException for card #{index}. Skipping.")
                continue
            except Exception as e:
                # Capture screenshot for debugging
                screenshot_name = f'error_card_{index}.png'
                driver.save_screenshot(screenshot_name)
                logging.error(f"Error parsing game card #{index}: {e}. Screenshot saved as '{screenshot_name}'")
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
setup_logging()

# Run the scraper locally for testing
if __name__ == "__main__":
    prime_games = scrape_prime()
    print("\nPrime Gaming freebies found (if any):")
    for game in prime_games:
        print(f" - {game['title']} => {game['link']}")
