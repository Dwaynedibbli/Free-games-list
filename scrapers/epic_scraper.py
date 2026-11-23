from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

URL = 'https://store.epicgames.com/en-US/free-games'

def scrape_epic():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    games = []
    try:
        driver.get(URL)
        print('Epic URL:', driver.current_url)
        print('Epic title:', driver.title)
        section = WebDriverWait(driver, 45).until(
            lambda d: d.find_element(By.CSS_SELECTOR, 'section[aria-labelledby="free-games-heading"]')
        )
        WebDriverWait(driver, 20).until(
            lambda d: section.find_elements(By.CSS_SELECTOR, 'ul li a[href][aria-label]')
        )
        cards = section.find_elements(By.CSS_SELECTOR, 'ul li')
        print('Epic free-game section cards:', len(cards))
        seen = set()
        for card in cards:
            try:
                anchor = card.find_element(By.CSS_SELECTOR, 'a[href][aria-label]')
                label = anchor.get_attribute('aria-label') or ''
                status = card.find_element(By.CSS_SELECTOR, 'p[aria-hidden="true"]').text.strip()
                print('Epic candidate:', label, '| status:', status)
                if not status.lower().startswith('free now'):
                    continue
                title = anchor.find_element(By.CSS_SELECTOR, 'h2').get_attribute('textContent').strip()
                link = urljoin('https://store.epicgames.com', anchor.get_attribute('href'))
                if title and link not in seen:
                    seen.add(link)
                    games.append({'title': title, 'link': link})
            except Exception as exc:
                print('Epic card skipped:', type(exc).__name__, str(exc)[:200])
    except TimeoutException:
        print('Epic ERROR: free-game section did not load in time')
        print('Current URL:', driver.current_url)
        print('Page title:', driver.title)
        print('HTML contains free-games-heading:', 'free-games-heading' in driver.page_source)
        print('HTML contains Free Now:', 'Free Now' in driver.page_source)
    finally:
        driver.quit()
    print('Epic games found:', games)
    return games

if __name__ == '__main__':
    scrape_epic()
