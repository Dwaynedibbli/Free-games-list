from scrapers.steam_scraper import scrape_steam
from scrapers.gog_scraper import scrape_gog
from scrapers.epic_scraper import scrape_epic  # Import Epic scraper
from scrapers.save_to_file import save_to_file
from datetime import datetime

if __name__ == "__main__":
    # Run the Steam scraper
    steam_games = scrape_steam()

    # Run the GOG scraper
    gog_games = scrape_gog()

    # Run the Epic scraper
    epic_games = scrape_epic()

    # Ensure that Steam, GOG, and Epic are always listed, even if no games are available
    games_by_platform = {
        "Steam": steam_games if steam_games else [],
        "GOG": gog_games if gog_games else [],
        "Epic": epic_games if epic_games else []  # Add Epic Games
    }

    # Save the scraped data to index.html
    today = datetime.now().strftime("%B %d, %Y")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Games Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Page title
        f.write(f'    <h1>Free Games Today</h1>\n')

        # Two Column Layout
        f.write('    <div class="platform-container">\n')

        # Column 1 (Steam)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')  # Placeholder for the banner ad
        f.write('            </div>\n')
        f.write('            <h2>Steam</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game  # Steam scraper uses tuple format
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of Steam game list
        f.write('        </div>\n')  # End of Steam column

        # Column 2 (GOG)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')  # Placeholder for the banner ad
        f.write('            </div>\n')
        f.write('            <h2>GOG</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["GOG"]:
            for game in games_by_platform["GOG"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of GOG game list
        f.write('        </div>\n')  # End of GOG column

        # Column 3 (Epic Games)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')  # Placeholder for the banner ad
        f.write('            </div>\n')
        f.write('            <h2>Epic Games</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Epic"]:
            for game in games_by_platform["Epic"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')  # End of Epic game list
        f.write('        </div>\n')  # End of Epic column

        f.write('    </div>\n')  # End of platform-container

        # Footer with date
        f.write('<footer>\n')
        f.write(f'    <p>Generated on {today}</p>\n')
        f.write('</footer>\n')

        f.write('</body>\n</html>')

    # Append the disclaimer from './styles/Disclaimer.html'
    with open('styles/Disclaimer.html', 'r') as disclaimer_file:
        disclaimer_content = disclaimer_file.read()

    # Append the disclaimer to the end of the index.html file
    with open('index.html', 'a') as index_file:
        index_file.write(disclaimer_content)
