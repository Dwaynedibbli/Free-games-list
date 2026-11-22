from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


def scrape_epic():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options,
    )
    free_games = []
    try:
        driver.get("https://store.epicgames.com/en-US/free-games")
        selector = 'a[data-discover="true"][aria-label*="Free Now"]'
        WebDriverWait(driver, 30).until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, selector)) > 0
        )

        seen = set()
        for game in driver.find_elements(By.CSS_SELECTOR, selector):
            try:
                title = game.find_element(By.CSS_SELECTOR, "h2").text.strip()
                link = game.get_attribute("href")
                if not title or not link or link in seen:
                    continue
                seen.add(link)
                free_games.append({"title": title, "link": link})
                print(f"Epic: {title} - {link}")
            except Exception as exc:
                print(f"Could not parse an Epic game: {exc}")
    except TimeoutException:
        print("Epic: timed out waiting for 'Free Now' game links; page structure or loading may have changed.")
    finally:
        driver.quit()

    print(f"Epic: found {len(free_games)} free-now games")
    return free_games


if __name__ == "__main__":
    scrape_epic()
