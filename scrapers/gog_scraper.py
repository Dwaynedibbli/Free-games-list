import requests
from bs4 import BeautifulSoup

# Scrape GOG always-free games
def scrape_gog_always_free():
    url = "https://www.gog.com/en/partner/free_games"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    print("Scraping GOG for always-free games...")

    # Find all game items by looking for 'product-tile' class
    for item in soup.find_all('div', class_='product-tile'):
        title = item.find('span', class_='product-title').text
        link = item.find('a', href=True)['href']
        games.append((title, "https://www.gog.com" + link))

    print(f"GOG always-free games found: {games}")
    return games

# Scrape GOG discounted-to-free games (looking for "Free" label)
def scrape_gog_discounted():
    url = "https://www.gog.com/en/games?priceRange=0,0&discounted=true"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    print("Scraping GOG for discounted-to-free games...")

    # Find all game items by looking for 'product-tile' class
    for item in soup.find_all('div', class_='product-tile'):
        title = item.find('span', class_='product-title').text
        link = item.find('a', href=True)['href']
        price_tag = item.find('span', class_='final-price')
        
        # Check if the price is listed as "Free"
        if price_tag and price_tag.text.strip().lower() == "free":
            games.append((title, "https://www.gog.com" + link))

    print(f"GOG discounted-to-free games found: {games}")
    return games

# Combined function to return both lists
def scrape_gog():
    always_free_games = scrape_gog_always_free()
    discounted_free_games = scrape_gog_discounted()

    # Combine the two lists of games
    all_gog_games = always_free_games + discounted_free_games
    return all_gog_games
