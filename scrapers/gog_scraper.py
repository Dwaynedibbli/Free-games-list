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
        link = game.find('a', class_='product-row__link')['href']
        full_link = f"https://www.gog.com{link}"

        games.append((title, full_link))  # Match format to Steam scraper

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
        if title_element:
            title = title_element['title'].strip()  # Extract title from 'title' attribute
            link = tile['href']
            full_link = f"https://www.gog.com{link}"

            games.append((title, full_link))  # Match format to Steam scraper

    return games

# Function to combine both scrapers and return all GOG games
def scrape_gog():
    always_free_games = scrape_gog_always_free()
    discounted_free_games = scrape_gog_discounted_free()
    return always_free_games + discounted_free_games
