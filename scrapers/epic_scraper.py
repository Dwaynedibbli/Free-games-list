import requests
from bs4 import BeautifulSoup

# Function to scrape currently free games from Epic Games Store
def scrape_epic():
    url = 'https://store.epicgames.com/en-US/free-games'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    games = []

    # Find all game containers with the free price
    game_tiles = soup.find_all('div', class_='css-1myhtyb')

    for tile in game_tiles:
        title_element = tile.find('span', class_='css-2ucwu')
        link_element = tile.find('a', class_='css-1jx3eyg')

        if title_element and link_element:
            title = title_element.text.strip()  # Extract title from text
            link = link_element['href']
            full_link = f"https://store.epicgames.com{link}"

            games.append({
                'title': title,
                'link': full_link
            })

    return games
