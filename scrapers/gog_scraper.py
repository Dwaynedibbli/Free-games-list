import requests
from bs4 import BeautifulSoup

# Scrape GOG for always free and temporarily discounted free games
def scrape_gog():
    games = []

    # Scraping always-free GOG games
    always_free_url = 'https://www.gog.com/en/partner/free_games'
    response = requests.get(always_free_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    print("Scraping GOG always free games...")

    game_containers = soup.find_all('div', class_='product-state-holder')
    for game in game_containers:
        title = game.find('span', class_='product-title__text').text.strip()
        price_free = game.find('span', class_='product-state__is-free')
        if price_free:
            link = game.find('a', class_='product-row__link')['href']
            full_link = f"https://www.gog.com{link}"
            games.append((title, full_link))

    # Scraping temporarily free (discounted) GOG games
    discounted_free_url = 'https://www.gog.com/en/games?priceRange=0,0&discounted=true'
    response = requests.get(discounted_free_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    print("Scraping GOG temporarily free games...")

    game_tiles = soup.find_all('a', class_='product-tile')
    for tile in game_tiles:
        title_elem = tile.find('span', selenium_id='productTitle')
        price_elem = tile.find('span', selenium_id='productPriceFreeLabel')

        if title_elem and price_elem:
            title = title_elem.get_text(strip=True)
            link = tile['href']
            full_link = f"https://www.gog.com{link}"
            games.append((title, full_link))

    print(f"GOG games found: {games}")

    return games
