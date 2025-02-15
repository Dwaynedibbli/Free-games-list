from scrapers.steam_scraper import scrape_steam
from scrapers.gog_scraper import scrape_gog
from scrapers.epic_scraper import scrape_epic
from scrapers.google_play_scraper import scrape_google_play
from scrapers.prime_gaming_scraper import scrape_prime
from scrapers.humble_choice_scraper import scrape_humble_choice
from scrapers.save_to_file import save_to_file
from datetime import datetime

if __name__ == "__main__":
    # Run scrapers
    steam_games = scrape_steam()
    gog_games = scrape_gog()
    epic_games = scrape_epic()
    google_play_games = scrape_google_play()
    prime_gaming_games = scrape_prime()
    humble_choice_games = scrape_humble_choice()

    # Ensure that all platforms are included even if no games are found
    games_by_platform = {
        "Steam": steam_games if steam_games else [],
        "GOG": gog_games if gog_games else [],
        "Epic": epic_games if epic_games else [],
        "Google Play": google_play_games if google_play_games else [],
        "Prime Gaming": prime_gaming_games if prime_gaming_games else [],
        "Humble Choice": humble_choice_games if humble_choice_games else []
    }

    # Save scraped data to separate pages
    save_to_file(games_by_platform)
