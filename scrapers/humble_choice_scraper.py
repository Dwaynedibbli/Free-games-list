# scrapers/humble_choice_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

URL = "https://www.humblebundle.com/membership"


def scrape_humble_choice():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    games = []
    seen = set()

    try:
        driver.get(URL)
        wait = WebDriverWait(driver, 25)
        carousel = wait.until(lambda d: d.find_element(
            By.CSS_SELECTOR, '[role="region"][aria-label="carousel"][data-choice-count]'
        ))
        expected = int(carousel.get_attribute("data-choice-count") or "0")
        print(f"Humble Choice reports {expected} games")

        # The carousel may render only four thumbnails at a time.
        # Selecting Next causes the visible buttons to update.
        max_steps = max(expected * 2, 12) if expected else 30
        for _ in range(max_steps):
            carousel = driver.find_element(
                By.CSS_SELECTOR, '[role="region"][aria-label="carousel"][data-choice-count]'
            )
            buttons = carousel.find_elements(By.CSS_SELECTOR, 'button[aria-label]')
            for button in buttons:
                title = (button.get_attribute("aria-label") or "").strip()
                if title and title not in seen:
                    seen.add(title)
                    games.append({"title": title, "link": URL})
                    print(f"Humble Choice: {title}")
            if expected and len(games) >= expected:
                break

            next_button = carousel.find_element(
                By.XPATH, './/button[.//span[normalize-space()="Next slide"]]'
            )
            before = tuple((b.get_attribute("aria-label") or "") for b in buttons)
            driver.execute_script("arguments[0].click();", next_button)
            try:
                wait.until(lambda d: tuple(
                    b.get_attribute("aria-label") or "" for b in
                    d.find_element(By.CSS_SELECTOR, '[role="region"][aria-label="carousel"][data-choice-count]')
                     .find_elements(By.CSS_SELECTOR, 'button[aria-label]')
                ) != before)
            except TimeoutException:
                print("Carousel did not advance; stopping")
                break

        print(f"Collected {len(games)} Humble Choice games")
        return games
    finally:
        driver.quit()


if __name__ == "__main__":
    print(scrape_humble_choice())
