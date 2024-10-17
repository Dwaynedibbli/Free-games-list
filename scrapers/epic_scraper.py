import requests
from bs4 import BeautifulSoup

# Function to scrape currently free games from Epic Games
def scrape_epic_free_games():
    url = 'https://store.epicgames.com/en-US/free-games'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    # Find all game containers
    game_tiles = soup.find_all('a', class_='css-1jx3eyg')
    print(f"Number of game tiles found: {len(game_tiles)}")

    for tile in game_tiles:
        title_element = tile.find('div', class_='css-16ukm6p')
        title = title_element.text.strip() if title_element else "Unknown Title"
        
        # Check if the game might be freemium or free-to-play
        if "free-to-play" in title.lower() or "freemium" in title.lower():
            continue  # Skip freemium or free-to-play games
        
        link = tile['href']
        full_link = f"https://store.epicgames.com{link}"

        games.append({
            'title': title,
            'link': full_link
        })

    return games
