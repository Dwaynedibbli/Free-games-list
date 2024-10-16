from steam_scraper import scrape_steam, save_to_file
from gog_scraper import scrape_gog

if __name__ == "__main__":
    steam_games = scrape_steam()
    gog_games = scrape_gog()

    # Create a dictionary with both platforms
    games_by_platform = {
        "Steam": steam_games,
        "GOG": gog_games
    }

    # Save the scraped data to index.html
    save_to_file(games_by_platform)
