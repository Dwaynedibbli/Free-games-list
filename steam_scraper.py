import requests
from bs4 import BeautifulSoup

# Scrape Steam free games based on discounts (-100%)
def scrape_steam():
    url = "https://store.steampowered.com/search/?sort_by=Price_ASC&supportedlang=english&specials=1&ndl=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    print("Scraping Steam for discounted games...")

    for item in soup.find_all('a', class_='search_result_row'):
        title = item.find('span', class_='title').text
        link = item['href']
        discount_tag = item.find('div', class_='discount_pct')

        if discount_tag is not None and discount_tag.text.strip() == "-100%":
            games.append((title, link))

    print(f"Steam games found: {games}")
    
    return games
