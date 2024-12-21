from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_prime():
    # Initialize the WebDriver using ChromeDriverManager
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for GitHub Actions
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://gaming.amazon.com/home")
    time.sleep(5)  # Allow page to load

    free_games = []

    try:
        # Handle the cookie banner if it exists
        try:
            cookie_banner = driver.find_element(By.CSS_SELECTOR, "div[data-a-target='cookie-policy-banner']")
            if cookie_banner.is_displayed():
                close_button = cookie_banner.find_element(By.XPATH, ".//button")
                close_button.click()
                time.sleep(2)  # Wait for banner to disappear
        except Exception as e:
            print(f"No cookie banner found or unable to close: {e}")

        # Locate the free games tab and click
        free_games_tab = driver.find_element(By.XPATH, "//p[contains(text(), 'Free games')]")
        driver.execute_script("arguments[0].scrollIntoView();", free_games_tab)  # Ensure it's visible
        ActionChains(driver).move_to_element(free_games_tab).click().perform()
        time.sleep(3)  # Allow time for the games to load

        # Locate all game cards
        game_cards = driver.find_elements(By.CSS_SELECTOR, "div.item-card-details")
        
        for card in game_cards:
            try:
                # Extract the title
                title_element = card.find_element(By.CSS_SELECTOR, "h3.tw-bold")
                title = title_element.get_attribute("title")

                # Extract the link
                link_element = card.find_element(By.CSS_SELECTOR, "a[data-a-target='FGWPOffer']")
                link = link_element.get_attribute("href")

                # Add the game to the list
                free_games.append({"title": title, "link": link})
            except Exception as e:
                print(f"Failed to extract title or link for a game: {e}")

    except Exception as e:
        print(f"Error navigating to Free Games tab: {e}")

    finally:
        driver.quit()

    return free_games
