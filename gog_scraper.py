import requests
from bs4 import BeautifulSoup

# Scrape GOG free games with 100% discount (originally paid)
def scrape_gog():
    url = "https://www.gog.com/games?sort=popularity&price=discounted"  # Adjusted URL to focus on discounts
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []
    
    # Debug: Print the HTML of the GOG page
    print("Scraping GOG for 100% discounted games...")

    # Find all game items by looking for 'product-tile' class
    for item in soup.find_all('div', class_='product-tile'):
        title = item.find('span', class_='product-title').text
        link = item.find('a', href=True)['href']
        price_tag = item.find('span', class_='price')
        discount_tag = item.find('span', class_='discount-tag')

        # Check if the game has a discount of 100%
        if discount_tag is not None and discount_tag.text.strip() == "-100%":
            original_price = item.find('span', class_='original-price').text if item.find('span', class_='original-price') else "Unknown"
            print(f"Found game: {title}, Original Price: {original_price}")  # Debugging print
            games.append((title, "https://www.gog.com" + link))

    # Debug: Print the scraped GOG games
    print(f"GOG games found: {games}")
    
    return games
