import requests
from bs4 import BeautifulSoup

# Scrape GOG always-free games
def scrape_gog_always_free():
    url = "https://www.gog.com/en/partner/free_games"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    print("Scraping GOG for always-free games...")

    # Find all free games by looking for the class that indicates a free game
    for item in soup.find_all('div', class_='product-state__price-btn price-btn--free'):
        # Safely find the title and link
        title_tag = item.find_previous('span', class_='product-title')
        link_tag = item.find_previous('a', href=True)

        if title_tag and link_tag:  # Ensure the elements exist
            title = title_tag.text
            link = link_tag['href']
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

    # Find all discounted free games by looking for the "Free" label in the product price
    for item in soup.find_all('span', class_='product-price__free'):
        # Safely find the title and link
        title_tag = item.find_previous('span', class_='product-title')
        link_tag = item.find_previous('a', href=True)

        if title_tag and link_tag:  # Ensure the elements exist
            title = title_tag.text
            link = link_tag['href']
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
