import os
import shutil

# Define folders
scraper_output_folder = "scrapers/"
public_folder = "game_pages/"

# Ensure the folders exist
os.makedirs(scraper_output_folder, exist_ok=True)
os.makedirs(public_folder, exist_ok=True)

def save_to_file(filename, content):
    """
    Saves the scraped game list to a file inside 'scrapers/' 
    and then copies it to 'game_pages/' for GitHub Pages.
    """
    # Save file in scrapers/
    scraper_filepath = os.path.join(scraper_output_folder, filename)
    with open(scraper_filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Copy file to game_pages/
    public_filepath = os.path.join(public_folder, filename)
    shutil.copy(scraper_filepath, public_filepath)

    print(f"✅ Saved and copied: {filename}")

# Example usage
if __name__ == "__main__":
    # Test save function
    test_filename = "steam.html"
    test_content = "<html><body><h1>Test Steam Games</h1></body></html>"
    save_to_file(test_filename, test_content)