from scrapers.steam_scraper import scrape_steam
from scrapers.gog_scraper import scrape_gog
from scrapers.epic_scraper import scrape_epic
from scrapers.google_play_scraper import scrape_google_play  # Import Google Play scraper
from scrapers.prime_gaming_scraper import scrape_prime       # ← New Prime Gaming scraper
from scrapers.save_to_file import save_to_file
from datetime import datetime

if __name__ == "__main__":
    # Run the Steam scraper
    steam_games = scrape_steam()

    # Run the GOG scraper
    gog_games = scrape_gog()

    # Run the Epic scraper
    epic_games = scrape_epic()

    # Run the Google Play scraper
    google_play_games = scrape_google_play()

    # Run the Prime Gaming scraper
    prime_gaming_games = scrape_prime()

    # Ensure that Steam, GOG, Epic, Google Play, and Prime Gaming are always listed, 
    # even if no games are available
    games_by_platform = {
        "Steam": steam_games if steam_games else [],
        "GOG": gog_games if gog_games else [],
        "Epic": epic_games if epic_games else [],
        "Google Play": google_play_games if google_play_games else [],
        "Prime Gaming": prime_gaming_games if prime_gaming_games else []  # ← Add Prime Gaming
    }

    # Save the scraped data to index.html
    today = datetime.now().strftime("%B %d, %Y")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<html lang="en">\n<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        f.write('    <title>Free Today</title>\n')
        f.write('    <link rel="stylesheet" type="text/css" href="styles/style.css">\n')
        f.write('</head>\n<body>\n')

        # Title and Logo
        f.write('    <div class="title-container">\n')
        f.write('        <img src="styles/logo.png" alt="Logo" class="logo">\n')
        f.write('        <h1>Free Today</h1>\n')
        f.write('    </div>\n')

        # Two Column Layout
        f.write('    <div class="platform-container">\n')

        # Column 1 (Steam)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
        f.write('            </div>\n')
        f.write('            <h2>Steam</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Steam"]:
            for game in games_by_platform["Steam"]:
                title, link = game
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')
        f.write('        </div>\n')

        # Column 2 (GOG)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
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
        f.write('            </div>\n')
        f.write('        </div>\n')

        # Column 3 (Epic Games)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
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
        f.write('            </div>\n')
        f.write('        </div>\n')

        # Column 4 (Google Play Store)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
        f.write('            </div>\n')
        f.write('            <h2>Google Play Store</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Google Play"]:
            for game in games_by_platform["Google Play"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')
        f.write('        </div>\n')

        # Column 5 (Prime Gaming)
        f.write('        <div class="platform-column">\n')
        f.write('            <div class="banner-ad">\n')
        f.write('                <p>Banner Ad</p>\n')
        f.write('            </div>\n')
        f.write('            <h2>Prime Gaming</h2>\n')
        f.write('            <div class="game-list">\n')
        if games_by_platform["Prime Gaming"]:
            for game in games_by_platform["Prime Gaming"]:
                title = game['title']
                link = game['link']
                f.write(f'            <div class="game-item">\n')
                f.write(f'                <a href="{link}">{title}</a><br>\n')
                f.write('            </div>\n')
        else:
            f.write('            <p>No free games available today.</p>\n')
        f.write('            </div>\n')
        f.write('        </div>\n')

        f.write('    </div>\n')

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
