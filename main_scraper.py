from steam_scraper import scrape_steam, save_to_file

if __name__ == "__main__":
    steam_games = scrape_steam()

    # Create a dictionary with Steam games
    games_by_platform = {
        "Steam": steam_games
    }

    # Save the scraped data to index.html
    save_to_file(games_by_platform)
