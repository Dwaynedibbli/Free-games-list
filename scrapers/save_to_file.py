def save_to_file(games_by_platform):
    print("\n📢 DEBUG: Checking collected game data...\n")
    for platform, games in games_by_platform.items():
        print(f"🔹 {platform}: {len(games)} games found")
        for game in games:
            print(game)  # Print each game's data

    platform_files = {
        "Steam": "steam.html",
        "GOG": "gog.html",
        "Epic": "epic.html",
        "Google Play": "google_play.html",
        "Prime Gaming": "prime_gaming.html"
    }

    for platform, filename in platform_files.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'<!DOCTYPE html>\n<html lang="en">\n<head>\n')
            f.write('    <meta charset="UTF-8">\n')
            f.write('    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            f.write(f'    <title>{platform} Free Games</title>\n')
            f.write('    <link rel="stylesheet" href="style.css">\n')
            f.write('    <script src="scripts.js"></script>\n')
            f.write('</head>\n<body>\n')

            f.write(f'    <h1>{platform} Free Games</h1>\n')
            f.write('    <div class="game-list">\n')

            if games_by_platform[platform]:
                for game in games_by_platform[platform]:
                    if isinstance(game, tuple):  
                        title, link = game
                    elif isinstance(game, dict):  
                        title = game.get('title', 'Unknown Game')
                        link = game.get('link', '#')

                    if not link.startswith("http"):
                        link = f"https://{link}"

                    f.write(f'        <div class="game-item"><a href="{link}">{title}</a></div>\n')
            else:
                f.write('        <p>No free games available today.</p>\n')

            f.write('    </div>\n')
            f.write('    <footer><a href="index.html">Back to Home</a></footer>\n')
            f.write('</body>\n</html>\n')

    print("\n✅ DEBUG: Game data written successfully.\n")