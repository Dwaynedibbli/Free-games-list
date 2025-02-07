def save_to_file(games_by_platform):
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

            # Fix: Handle both tuples (Steam) and dictionaries (Other platforms)
            if games_by_platform[platform]:
                for game in games_by_platform[platform]:
                    if isinstance(game, tuple):  # Steam uses tuples
                        title, link = game
                    elif isinstance(game, dict):  # Others use dicts
                        title = game.get('title', 'Unknown Game')
                        link = game.get('link', '#')
                    else:
                        continue  # Skip invalid data

                    f.write(f'        <div class="game-item"><a href="{link}">{title}</a></div>\n')
            else:
                f.write('        <p>No free games available today.</p>\n')

            f.write('    </div>\n')
            f.write('    <footer><a href="index.html">Back to Home</a></footer>\n')
            f.write('</body>\n</html>\n')

    print("Separate HTML pages dynamically generated.")