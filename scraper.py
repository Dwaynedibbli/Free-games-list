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
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []

    for item in soup.find_all('a', class_='css-1jx3eyg'):
        title = item.find('span', class_='css-2ucwu').text
        link = "https://www.epicgames.com" + item['href']
        if "Demo" not in title:
            games.append((title, link))
    return games

def scrape_gog():
    url = "https://www.gog.com/games?price=free"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []
    
    for item in soup.find_all('div', class_='product-tile'):
        title = item['data-title']
        link = "https://www.gog.com" + item.find('a')['href']
        if "Demo" not in title:
            games.append((title, link))
    return games

def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")
    
    # Write to index.html file
    with open('index.html', 'w') as f:  # Overwrite the file instead of appending
        f.write(f'<html><body>\n')
        f.write(f'<h1>Free Games for {today}</h1>\n')

        for platform, games in games_by_platform.items():
            f.write(f'<h2>{platform}</h2>\n')
            if games:
                for title, link in games:
                    f.write(f'<p><a href="{link}">{title}</a></p>\n')
            else:
                f.write(f'<p>No free games available on {platform} at this time.</p>\n')

        f.write('</body></html>\n')

if __name__ == "__main__":
    steam_games = scrape_steam()
    epic_games = scrape_epic()
    gog_games = scrape_gog()

    games_by_platform = {
        "Steam": steam_games,
        "Epic Games": epic_games,
        "GOG": gog_games
    }

    save_to_file(games_by_platform)
