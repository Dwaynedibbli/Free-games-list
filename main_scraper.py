from scrapers.steam_scraper import scrape_steam
from scrapers.gog_scraper import scrape_gog
from scrapers.epic_scraper import scrape_epic  # Import Epic scraper
from scrapers.save_to_file import save_to_file

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
    save_to_file(games_by_platform)

    # Correct path with proper capitalization for "Disclaimer.html"
    with open('styles/Disclaimer.html', 'r') as disclaimer_file:
        disclaimer_content = disclaimer_file.read()

    # Append the disclaimer to the end of the index.html file
    with open('index.html', 'a') as index_file:
        index_file.write(disclaimer_content)
