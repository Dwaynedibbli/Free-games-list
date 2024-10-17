import requests
from bs4 import BeautifulSoup

# Function to scrape always-free games from GOG
def scrape_gog_always_free():
    url = 'https://www.gog.com/en/partner/free_games'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    games = []

    # Find all game containers where the price is marked as free
    game_containers = soup.find_all('div', class_='product-state-holder')

    for game in game_containers:
        title = game.find('span', class_='product-title__text').text.strip()  # Extract game title
        price_free = game.find('span', class_='product-state__is-free')

        if price_free:
            link = game.find('a', class_='product-row__link')['href']
            full_link = f"https://www.gog.com{link}"

            games.append({
                'title': title,
                'link': full_link,
                'price': 'Free'
            })

    return games

# Function to scrape currently free discounted games from GOG
def scrape_gog_discounted_free():
    url = 'https://www.gog.com/en/games?priceRange=0,0&discounted=true'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    # Find all game containers with free price
    game_tiles = soup.find_all('a', class_='product-tile')

    for tile in game_tiles:
        title_element = tile.find('div', class_='product-tile__title')
        price_element = tile.find('span', class_='product-price__free')

        if title_element and price_element:
            title = title_element['title'].strip()  # Extract title from 'title' attribute
            link = tile['href']
            full_link = f"https://www.gog.com{link}"

            games.append({
                'title': title,
                'link': full_link,
                'price': 'Free'
            })

    return games

# Function to scrape all GOG games (both always-free and discounted-free)
def scrape_gog():
    gog_always_free_games = scrape_gog_always_free()
    gog_discounted_free_games = scrape_gog_discounted_free()
    all_free_games = gog_always_free_games + gog_discounted_free_games
    return all_free_games
