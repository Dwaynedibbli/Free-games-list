import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_steam():
    url = "https://store.steampowered.com/search/?filter=free&sort_by=Released_DESC"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []
    
    for item in soup.find_all('a', class_='search_result_row'):
        title = item.find('span', class_='title').text
        link = item['href']
        if "Demo" not in title and "Soundtrack" not in title:
            games.append((title, link))
    return games

def scrape_epic():
    url = "https://www.epicgames.com/store/en-US/free-games"
    response = requests
