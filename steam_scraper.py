import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Scrape Steam free games based on discounts (-100%)
def scrape_steam():
    url = "https://store.steampowered.com/search/?sort_by=Price_ASC&supportedlang=english&specials=1&ndl=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = []
    
    # Debug: Print the HTML of the Steam page
    print("Scraping Steam for discounted games...")

    # Find all games by looking for 'search_result_row' class
    for item in soup.find_all('a', class_='search_result_row'):
        title = item.find('span', class_='title').text
        link = item['href']
        discount_tag = item.find('div', class_='discount_pct')

        # Ensure the discount_tag exists and check if it's a -100% discount
        if discount_tag is not None:
            discount_text = discount_tag.text.strip()
            print(f"Found game: {title}, Discount: {discount_text}")  # Debugging print

            if discount_text == "-100%":
                games.append((title, link))
    
    # Debug: Print the scraped Steam games
    print(f"Steam games found: {games}")
    
    return games

# Save the scraped data to the index.html file
def save_to_file(games_by_platform):
    today = datetime.now().strftime("%B %d, %Y")
    
    # Use UTF-8 encoding to handle special characters
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <style>\n')
        f.write('        body {background-color: black; color: green; font-family: monospace;}\n')
        f.write('        h1 {text-align: center;}\n')
        f.write('        .game-list {margin: 20px;}\n')
        f.write('        .game-list a {color: #00FF00; text-decoration: none;}\n')
        f.write('    </style>\n')
        f.write('</head>\n<body>\n')
        f.write(f'    <h1>Free Games Today</h1>\n')
        f.write('    <div class="game-list">\n')

        # Write the Steam games to the file
        f.write(f'        <h2>Steam</h2>\n')
        if games_by_platform["Steam"]:
            for title, link in games_by_platform["Steam"]:
                f.write(f'        <a href="{link}">{title}</a><br>\n')
        else:
            f.write('        <p>No free games available today.</p>\n')

        f.write('    </div>\n')
        f.write(f'    <footer style="text-align: center; margin-top: 20px;">\n')
        f.write(f'        <p>Generated on {today}</p>\n')  # Ensure the date is included
        f.write('    </footer>\n')
        f.write('</body>\n</html>')

# Main function to run the scraper and save the data
if __name__ == "__main__":
    steam_games = scrape_steam()

    # Create a dictionary with the platform and the games
    games_by_platform = {
        "Steam": steam_games
    }

    # Save the scraped data to index.html
    save_to_file(games_by_platform)
