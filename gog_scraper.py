import requests
from bs4 import BeautifulSoup

# Scrape GOG free games
def scrape_gog():
    url = "https://www.gog.com/games"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    # Debug: Print the HTML of the GOG page
    print("Scraping GOG for free games...")

    # Find all games (adjust this part based on how GOG displays free games)
    for item in soup.find_all('div', class_='product-tile'):
        title = item.find('span', class_='product-title').text
        link = item.find('a', href=True)['href']
        price_tag = item.find('span', class_='price')

        # Check if the game is free (adjust logic based on GOG's layout)
        if price_tag is not None and price_tag.text.strip() == "Free":
            games.append((title, "https://www.gog.com" + link))

    # Debug: Print the scraped GOG games
    print(f"GOG games found: {games}")

    return games
