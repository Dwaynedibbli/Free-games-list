import requests
from bs4 import BeautifulSoup

# Scrape GOG free games with 100% discount (originally paid)
def scrape_gog():
    url = "https://www.gog.com/games?sort=popularity&price=discounted"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    print("Scraping GOG for 100% discounted games...")

    for item in soup.find_all('div', class_='product-tile'):
        title = item.find('span', class_='product-title').text
        link = item.find('a', href=True)['href']
        discount_tag = item.find('span', class_='discount-tag')

        if discount_tag is not None and discount_tag.text.strip() == "-100%":
            games.append((title, "https://www.gog.com" + link))

    print(f"GOG games found: {games}")
    
    return games
