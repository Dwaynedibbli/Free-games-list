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
    Saves scraped game data to 'scrapers/' and copies it to 'game_pages/' for GitHub Pages.
    Ensures both filename and content are valid before saving.
    """
    if not filename or not content:
        print(f"⚠️ Error: Missing filename or content. Filename: {filename}, Content Length: {len(content) if content else 0}")
        return

    try:
        # Save file in scrapers/
        scraper_filepath = os.path.join(scraper_output_folder, filename)
        with open(scraper_filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # Copy file to game_pages/
        public_filepath = os.path.join(public_folder, filename)
        shutil.copy(scraper_filepath, public_filepath)

        print(f"✅ Successfully saved and copied: {filename}")

    except Exception as e:
        print(f"❌ Error saving file {filename}: {e}")

# Example usage
if __name__ == "__main__":
    # Test the function with dummy data
    test_filename = "test.html"
    test_content = "<html><body><h1>Test Page</h1></body></html>"
    save_to_file(test_filename, test_content)